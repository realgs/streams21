<script>
	import FinanceChart from './components/FinanceChart.svelte';
	import Wallet from "./components/Wallet.svelte";
	import { 
		fetchTransactions, fetchBestOffers, calculateAvgLastTransaction, calculateRSI,
		getTrendSymbol, downloadJSON
	} from './utils'

	import { avgBuyRate, calculateProfit, Transaction } from './wallet'
	import { onDestroy } from "svelte";

	// Config
	const UPDATE_INTERVAL = 5000;
	const CURRENCY_PAIRS = ['BTC-PLN'];
	const RSI_PERIOD = 5;
	const TREND_SYMBOL_PERIOD = 2;

	const lastTransactionsFetch = Array.from(Array(CURRENCY_PAIRS.length), () => Date.now());
	const chartsData = CURRENCY_PAIRS.map((currencyPair, i) => {
		return  {
			id: i,
			currencyPair,
			transactions: [],
			volumes: [],
			buysOffers: [],
			sellsOffers: [],
			rsi: [],
			rsiPeriod: RSI_PERIOD,
			trendSymbol: '',
			isCandidate: false,
			isVolatileAsset: false,
			isLiquidAsset: false,
			profit: 0,
			avgBuyRate: null
		}
	});

	let userTransactions = [];

	function updateCharts() {
		CURRENCY_PAIRS.forEach(async (currencyPair, i) => {
			function appendChartData(name, value) {
				chartsData[i][name][chartsData[i][name].length] = value;
			}

			const { success: tSuccess, data: tData } = await fetchTransactions(currencyPair, lastTransactionsFetch[i], 5);
			const { success: oSuccess, data: oData } = await fetchBestOffers(currencyPair);
			
			if (tSuccess) {
				lastTransactionsFetch[i] = tData['time'];
				const { rate, volume } = calculateAvgLastTransaction(tData);

				if (!!volume) {
					appendChartData('transactions', { x: lastTransactionsFetch[i], y: rate });
					appendChartData('volumes', { x: lastTransactionsFetch[i], y: volume });

					const calculatedRSI = calculateRSI(chartsData[i]['transactions'], RSI_PERIOD);

					if (calculatedRSI !== -1) 
						appendChartData('rsi', { x: lastTransactionsFetch[i], y: calculatedRSI });
				}
			} else
				console.error(tData);

			if (oSuccess) {
				appendChartData('buysOffers', { x: oData['time'], y: oData['buy'] });
				appendChartData('sellsOffers', { x: oData['time'], y: oData['sell'] });
			} else
				console.error(tData);

			chartsData[i]['trendSymbol'] = getTrendSymbol(chartsData[i]['rsi'], TREND_SYMBOL_PERIOD);
		});
	}

	const interval = setInterval(() => updateCharts(), UPDATE_INTERVAL);

	onDestroy(() => {
		clearInterval(interval);
	});
	
	function onSell(event) {
		const currencyPair = event.detail.currencyPair;
		updateProfit(currencyPair);
		updateAvgBuyRate(currencyPair);
	}

	function onBuy(event) {
		const currencyPair = event.detail.currencyPair;
		updateAvgBuyRate(currencyPair);
	}

	function updateProfit(currencyPair) {
		chartsData[CURRENCY_PAIRS.indexOf(currencyPair)]['profit'] = calculateProfit(currencyPair, userTransactions);
	}

	function updateAvgBuyRate(currencyPair) {
		const avg = avgBuyRate(currencyPair, userTransactions);
		chartsData[CURRENCY_PAIRS.indexOf(currencyPair)]['avgBuyRate']	= avg;
	}

	function onWalletDownloadRequested(event) {
		downloadJSON(userTransactions, 'user-wallet-transactions');
	}

	function onTransactionFileLoaded(event) {
		const file = event.detail.file;
		const reader = new FileReader();

		reader.onload = () => {
			const parsed = JSON.parse(reader.result);
			if (!parsed || !Array.isArray(parsed)) {
				alert('Loaded file is corrupted!');
				return;
			}

			const newTransactions = [];
			for (let transaction of parsed)
				newTransactions.push(Object.assign(new Transaction, transaction));
			

			userTransactions = newTransactions;

			CURRENCY_PAIRS.forEach((currencyPair) => {
				updateAvgBuyRate(currencyPair);
				updateProfit(currencyPair)
			});
			
			alert('Transactions file loaded successfully!')
		};
		reader.readAsText(file)
	}

</script>

<div id="container">
	<h1>Live crypto transactions wallet</h1>
	<div id="charts">
		{#each CURRENCY_PAIRS as _, i}
			<FinanceChart data={chartsData[i]} />
		{/each}
	</div>
	<Wallet 
	{CURRENCY_PAIRS}
	{userTransactions}
	on:sell={onSell}
	on:buy={onBuy}
	on:walletDownloadRequested={onWalletDownloadRequested}
	on:transactionFileLoaded={onTransactionFileLoaded}
	/>
</div>

<style>
	h1 {
		text-align: center;
		margin-bottom: 40px;
	}

	div#container {
		width: 80%;
		margin: auto;
		background-color: rgb(0, 0, 128, 0.2);
		padding: 30px;
		border-radius: 25px;
	}
</style>