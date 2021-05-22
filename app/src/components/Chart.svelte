<script>
	import Chart from 'chart.js/auto'
	import { onMount } from 'svelte'
	import { normalizeArray } from '../utils.js'
	import { dateToJS, sliceByDate } from '../date.js'

  export let currency
  export let timestamps
  export let bids
  export let asks
  export let trend
  export let candidate

  export let range

  let canvas
  let chart
  
	$: if (chart) {
    // get the index of the date from which to slice data
    let datetime = range.date+', '+range.time
    let timestampsEdited = editTimestamps(datetime)
    let datasets = sliceByDate([
      bids.rate, asks.rate,
      bids.avg, asks.avg,
      bids.rsi, asks.rsi,
      bids.vol
    ], datetime, timestamps)
    chart.data.labels = timestampsEdited
    for (let i=0; i < chart.data.datasets.length; i++)
      chart.data.datasets[i].data = datasets[i]
    chart.update()
  }

  function editTimestamps(datetime) {
    let sliced = sliceByDate([timestamps], dateToJS(datetime), timestamps)
    if (sliced.length == 1) {
      return [sliced[0].split(', ')[1]]
    } else if (sliced.length >= 2) {
      let minDate = sliced[0].split(', ')[0]
      let maxDate = sliced[sliced.length-1].split(', ')[0]
      if (minDate == maxDate) {
        return sliced.map(timestamp => {
          return timestamp.split(', ')[1]
        })
      } 
    }
    return sliced
  }

  function newChart(canvas) {
    return new Chart(canvas, {
      type: 'line',
      data:	{ datasets: [{
        label: 'Bids',
        yAxisID: 'VALUES',
        borderColor: 'rgb(255, 153, 0)',
        tension: 0
      },{
        label: 'Asks',
        yAxisID: 'VALUES',
        borderColor: 'rgb(0, 170, 255)',
        tension: 0
      },{
        label: 'Avg',
        yAxisID: 'VALUES',
        borderColor: 'rgb(255, 173, 51)',
        borderDash: [10,5],
        tension: 0.5
      },{
        label: 'Avg',
        yAxisID: 'VALUES',
        borderColor: 'rgb(51, 187, 255)',
        borderDash: [10,5],
        tension: 0.5
      },{
        label: 'RSI',
        yAxisID: 'RSI',
        borderColor: 'rgb(179, 107, 0)',
        borderDash: [5,3],
        tension: 0.5
      },{
        label: 'RSI',
        yAxisID: 'RSI',
        borderColor: 'rgb(0, 119, 179)',
        borderDash: [5,3],
        tension: 0.5
      },{
        label: 'Vol',
        type: 'bar',
        yAxisID: 'VOLUME',
        borderColor: 'rgb(204, 238, 255)',
        backgroundColor: 'rgba(204, 238, 255, 0.75)'
      }] },
      options: {
        fill: false,
        interaction: { intersect: false },
        radius: 0,
        spanGaps: true,
        plugins: { legend: { position: 'bottom' } },
        scales: {
          VALUES: { position: 'left' },
          RSI:    { position: 'right', grid: { drawOnChartArea: false } },
          VOLUME: { position: 'right', grid: { drawOnChartArea: false } },
        }
      }
    })
  }
  
	onMount(() => { chart = newChart(canvas)})
</script>


<h3>
  {currency}
  {#if trend == 1}
    <img class="icon trend" src="/static/up.svg" alt="trend up">
  {:else if trend == 0}
    <img class="icon trend" src="/static/flat.svg" alt="trend flat">
  {:else if trend == -1}
    <img class="icon trend" src="/static/down.svg" alt="trend down">
  {/if}
  {#if candidate}
    <img class="icon candidate" src="/static/anchor.svg" alt="candidate">
  {/if}
</h3>
<canvas width="100" height="40" bind:this={canvas}></canvas>


<style>
  h3 {
    position: relative;
    margin-top: 20px;
  }
  .icon {
    position: absolute;
    left: 0;
    transform: translate(calc(-100% - 20px), -50%);
    height: 30px;
  }
  .trend {
    top: 50%;
  }
  .candidate {
    top: calc(150% + 20px);
  }
</style>
