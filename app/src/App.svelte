<script>
	import Chart from 'chart.js/auto'
	import { onMount, onDestroy } from 'svelte'
	import { fade } from 'svelte/transition';
	import { fetchOffers, normalizeArray } from './utils.js'
	import { dateToHTML, dateToJS, sliceByDate } from './date.js'
	import { calculateAverage, calculateRSI, calculateVolume } from './calculate.js'

	
	const RESOURCES = ['BTC-PLN','ETH-PLN','LTC-PLN']
	const API_ENDPOINT = 'orderbook-limited' // transactions / orderbook-limited
	const FETCH_FREQUENCY = 5   // seconds
	const VOLUME_FREQUENCY = 1/60 // hours

	let error

	let interval

	let range = {
		min: { date: null, time: null },
	  max: { date: null, time: null },
		set: { date: null, time: null }
	}
	let avg = 5
	let rsi = 5

	let charts = RESOURCES.map(resource => {
		return {
			currency: resource,
			canvas: null,
			ctx: null,
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
		range.max.date = max.split(', ')[0]
		range.min.time = min.split(', ')[1]
		range.max.time = max.split(', ')[1]
		// set the date and time input fields if unset
		if (!range.set.date) range.set.date = range.min.date
		if (!range.set.time) range.set.time = range.min.time
	}

	function updateChart(chart) {
		let { timestamps, bids, asks } = chart
		updateRange(timestamps)
		// get the index of the date from which to slice data
		let datetime = range.set.date+', '+range.set.time
		let timestamp = sliceByDate([timestamps], dateToJS(datetime), timestamps)
		let data = sliceByDate([
			bids.rate, asks.rate,
			bids.avg, asks.avg,
			bids.rsi, asks.rsi,
			bids.vol
		], datetime, timestamps)
		data = data.map(d => normalizeArray(d))
		// draw on ctx
		let ctx = chart.ctx
		ctx.data.labels = timestamp
		for (let i=0; i < ctx.data.datasets.length; i++)
			ctx.data.datasets[i].data = data[i]
		ctx.update()
	}

	function updateOffers() {
		charts.forEach(async (chart) => {
			let { timestamps, bids, asks } = chart
			let { bid, ask } = await fetchOffers(chart.currency, API_ENDPOINT)
			// push a timestamp
			timestamps.push( (new Date).toLocaleString() )
			// push new base values
			bids.rate.push(bid.rate)
			asks.rate.push(ask.rate)
			bids.amount.push(bid.amount)
			asks.amount.push(ask.amount)
			// calculate and push additional values
			bids.avg.push(calculateAverage(bids.rate, avg))
			console.log(bids.avg);
			asks.avg.push(calculateAverage(asks.rate, avg))
			bids.rsi.push(calculateRSI(bids.rate, rsi))
			asks.rsi.push(calculateRSI(asks.rate, rsi))
			bids.vol.push(calculateVolume(bids.amount, VOLUME_FREQUENCY, timestamps))
			asks.vol.push(calculateVolume(asks.amount, VOLUME_FREQUENCY, timestamps))
			// draw new values on the chart
			updateChart(chart)
		})
	}

	function newChart(canvas) {
		return new Chart(canvas, {
			type: 'line',
			data:	{
				datasets: [
					{
						label: 'Bids',
						fill: false,
						borderColor: 'rgb(255, 170, 0)',
						tension: 0
					},{
						label: 'Asks',
						fill: false,
						borderColor: 'rgb(43, 192, 255)',
						tension: 0
					},{
						label: 'Bids average',
						borderColor: 'rgb(255, 213, 130)',
						borderDash: [10,5],
						tension: 0.5
					},{
						label: 'Asks average',
						borderColor: 'rgb(171, 230, 255)',
						borderDash: [10,5],
						tension: 0.5
					},{
						label: 'Bids RSI',
						borderColor: 'rgb(135, 114, 73)',
						borderDash: [5,3],
						tension: 0.5
					},{
						label: 'Asks RSI',
						borderColor: 'rgb(92, 124, 138)',
						borderDash: [5,3],
						tension: 0.5
					},{
						label: 'Volume',
						type: 'bar',
						borderColor: 'rgb(143, 235, 198)',
						backgroundColor: 'rgba(143, 235, 198, 0.3)'
					}
				]
			},
			options: {
				spanGaps: true,
				plugins: { legend: { position: 'right' } }
			}
		})
	}

	onMount(() => {
		charts.forEach(chart => {
			chart.ctx = newChart(chart.canvas)
		})
	})

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
				min={range.min.date} max={range.max.date}
				on:change={() => { charts.forEach(chart => updateChart(chart)) }}>
			<input type="time"
				bind:value={range.set.time}
				min={range.min.time} max={range.max.time}
				on:change={() => { charts.forEach(chart => updateChart(chart)) }}>
		</p>
		<p>Moving average: <input type="number" bind:value={avg}> samples</p>
		<p>RSI: <input type="number" bind:value={rsi}> samples</p>
	</nav>

	{#each charts as chart}
		<h3>{chart.currency}</h3>
		<canvas width="400" height="150" bind:this={chart.canvas}></canvas>
		<br>
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
		width: 60px;
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
