<script>
	import Chart from 'chart.js/auto'
	import { onMount } from 'svelte'
	import { normalizeArray } from '../utils.js'
	import { dateToJS, sliceByDate } from '../date.js'

  export let currency
  export let timestamps
  export let bids
  export let asks
  export let range

  let canvas
  let chart
  
	$: {
		// get the index of the date from which to slice data
		let datetime = range.date+', '+range.time
		let timestamp = sliceByDate([timestamps], dateToJS(datetime), timestamps)
		let datasets = sliceByDate([
			bids.rate, asks.rate,
			bids.avg, asks.avg,
			bids.rsi, asks.rsi,
			bids.vol
		], datetime, timestamps)
      .map(d => normalizeArray(d))
		// draw on ctx
    if (chart) {
      chart.data.labels = timestamp
      for (let i=0; i < chart.data.datasets.length; i++)
        chart.data.datasets[i].data = datasets[i]
      chart.update()
    }
  }

  function newChart(canvas) {
    return new Chart(canvas, {
      type: 'line',
      data:	{ datasets: [{
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
      }] },
      options: {
        spanGaps: true,
        plugins: { legend: { position: 'right' } }
      }
    })
  }
  
	onMount(() => { chart = newChart(canvas)})
</script>


<h3>{currency}</h3>
<canvas width="400" height="150" bind:this={canvas}></canvas>


<style>
  h3 {
    margin-top: 20px;
  }
</style>
