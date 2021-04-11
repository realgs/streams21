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
  }),
  computed: {
    stripedData() {
      if (!this.cryptoData) return
      const copiedData = [...this.cryptoData]

      return copiedData.length >= 10
        ? copiedData.slice(1).slice(-10)
        : copiedData
    },
    bounds() {
      if (!this.stripedData) return
      const minAsk = this.stripedData.reduce(findMinAsk).data.ask
      const maxAsk = this.stripedData.reduce(findMaxAsk).data.ask
      const minBid = this.stripedData.reduce(findMinBid).data.bid
      const maxBid = this.stripedData.reduce(findMaxBid).data.bid

      return {
        min: minAsk < minBid ? minAsk : minBid,
        max: maxAsk > maxBid ? maxAsk : maxBid,
      }
    },
    chartOptions() {
      if (!this.stripedData) return

      const chart = {
        id: `${this.cryptoCurrencyName}${this.nationalCurrencyName}`,
      }

      const xaxis = {
        categories: this.stripedData.map((el) => el.time),
      }

      const yaxis = {
        min: this.bounds.min - this.fixDiff,
        max: this.bounds.max + this.fixDiff,
      }

      return { chart, xaxis, yaxis }
    },
    chartSeries() {
      if (!this.stripedData) return

      const series = [
        {
          name: 'Asks',
          data: this.stripedData.map((el) => el.data.ask),
        },
        {
          name: 'Bids',
          data: this.stripedData.map((el) => el.data.bid),
        },
      ]

      return series
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
