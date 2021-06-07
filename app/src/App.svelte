<script>
	import { onDestroy } from 'svelte'
	import { fade } from 'svelte/transition'
	import { fetchOffers } from './utils.js'
	import Chart from './components/Chart.svelte'
	import Loader from './components/Loader.svelte'
	import { getSum, getAvg, calculateRSI, checkLiquid, checkVolatile }
		from './calculate.js'
	import { format as formatDate, parseJSON as parseDate, 
		min as minDate, max as maxDate } from 'date-fns'


	const RESOURCES = ['BTC-PLN','ETH-PLN','LTC-PLN']
	const FETCH_FREQUENCY = 5   // seconds

	let interval
	let error

	let range = {
		min: { date: null, time: null },
		max: { date: null, time: null },
		set: { date: null, time: null }
	}
	let vol = 12
	let avg = 5
	let rsi = 5
	let volatile = { samples: 5, percent: 5 }
	let liquid   = { samples: 5, percent: 5 }
	let normalize = false

	let wallets = RESOURCES.map(resource => ({
		currency: resource,
		balance: 0,
		avg: null,
		buy:  { rate: null, amount: null },
		sell: { rate: null, amount: null }
	}))
	let currentWallet = 0

	let charts = RESOURCES.map(resource => ({
		currency: resource,
		bids: [], asks: [],
		buys: [], sells: [],
		bought: [], sold: [],
		trend: 0,
		candidate: false,
		volatile: false,
		liquid: false
	}))

	let filename = 'data'


	async function loadJSON() {
		let req = await fetch(`/load/${filename}`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' }
		})
		const json = await req.json()
		json.charts.forEach(chart => {
			for (const key in chart) {
				if (typeof chart[key] == 'object') {
					chart[key].forEach(elem => {
						elem.timestamp = parseDate(elem.timestamp)
					})
				}
			}
		})
		wallets = json.wallets
		charts = json.charts
		update()
	}

	async function saveJSON() {
		await fetch(`/save/${filename}`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ wallets: wallets, charts: charts	})
		})
	}

	function getBoughtAvg(chart) {
		return chart.bought.map(b => b.rate*b.amount).reduce((a,b) => a+b, 0)
		/ chart.bought.map(b => b.amount).reduce((a,b) => a+b, 0)
	}

	function transaction(key) {
		let wallet = wallets[currentWallet]
		let chart = charts.find(chart => chart.currency == wallet.currency)
		let type = key == 'buy' ? 'bought' : 'sold'
		let timestamp = new Date()
		add(chart[type], timestamp, wallet[key])
		let queue = chart.bought
		if (key == 'buy') {
			let avg = getBoughtAvg(chart)
			queue[queue.length-1].avg = avg
			wallet.avg = avg
		}	else if (key == 'sell') {
			for (const elem of queue) {
				let walletAmount = wallet.sell.amount
				wallet.sell.amount -= elem.amount
				if (wallet.sell.amount > 0) {
					wallet.balance +=	elem.amount * (wallet.sell.rate - elem.rate)
					elem.amount = 0
				} else {
					wallet.balance += walletAmount * (wallet.sell.rate - elem.rate)
					elem.amount = -wallet.sell.amount
					if (elem.amount < 0) elem.amount = 0
					break
				}
			}
			// remove empty boughts
			chart.bought = queue.filter(elem => elem.amount > 0)
			// calculate average
			let avg = getBoughtAvg(chart)
			chart.bought.push(
				{ timestamp: timestamp,	rate: null, amount: null, avg: avg })
			wallet.avg = avg
		}
		wallet[key] = { rate: null, amount: null }
		update()
	}

	function calculate(list, elem) {
		elem.avg = getAvg(list.map(b => b.rate), avg)
		elem.rsi = calculateRSI(list.map(b => b.rate), rsi)
		elem.vol = getSum(list.map(b => b.amount), vol)
	}

	function add(list, timestamp, fetched, callback) {
		let last = { timestamp: null, rate: null, amount: null }
		last.timestamp = timestamp
		last.rate = fetched.rate
		last.amount = fetched.amount
		list.push(last)
		if (callback)	callback(list, last)
	}

	function updateRange(chart) {
		let { bids, asks, buys, sells, bought, sold } = chart
		let data = [bids, asks, buys, sells, bought, sold]
		let dates = []
		data.forEach(list => { dates.push(...list.map(e => e.timestamp)) })
		if (dates.length > 0) {
			let minmax = { min: minDate(dates), max: maxDate(dates) }
			for (const key in minmax) {
				range[key].date = formatDate(minmax[key], 'yyyy-MM-dd')
				range[key].time = formatDate(minmax[key], 'HH:mm:ss')
			}
			if (!range.set.date) range.set.date = range.min.date
			if (!range.set.time) range.set.time = range.min.time
		}
	}

	function defineTrend(rsi) {
		if (rsi[rsi.length-1] > 70)	return 1
		if (rsi[rsi.length-1] < 30) return -1
		return 0
	}

	function chooseCandidate() {
		let candidate = null
		charts.forEach(chart => {
			if (chart.trend != -1) {
				if (candidate) {
					let candidateVols = candidate.bids.map(b => b.vol)
					let candidateVol = candidateVols[candidateVols.length-1]
					let currentVols = chart.bids.map(b => b.vol)
					let currentVol = currentVols[currentVols.length-1]
					if (currentVol > candidateVol) candidate = chart
				} else candidate = chart
			}
		})
		return candidate
	}

	function updateOffers() {
		charts.forEach(async (chart) => {
			let { bids, asks, buys, sells } = chart
			let { bid, ask } = await fetchOffers(chart.currency, 'orderbook-limited')
			let { buy, sell } = await fetchOffers(chart.currency, 'transactions')
			// add fetched values if available
			let timestamp = new Date()
			if (bid) add(bids, timestamp, bid, calculate)
			if (ask) add(asks, timestamp, ask, calculate)
			if (buy) add(buys, timestamp, buy)
			if (sell) add(sells, timestamp, sell)
			// define the trend
			chart.trend = defineTrend(bids.map(b => b.rsi))
			// reset candidates and choose one if possible
			let candidate = charts.find(chart => chart.candidate == true)
			let candidateNew = chooseCandidate()
			if (candidateNew && candidateNew != candidate) {
				if (candidate)
					candidate.candidate = candidate.volatile = candidate.liquid = false
				candidate = candidateNew
				candidate.candidate = true
			}
			if (candidate) {
				candidate.volatile = checkVolatile(
					buys.map(b => b.rate),
					volatile.samples, volatile.percent,
					false)
				candidate.liquid = checkLiquid(
					bids.map(b => b.rate), asks.map(b => b.rate),
					liquid.samples, liquid.percent,
					false)
			}
			update()
		})
	}

	function update() {
		// update wallets and charts
		wallets = wallets
		charts = charts
		// update the range input field
		charts.forEach((chart) => { updateRange(chart) })
	}

	function toggle() {
		if (interval)	stop()
		else interval = setInterval(updateOffers, FETCH_FREQUENCY*1000)
	}
	
	function stop() {
		clearInterval(interval)
		interval = false
	}

	onDestroy(() => {
		clearInterval(interval)
	})

	function buy(e) {
		if (e.key === 'Enter') transaction('buy')
	}

	function sell(e) {
		if (e.key === 'Enter') transaction('sell')
	}
