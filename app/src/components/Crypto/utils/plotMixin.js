export default {
  data: () => ({ currentRSI: null }),
  computed: {
    chartOptions() {
      if (!this.stripedData) return

      const chart = {
        id: `${this.cryptoCurrencyName}${this.nationalCurrencyName}`,
        colors: ['#FF1654', '#247BA0'],
      }

      const plotOptions = {
        bar: {
          horizontal: false,
          columnWidth: '0.1%',
        },
      }

      const xaxis = {
        categories: this.stripedData.map((el) => el.time),
      }

      const yaxis = [
        {
          axisTicks: {
            show: true,
          },
          axisBorder: {
            show: true,
            color: '#008FFB',
          },
          labels: {
            style: {
              colors: '#008FFB',
            },
          },
          title: {
            text: 'Transaction volume',
            style: {
              color: '#008FFB',
            },
          },
          min: 0,
          max: this.bounds.maxVolume,
        },
        {
          seriesName: 'Asks',
          min: this.bounds.min,
          max: this.bounds.max,
          opposite: true,
          axisTicks: {
            show: true,
          },
          axisBorder: {
            show: true,
            color: '#00E396',
          },
          labels: {
            style: {
              colors: '#00E396',
            },
          },
          title: {
            text: 'Asks/Bids',
            style: {
              color: '#00E396',
            },
          },
        },
        {
          seriesName: 'Bids',
          min: this.bounds.min,
          max: this.bounds.max,
          show: false,
        },
        {
          seriesName: 'Avg Asks',
          min: this.bounds.min,
          max: this.bounds.max,
          show: false,
        },
        {
          seriesName: 'Avg Bids',
          min: this.bounds.min,
          max: this.bounds.max,
          show: false,
        },
        {
          seriesName: 'RSI',
          min: 0,
          max: 100,
          opposite: true,
          color: '#421ABC',
          stroke: {
            color: '#421ABC',
          },
          axisTicks: {
            show: true,
          },
          axisBorder: {
            show: true,
            color: '#421ABC',
          },
          labels: {
            style: {
              colors: '#421ABC',
            },
          },
          title: {
            text: 'RSI',
            style: {
              color: '#421ABC',
            },
          },
        },
      ]

      return { chart, plotOptions, xaxis, yaxis }
    },
    defaultSeries() {
      if (!this.stripedData) return []

      return [
        {
          name: 'Transaction volume',
          type: 'column',
          data: this.stripedData.map((el) => el.data.volume),
        },
        {
          name: 'Asks',
          type: 'line',
          data: this.stripedData.map((el) => el.data.ask),
        },
        {
          name: 'Bids',
          type: 'line',
          data: this.stripedData.map((el) => el.data.bid),
        },
      ]
    },
    avgSeries() {
      if (
        this.tickerData.length <= 2 * this.transactionsToCount ||
        this.transactionsToCount > this.tickerData.length
      )
        return []

      const asksHistory = []
      const bidsHistory = []
      const RSIHistory = []

      this.stripedData.forEach((el) => {
        const index = this.tickerData.indexOf(el) - 1
        const { askAvg, bidAvg } = this.countAvgs(index)
        const RSI = this.countRSI(index)

        asksHistory.push(askAvg)
        bidsHistory.push(bidAvg)
        RSIHistory.push(RSI)
      })

      const series = [...this.defaultSeries]

      const lastVolume = series[0].data[series[0].data.length - 1]
      const lastAsk = series[1].data[series[1].data.length - 1]

      this.currentRSI = RSIHistory[RSIHistory.length - 1]
      this.$emit('volume', {
        volume: lastVolume * lastAsk,
        trend: this.RSIUpTrend,
        cryptoCurrencyName: this.cryptoCurrencyName,
        nationalCurrencyName: this.nationalCurrencyName,
      })

      return [
        {
          name: 'Avg Asks',
          type: 'line',
          data: asksHistory,
        },
        {
          name: 'Avg Bids',
          type: 'line',
          data: bidsHistory,
        },
        {
          name: 'RSI',
          type: 'line',
          data: RSIHistory,
          color: '#421ABC',
        },
      ]
    },
    chartSeries() {
      return [...this.defaultSeries, ...this.avgSeries]
    },
  },
}
