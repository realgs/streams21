<script>
	import { onDestroy } from 'svelte'
	import { fade } from 'svelte/transition';
	import { fetchOffers } from './utils.js'
	import { dateToHTML } from './date.js'
	import { calculateAverage, calculateRSI, calculateVolume } from './calculate.js'
	import Chart from './components/Chart.svelte'

	
	const RESOURCES = ['BTC-PLN','ETH-PLN','LTC-PLN']
	const API_ENDPOINT = 'orderbook-limited' // transactions / orderbook-limited
	const FETCH_FREQUENCY = 5   // seconds

	let interval
	let error

	let range = {
		min: { date: null, time: null },
	  max: { date: null, time: null },
		set: { date: null, time: null }
	}
	let vol = 1/60
	let avg = 5
	let rsi = 5

	let charts = RESOURCES.map(resource => {
		return {
			currency: resource,
			timestamps: [],
			bids: { rate: [], amount: [], avg: [], rsi: [], vol: [] },
			asks: {	rate: [], amount: [], avg: [], rsi: [], vol: [] }
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
			let { timestamps, bids, asks } = chart
			let { bid, ask } = await fetchOffers(chart.currency, API_ENDPOINT)
			// push a timestamp
			timestamps.push( (new Date).toLocaleString() )
			updateRange(timestamps)
			// push new base values
			bids.rate.push(bid.rate)
			asks.rate.push(ask.rate)
			bids.amount.push(bid.amount)
			asks.amount.push(ask.amount)
			// calculate and push additional values
			bids.avg.push(calculateAverage(bids.rate, avg))
			asks.avg.push(calculateAverage(asks.rate, avg))
			bids.rsi.push(calculateRSI(bids.rate, rsi))
			asks.rsi.push(calculateRSI(asks.rate, rsi))
			bids.vol.push(calculateVolume(bids.amount, vol, timestamps))
			asks.vol.push(calculateVolume(asks.amount, vol, timestamps))
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
		{#if interval}
			<span transition:fade>running on <b>/{API_ENDPOINT}</b></span>
		{/if}

		<p>
			Range from:
			<input type="date"
				bind:value={range.set.date}
				min={range.min.date} max={range.max.date}>
			<input type="time"
				bind:value={range.set.time}
				min={range.min.time} max={range.max.time}>
		</p>
		<p>Volume frequency: <input type="number" bind:value={vol}> hours</p>
		<p>Moving average: <input type="number" bind:value={avg}> samples</p>
		<p>RSI: <input type="number" bind:value={rsi}> samples</p>
	</nav>

	{#each charts as chart}
		<Chart {...chart} range={range.set}/>
	{/each}
</main>


<style>
	main {
		padding: 10vh 20vw;
	}
	nav {
		margin-bottom: 5vh;
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
	input[type='number'] {
		width: 70px;
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