</script>

<main>
	<nav>
		{#if error}{error}{/if}
	
		<button on:click={toggle} class="big {interval ? 'red' : 'green'}">
			{#if interval}Stop{:else}Start{/if}
		</button>
		{#if interval}<span transition:fade><Loader/></span>{/if}

		<div class="inputs">

			<label>Filename:
				<input type="text" bind:value={filename}>
				<button on:click={loadJSON}>Load</button>
				<button on:click={saveJSON}>Save</button>
			</label>

			{#if range.set.date}
				<label>Range from:
					<input type="date"
						bind:value={range.set.date}
						min={range.min.date} max={range.max.date}>
					<input type="time"
						bind:value={range.set.time}
						min={range.min.time} max={range.max.time}>
				</label>
			{:else}
				<p>Range from: <small class="red">no data</small></p>
			{/if}

			<div class="wallet">
				<p><b>Wallet</b></p>
				<select bind:value={currentWallet}>
					{#each RESOURCES as resource, i}
						<option value={i}>{resource}</option>
					{/each}
				</select>
				<p>Balance: {wallets[currentWallet].balance}</p>
				{#if wallets[currentWallet].avg}
					<p>Last average: {wallets[currentWallet].avg}</p>
				{/if}
				<form on:keydown={buy}>
					<label>Buy<br>
						<input type="number" placeholder="amount"
							bind:value={wallets[currentWallet].buy.amount}>
						<input type="number" placeholder="rate" step="0.001"
							bind:value={wallets[currentWallet].buy.rate}>
						{#if wallets[currentWallet].buy.rate != null &&
							wallets[currentWallet].buy.amount != null}
							<button on:click={()=>{ transaction('buy') }}>Submit</button>
						{/if}
					</label>
				</form>
				<form on:keydown={sell}>
					<label>Sell<br>
						<input type="number" placeholder="amount"
							bind:value={wallets[currentWallet].sell.amount}>
						<input type="number" placeholder="rate"
							bind:value={wallets[currentWallet].sell.rate}>
						{#if wallets[currentWallet].sell.rate != null &&
							wallets[currentWallet].sell.amount != null}
							<button on:click={()=>{ transaction('sell') }}>Submit</button>
						{/if}
					</label>
				</form>
			</div>

			<div>
				<label>Volume<br>
					<input type="number" min="0" bind:value={vol}> <small>samples</small>
				</label>
				<label>Average<br>
					<input type="number" min="0" bind:value={avg}> <small>samples</small>
				</label>
				<label>RSI<br>
					<input type="number" min="0" bind:value={rsi}> <small>samples</small>
				</label>
			</div>

			<div>
				<label>Volatile<br>
					<input type="number" min="0" bind:value={volatile.percent}>
						<small>%</small>
					<input type="number" min="0" bind:value={volatile.samples}>
						<small>samples</small>
				</label>
				<label>Liquid<br>
					<input type="number" min="0" bind:value={liquid.percent}>
						<small>%</small>
					<input type="number" min="0" bind:value={liquid.samples}>
						<small>samples</small>
				</label>
				<label>Normalize<br>
					<input type=checkbox min="0" bind:checked={normalize}>
				</label>
			</div>

			<div class="legend">
				<p><b>Legend</b></p>
				<div><img alt="trend up" src="/static/up.svg"><small>Upward trend</small></div>
				<div><img alt="trend flat" src="/static/flat.svg"><small>Steady trend</small></div>
				<div><img alt="trend down" src="/static/down.svg"><small>Downward trend</small></div>
				<div><img alt="candidate" src="/static/anchor.svg"><small>Candidate</small></div>
				<div><img alt="volatile asset" src="/static/volatile.svg"><small>Volatile asset</small></div>
				<div><img alt="liquid asset" src="/static/liquid.svg"><small>Liquid asset</small></div>
			</div>

		</div>
	</nav>

	{#each charts as chart}
		<Chart {...chart} range={range.set} {normalize}/>
	{/each}
</main>


<style>
	main {
		padding: 10vh 20vw;
	}
	
	nav {
		margin-bottom: 7.5vh;
	}
	nav > span {
		margin-left: 10px;
	}

	.inputs {
		display: grid;
		grid-template-columns: 270px 170px 250px 200px auto;
  	grid-template-rows: auto auto auto;
	}
	.inputs > div {
		display: flex;
		flex-direction: column;
	}
	p, label {
		grid-column: span 5;
	}

	.wallet select {
		border: none;
		padding: 5px 10px;
  }
  .wallet input[type='number'] {
		width: 110px;
	}
	.wallet select {
		width: 230px;
	}
	.wallet button {
		margin-top: 10px;
		padding-top: 0;
		padding-bottom: 0;
	}

	.legend {
		display: block;
	}
	.legend div {
		display: flex;
		align-items: center;
	}
	.legend img {
		margin-right: 10px;
		height: 25px;
	}
</style>
