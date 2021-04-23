<template>
  <div class="crypto-currency">
    <div class="crypto-currency--header">
      <h2>{{ cryptoCurrencyName }} -> {{ nationalCurrencyName }}</h2>
    </div>
    <template v-if="cryptoData && cryptoData.length > 0">
      <div class="crypto-currency__chart">
        <Apexchart
          width="1500"
          height="600"
          type="line"
          :options="chartOptions"
          :series="chartSeries"
        />
      </div>
      <CryptoHistory :cryptoData="cryptoData" />
    </template>
    <template v-else>
      <h2>No data, please wait.</h2>
    </template>
  </div>
</template>

<script>
import { handleData } from '@/services/FinanceAPI'
import CryptoHistory from '@/components/CryptoHistory'

const findMinAsk = (p, v) => (p.data.ask < v.data.ask ? p : v)
const findMaxAsk = (p, v) => (p.data.ask > v.data.ask ? p : v)
const findMinBid = (p, v) => (p.data.bid < v.data.bid ? p : v)
const findMaxBid = (p, v) => (p.data.bid > v.data.bid ? p : v)
const findMaxVolume = (p, v) => (p.data.volume > v.data.volume ? p : v)

export default {
  name: 'CryptoCurrency',
  components: {
    CryptoHistory,
  },
  props: {
    cryptoCurrencyName: {
      type: String,
      required: true,
    },
    nationalCurrencyName: {
      type: String,
      required: true,
    },
    fixDiff: {
      type: Number,
    },
  },
  data: () => ({
    cryptoData: [],
    dataInterval: null,
    transactionsCount: 5,
  }),
  computed: {
    stripedData() {
      if (!this.cryptoData) return
      const copiedData = [...this.cryptoData]

      return copiedData.length >= this.transactionsCount
        ? copiedData.slice(1).slice(-this.transactionsCount)
        : copiedData
    },
    bounds() {
      if (!this.stripedData) return
      const minAsk = this.stripedData.reduce(findMinAsk).data.ask
      const maxAsk = this.stripedData.reduce(findMaxAsk).data.ask
      const minBid = this.stripedData.reduce(findMinBid).data.bid
      const maxBid = this.stripedData.reduce(findMaxBid).data.bid
      const maxVolume = 15 * this.stripedData.reduce(findMaxVolume).data.volume

      return {
        min: minAsk < minBid ? minAsk : minBid,
        max: maxAsk > maxBid ? maxAsk : maxBid,
        maxVolume,
      }
    },
    chartOptions() {
      if (!this.stripedData) return

      const chart = {
        id: `${this.cryptoCurrencyName}${this.nationalCurrencyName}`,
      }

      const plotOptions = {
        bar: {
          horizontal: false,
          columnWidth: '0.5%',
          endingShape: 'rounded',
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

      if (this.cryptoData.length <= 2 * this.transactionsCount) return series

      const asksHistory = []
      const bidsHistory = []

      this.stripedData.forEach((el) => {
        const index = this.cryptoData.indexOf(el) - 1
        const { askAvg, bidAvg } = this.countAvgs(index)

        asksHistory.push(askAvg)
        bidsHistory.push(bidAvg)
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
      ]

      return [...series, ...avgSeries]
    },
  },
  methods: {
    async getCryptoData() {
      const downloadedData = await handleData(
        this.cryptoCurrencyName,
        this.nationalCurrencyName
      )
      const time = new Date()
      this.cryptoData.push({
        time: time.toLocaleString(),
        data: downloadedData,
      })
    },
    countAvgs(startIndex) {
      const asksHistory = []
      const bidsHistory = []

      // for (
      //   let i = startIndex;
      //   i > this.cryptoData.length - this.transactionsCount;
      //   i--
      // ) {
      // asksHistory.push(this.cryptoData[i].data.ask)
      // bidsHistory.push(this.cryptoData[i].data.bid)
      // }

      let i = startIndex
      while (i !== startIndex - this.transactionsCount) {
        asksHistory.push(this.cryptoData[i].data.ask)
        bidsHistory.push(this.cryptoData[i].data.bid)
        i--
      }

      const askAvg =
        asksHistory.reduce((a, b) => a + b, 0) / this.transactionsCount
      const bidAvg =
        bidsHistory.reduce((a, b) => a + b, 0) / this.transactionsCount

      return { askAvg, bidAvg }
    },
  },
  created() {
    this.dataInterval = setInterval(async () => {
      await this.getCryptoData()
    }, 5000)
  },
  destroyed() {
    clearInterval(this.dataInterval)
  },
}
</script>

<style lang="scss" scoped>
.crypto-currency {
  position: relative;
  display: flex;
  flex-direction: column;
  background: #444;
  margin: 2rem 2rem 2rem 2rem;
  padding: 2rem 2rem 2rem 2rem;
  color: #fff;
  border-radius: 0.5rem;

  &__chart {
    background: #fff;
    color: black;
    margin-bottom: 1rem;
  }

  &--header {
    text-align: center;
    margin-bottom: 1rem;
  }
}
</style>
