<script>
	import { Transaction, sumVolume } from '../wallet'
	import { createEventDispatcher } from 'svelte';

	export let CURRENCY_PAIRS;
	export let userTransactions;
	let files;

	const dispatch = createEventDispatcher();

	const TRANSACTIONS_TYPES = ['Buy', 'Sell'];

	let transactionType, amount, amountCurrencyIndex, price;

	$: if(files) {
		dispatch('transactionFileLoaded', {file: files[0]});
	}

	function addNewTransaction() {
		if (amount == undefined || amount == 0 || price == undefined || price == 0) {
			alert('Amount or price is invalid.')
			return;
		}

		let currencyPair = CURRENCY_PAIRS[amountCurrencyIndex];
		
		if (transactionType === 'Sell' && sumVolume(currencyPair, userTransactions) - amount < 0) {
			alert('You do not have sufficient crypto!');
			return;
		}

		userTransactions[userTransactions.length] = new Transaction(
			transactionType,
			CURRENCY_PAIRS[amountCurrencyIndex],
			 amount,
			 price,
		);

		if (transactionType === 'Sell')
			dispatch('sell', {currencyPair});
		else
			dispatch('buy', {currencyPair});
	}

	function downloadCurrentWallet() {
		dispatch('walletDownloadRequested');
	}
</script>

<div id="panel">
	<h2>Wallet</h2>
	<form>
		<ul>
			<li>
				<label for='userTransactions'>Load wallet configuration</label>
				<input id='userTransactions' type='file' accept='.json' bind:files>
			</li>
			{#if userTransactions.length}
			<li>
				<label for='download'>Download current wallet configuration</label>
				<button id='download' on:click|preventDefault={downloadCurrentWallet}>⬇︎</button>
			</li>
			{/if}

		</ul>
	</form>
	<h2>Wallet transactions</h2>
	<form >
		<ul>
			<li>
				<select bind:value={transactionType}>
					{#each TRANSACTIONS_TYPES.map((v) => v.split("-")[0]) as transactionType}
						<option value={transactionType}>
							{transactionType}
						</option>
					{/each}
				</select>
			</li>
			<li>
				<label for="amount">Volume</label>
				<input id="amount" type="number" min="0"  bind:value={amount} />

				<select bind:value={amountCurrencyIndex}>
					{#each CURRENCY_PAIRS.map((v) => v.split("-")[0]) as currencyPair, i}
						<option value={i}>
							{currencyPair}
						</option>
					{/each}
				</select>
			</li>
			<li>
				<label for='price'>Price</label>
				<input id='price' type='number' min="0" bind:value={price} />
				{#if amountCurrencyIndex !== undefined}
					{CURRENCY_PAIRS[amountCurrencyIndex].split("-")[1]}
				{/if}
			</li>
			<li>
				<button on:click|preventDefault={addNewTransaction}>
					Add
				</button>
			</li>
		</ul>
	</form>
	{#if userTransactions.length}
	<table>
		<tr>
			<th>Type</th>
			<th>Volume</th>
			<th>Price</th>
			<th>Rate</th>
		</tr>
		{#each userTransactions as transaction}
		<tr>
			<td>{transaction.type.toUpperCase()}</td>
			<td>{transaction.volume} {transaction.volumeCurrency}</td>
			<td>{transaction.price} {transaction.priceCurrency}</td>
			<td>{transaction.rate} {transaction.priceCurrency}</td>
		</tr>
		{/each}
	</table>
	{/if}
</div>

<style>
	div#panel {
		margin: auto;
		background-color: rgb(0, 0, 128, 0.25);
		border-radius: 10px;
		padding: 15px;
		margin: 20px
	}

	form {
		display: block;
		margin: auto;
		text-align: center;
	}

	h2 {
		text-align: center;
		padding: 20px;
	}

	label {
		font-weight: bold;
		margin: 10px;
	}

	li {
		display: inline-block;
		padding: 5px;
	}

	button#download {
		width: 100px;
	}

	table {
		width: 100%;
		text-align: center;
		border-collapse: collapse;
	}
	table, td, th {
  		border: 1px solid rgba(0, 0, 0);
		padding: 10px;
		background-color: white;
	}
</style>
