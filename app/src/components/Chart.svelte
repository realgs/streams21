<script>
	import Chart from 'chart.js/auto'
  import 'chartjs-adapter-date-fns'
  import { pl } from 'date-fns/locale';
	import { onMount } from 'svelte'
	import { fade } from 'svelte/transition'
  import { normalizeArray, copyDatasets } from '../utils.js'
  import { closestIndexTo as closestIndexToDate, add as addDate }
    from 'date-fns'


  export let currency
  export let bids, asks
	export let buys, sells
  export let bought, sold
  export let trend
  export let candidate, volatile, liquid

  export let range
  export let normalize

  let canvas
  let chart


  function sliceDatasets(data, timestamp) {
    const datasets = data.map(d => {
      let timestamps = d.map(elem => elem.timestamp)
      let i = closestIndexToDate(timestamp, timestamps)
      return d.slice(i)
    })
    if (datasets.length == 1)
      return datasets[0]
    return datasets
  }

  function normalizeDatasets(data) {
    const datasets = copyDatasets(data).map(d => {
      if (d.length > 0) {
        for (const key in d[0]) {
          if (!['timestamp','rsi'].includes(key)) {
            let values = d.map(elem => elem[key])
            values = normalizeArray(values)
            d.forEach((elem, i) => { elem[key] = values[i] })
          }
        }
      }
      return d
    })
    if (datasets.length == 1)
      return datasets[0]
    return datasets
  }

  function transformDatasets(data) {
    const datasets = copyDatasets(data).map(d => {
      d.forEach(elem => {
        for (const key in elem) {
          if (key != 'timestamp')
            elem[key] = { x: elem.timestamp, y: elem[key] }
        }
      })
      return d
    })
    if (datasets.length == 1)
      return datasets[0]
    return datasets
  }


	$: if (chart) {
    if (range.date && range.time) {
      // get set range date
      let date = new Date(...range.date.split('-'), ...range.time.split(':'))
      date = addDate(date, { months: -1 })
      // modify datasets
      let datasets = sliceDatasets([bids, asks, buys, sells, bought, sold], date)
      if (normalize)
        datasets = normalizeDatasets(datasets)
      datasets = transformDatasets(datasets)
      // define which data to display on each axis
      let data = [
        datasets[5].map(d => d.rate), // sold rate
        datasets[4].map(d => d.rate), // bought rate
        datasets[4].map(d => d.avg),  // bought/sold avg
        datasets[0].map(d => d.rate), // bids rate
        datasets[1].map(d => d.rate), // asks rate
        datasets[0].map(d => d.avg),  // bids avg
        datasets[1].map(d => d.avg),  // asks avg
        datasets[0].map(d => d.rsi),  // bids rsi
        datasets[1].map(d => d.rsi),  // asks rate
        datasets[2].map(d => d.rate), // buys rate
        datasets[3].map(d => d.rate), // sells rate
        datasets[0].map(d => d.vol),  // bids vol
      ]
      for (let i=0; i < chart.data.datasets.length; i++)
        chart.data.datasets[i].data = data[i]
      chart.update()
    }
  }

  function newChart(canvas) {
    return new Chart(canvas, {
      type: 'line',
      data:	{ datasets: [{
        label: 'Sold',
        backgroundColor: 'rgb(16, 237, 12)',
        radius: 4,
        showLine: false
      },{
        label: 'Bought',
        backgroundColor: 'rgb(134, 23, 226)',
        radius: 4,
        showLine: false
      },{
        label: 'Bought Average',
        borderColor: 'rgb(181, 25, 255)',
        tension: 0.5
      },{
        label: 'Bids',
        borderColor: 'rgb(255, 153, 0)'
      },{
        label: 'Asks',
        borderColor: 'rgb(0, 170, 255)'
      },{
        label: 'Bids Average',
        borderColor: 'rgb(255, 173, 51)',
        borderDash: [20,5],
        tension: 0.5
      },{
        label: 'Asks Average',
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
        borderColor: 'rgb(102, 61, 0)',
        borderDash: [5,4]
      },{
        label: 'Sells',
        borderColor: 'rgb(0, 68, 102)',
        borderDash: [5,4]
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
          x: {
            type: 'time',
            adapters: { date: { locale: pl } }
          },
          y: { type: 'linear' },
          RSI: {
						position: 'right',
						min: 0, max: 100,
						grid: { drawOnChartArea:false }
					},
          VOLUME: { position: 'right', grid: { drawOnChartArea: false } },
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
      <img alt="trend down" class="trend" src="/static/down.svg">
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
