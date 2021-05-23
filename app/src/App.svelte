<script>
	import { onDestroy } from 'svelte'
	import { fade } from 'svelte/transition';
	import { fetchOffers } from './utils.js'
	import { dateToHTML } from './date.js'
	import { calculateAverage, calculateRSI, calculateVolume }
		from './calculate.js'
	import Chart from './components/Chart.svelte'

	
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
	let normalize = false

	let charts = RESOURCES.map(resource => {
		return {
			currency: resource,
			timestamps: [],
			bids:  { rate: [], amount: [], avg: [], rsi: [], vol: [] },
			asks:  { rate: [], amount: [], avg: [], rsi: [], vol: [] },
			buys:  { rate: [], amount: [] },
			sells: { rate: [], amount: [] },
			trend: 0,
			candidate: false,
			volatile: false,
			liquid: false
		}
	})

	function updateRange(timestamps) {
		// set min and max values
		const min = dateToHTML(timestamps[0])
		const max = dateToHTML(timestamps[timestamps.length-1])
		range.min.date = min.split(', ')[0]
		range.min.time = min.split(', ')[1]
		range.max.date = max.split(', ')[0]
		range.max.time = max.split(', ')[1]
		// set the date and time input fields if unset
		if (!range.set.date) range.set.date = range.min.date
		if (!range.set.time) range.set.time = range.min.time
	}

	function update() {
		charts.forEach(async (chart) => {
			let { timestamps, bids, asks, buys, sells } = chart
			let { bid, ask } = await fetchOffers(chart.currency, 'orderbook-limited')
			let { buy, sell } = await fetchOffers(chart.currency, 'transactions')
			// push a timestamp
			timestamps.push( (new Date).toLocaleString() )
			updateRange(timestamps)
			// base values
			bids.rate.push(bid.rate)
			asks.rate.push(ask.rate)
			bids.amount.push(bid.amount)
			asks.amount.push(ask.amount)
			buys.rate.push(buy.rate)
			sells.rate.push(sell.rate)
			buys.amount.push(buy.amount)
			sells.amount.push(sell.amount)
			// additional values
			// AVG
			bids.avg.push(calculateAverage(bids.rate, avg))
			asks.avg.push(calculateAverage(asks.rate, avg))
			// RSI
			bids.rsi.push(calculateRSI(bids.rate, rsi))
			asks.rsi.push(calculateRSI(asks.rate, rsi))
			// defining the trend
			if (bids.rsi[bids.rsi.length-1] > 70)	chart.trend = 1
			else if (bids.rsi[bids.rsi.length-1] < 30) chart.trend = -1
			else chart.trend = 0
			// VOL
			bids.vol.push(calculateVolume(bids.amount, vol, timestamps))
			asks.vol.push(calculateVolume(asks.amount, vol, timestamps))
			// choose a candidate if possible
			let candidate = charts.find(chart => chart.candidate == true)
			if (chart.trend != -1) {
				let assign = false
				if (candidate) {
					let candidateVol = candidate.bids.vol[candidate.bids.vol.length-1]
					let currentVol = bids.vol[bids.vol.length-1]
					if (currentVol > candidateVol || candidate.trend == -1) {
						candidate.candidate = false
						candidate.volatile = false
						candidate.liquid = false
						assign = true
					}
				} else assign = true
				if (assign) {
					chart.candidate = true
					chart.volatile = true
					chart.liquid = true
				}
			}
			charts = charts
		})
	}

	function toggle() {
		if (interval)	stop()
		else interval = setInterval(update, FETCH_FREQUENCY*1000)
	}
	
	function stop() {
		clearInterval(interval)
		interval = false
	}

	onDestroy(() => {
		clearInterval(interval)
	})
</script>

<main>
	<nav>
		{#if error}{error}{/if}
	
		<button on:click={toggle} class="{interval ? 'red' : 'green'}">
			{#if interval}Stop{:else}Start{/if}
		</button>
		{#if interval}<span transition:fade>running...</span>{/if}

		<div class="inputs">
			<label>Range from:
				<input type="date"
					bind:value={range.set.date}
					min={range.min.date} max={range.max.date}>
				<input type="time"
					bind:value={range.set.time}
					min={range.min.time} max={range.max.time}>
			</label>
			<label>Volume:
				<input type="number" min="0" bind:value={vol}> <small>samples</small>
			</label>
			<label>Moving average:
				<input type="number" min="0" bind:value={avg}> <small>samples</small>
			</label>
			<label>RSI:
				<input type="number" min="0" bind:value={rsi}> <small>samples</small>
			</label>
			<label>Normalize:
				<input type=checkbox min="0" bind:checked={normalize}>
			</label>
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
		font-size: small;
	}

	button {
		border-radius: 5px;
		height: 40px;
		width: 80px;
		font-weight: bold;
	}

	.inputs {
		display: flex;
		flex-direction: column;
	}
	label {
		margin-top: 10px;
	}
	input {
		border: none;
		padding: 5px 10px;
	}
	input[type='number'] {
		width: 60px;
	}
	input[type='checkbox'] {
		width: 18px;
		height: 18px;
	}

	.red {
		color: #ff6464;
		border-color: #ff6464;
		background-color: #fee;
	}
	.green {
		color: #05d432;
		border-color: #05d432;
		background-color: #efe;
	}
</style>
