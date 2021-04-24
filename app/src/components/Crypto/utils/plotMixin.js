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
          min: this.bounds.min - this.fixDiff,
          max: this.bounds.max + this.fixDiff,
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
          min: this.bounds.min - this.fixDiff,
          max: this.bounds.max + this.fixDiff,
          show: false,
        },
        {
          seriesName: 'Avg Asks',
          min: this.bounds.min - this.fixDiff,
          max: this.bounds.max + this.fixDiff,
          show: false,
        },
        {
          seriesName: 'Avg Bids',
          min: this.bounds.min - this.fixDiff,
          max: this.bounds.max + this.fixDiff,
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
    chartSeries() {
      if (!this.stripedData) return

      const series = [
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

      if (
        this.cryptoData.length <= 2 * this.transactionsToCount ||
        this.transactionsToCount > this.cryptoData.length
      )
        return series

      const asksHistory = []
      const bidsHistory = []
      const RSIHistory = []

      this.stripedData.forEach((el) => {
        const index = this.cryptoData.indexOf(el) - 1
        const { askAvg, bidAvg } = this.countAvgs(index)
        const RSI = this.countRSI(index)

        asksHistory.push(askAvg)
        bidsHistory.push(bidAvg)
        RSIHistory.push(RSI)
      })

      const avgSeries = [
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

      this.currentRSI = RSIHistory[RSIHistory.length - 1]
      this.$emit('volume', {
        volume: series[0].data[series[0].data.length - 1],
        trend: this.RSITrend,
        cryptoCurrencyName: this.cryptoCurrencyName,
        nationalCurrencyName: this.nationalCurrencyName,
      })

      return [...series, ...avgSeries]
    },
  },
}
