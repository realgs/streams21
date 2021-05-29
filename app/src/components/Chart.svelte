<script>
	import Chart from 'chart.js/auto'
	import { onMount } from 'svelte'
	import { fade } from 'svelte/transition';
  import { normalizeArray } from '../utils.js';
	import { dateToJS, sliceByDate } from '../date.js'


  export let currency
	export let timestamps
  export let bids, asks
	export let buys, sells
  export let trend
  export let candidate, volatile, liquid

  export let range
  export let normalize

  let canvas
  let chart
  
	$: if (chart) {
    // get the index of the date from which to slice data
    let datetime = range.date+', '+range.time
    let timestampsEdited = editTimestamps(datetime)
    let datasets = sliceByDate([
      bids.rate, asks.rate,
      bids.avg,  asks.avg,
      bids.rsi,  asks.rsi,
			buys.rate, sells.rate,
      bids.vol
    ], datetime, timestamps)
    if (normalize) {
      datasets = datasets.map((dataset, i) => {
        if (i == 4 || i == 5) return dataset
        else return normalizeArray(dataset)
      })
    }
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
      },{
        label: 'Asks',
        yAxisID: 'VALUES',
        borderColor: 'rgb(0, 170, 255)',
      },{
        label: 'Bids Average',
        yAxisID: 'VALUES',
        borderColor: 'rgb(255, 173, 51)',
        borderDash: [20,5],
        tension: 0.5
      },{
        label: 'Asks Average',
        yAxisID: 'VALUES',
        borderColor: 'rgb(51, 187, 255)',
        borderDash: [20,5],
        tension: 0.5
      },{
        label: 'Bids RSI',
        yAxisID: 'RSI',
        borderColor: 'rgb(179, 107, 0)',
        borderDash: [12,5],
        tension: 0.5
      },{
        label: 'Asks RSI',
        yAxisID: 'RSI',
        borderColor: 'rgb(0, 119, 179)',
        borderDash: [12,5],
        tension: 0.5
      },{
        label: 'Buys',
        yAxisID: 'VALUES',
        borderColor: 'rgb(102, 61, 0)',
        borderDash: [5,4],
      },{
        label: 'Sells',
        yAxisID: 'VALUES',
        borderColor: 'rgb(0, 68, 102)',
        borderDash: [5,4],
      },{
        label: 'Volume',
        type: 'bar',
        yAxisID: 'VOLUME',
        borderColor: 'rgb(204, 238, 255)',
        backgroundColor: 'rgba(204, 238, 255, 0.75)'
      }] },
      options: {
        fill: false,
        interaction: { intersect: false },
        radius: 0,
				tension: 0,
        spanGaps: true,
        plugins: { legend: { position: 'bottom' } },
        scales: {
          VALUES: {
            title: { text: 'Rate', display: true },
            position: 'left',
          },
          RSI: {
            title: { text: 'RSI', display: true },
						position: 'right',
						min: 0, max: 100,
						grid: { drawOnChartArea:false }
					},
          VOLUME: {
            title: { text: 'Volume', display: true },
            position: 'right',
            grid: { drawOnChartArea: false }
          },
        }
      }
    })
  }
  
	onMount(() => { chart = newChart(canvas)})
</script>


<h3>
  {currency}
  <div class="icons">
    {#if trend == 1}
      <img alt="trend up" class="trend" src="/static/up.svg">
    {:else if trend == 0}
      <img alt="trend flat" class="trend" src="/static/flat.svg">
    {:else if trend == -1}
      <img  alt="trend down" class="trend" src="/static/down.svg">
    {/if}
    {#if candidate}
      <img transition:fade alt="candidate" src="/static/anchor.svg">
    {/if}
    {#if volatile}
      <img transition:fade alt="volatile asset" src="/static/volatile.svg">
    {/if}
    {#if liquid}
      <img transition:fade alt="liquid asset" src="/static/liquid.svg">
    {/if}
  </div>
</h3>
<canvas width="100" height="40" bind:this={canvas}></canvas>


<style>
  h3 {
    position: relative;
    margin-top: 20px;
  }
  .icons {
    position: absolute;
    display: flex;
    flex-direction: column;
    top: 0;
    left: 0;
    transform: translate(calc(-100% - 20px), -3px);
  }
  .icons > img {
    height: 30px;
    margin-bottom: 10px;
  }
  .icons > .trend {
    border-radius: 10px;
    background-color: #ffffff;
  }
</style>
