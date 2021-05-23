<script>
	import { onDestroy } from 'svelte'
	import { fade } from 'svelte/transition';
	import { fetchOffers } from './utils.js'
	import { dateToHTML } from './date.js'
	import { getSum, getAvg, calculateRSI, checkLiquid, checkVolatile }
		from './calculate.js'
	import Chart from './components/Chart.svelte'
	import Loader from './components/Loader.svelte'
	

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
					let candidateVol = candidate.bids.vol[candidate.bids.vol.length-1]
					let currentVol = chart.bids.vol[chart.bids.vol.length-1]
					if (currentVol > candidateVol) candidate = chart
				} else candidate = chart
			}
		})
		return candidate
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
			bids.avg.push(getAvg(bids.rate, avg))
			asks.avg.push(getAvg(asks.rate, avg))
			// RSI
			bids.rsi.push(calculateRSI(bids.rate, rsi))
			asks.rsi.push(calculateRSI(asks.rate, rsi))
			// VOL
			bids.vol.push(getSum(bids.amount, vol))
			asks.vol.push(getSum(asks.amount, vol))
			// define the trend
			chart.trend = defineTrend(bids.rsi)
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
				candidate.volatile = checkVolatile(buys.rate,
					volatile.samples, volatile.percent)
				candidate.liquid = checkLiquid(bids.rate, asks.rate,
					liquid.samples, liquid.percent)
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
		{#if interval}<span transition:fade><Loader/></span>{/if}

		<div class="inputs">
			{#if charts[0].timestamps.length > 0}
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
			<div>
				<label>Volume:<br>
					<input type="number" min="0" bind:value={vol}> <small>samples</small>
				</label>
				<label>Average:<br>
					<input type="number" min="0" bind:value={avg}> <small>samples</small>
				</label>
				<label>RSI:<br>
					<input type="number" min="0" bind:value={rsi}> <small>samples</small>
				</label>
			</div>
			<div>
				<label>Volatile:<br>
					<input type="number" min="0" bind:value={volatile.percent}>
						<small>%</small>
					<input type="number" min="0" bind:value={volatile.samples}>
						<small>samples</small>
				</label>
				<label>Liquid:<br>
					<input type="number" min="0" bind:value={liquid.percent}>
						<small>%</small>
					<input type="number" min="0" bind:value={liquid.samples}>
						<small>samples</small>
				</label>
				<label>Normalize:<br>
					<input type=checkbox min="0" bind:checked={normalize}>
				</label>
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

	button {
		border-radius: 5px;
		height: 40px;
		width: 80px;
		font-weight: bold;
	}
	
	nav {
		margin-bottom: 7.5vh;
	}
	nav > span {
		margin-left: 10px;
	}

	.inputs {
		display: grid;
		grid-template-columns: 175px 250px auto;
  	grid-template-rows: auto auto;
	}
	.inputs > div {
		display: flex;
		flex-direction: column;
	}
	p, label {
		grid-column: span 3;
		margin-top: 15px;
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
