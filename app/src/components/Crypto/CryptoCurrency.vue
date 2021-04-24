<template>
  <div class="crypto-currency">
    <div class="crypto-currency--header">
      <div v-if="cryptoData && cryptoData.length > 0">
        <label for="transactionsToShow">Transactions to show: </label>
        <input
          type="number"
          id="transactionsToShow"
          v-model="transactionsToShow"
        />
      </div>
      <h2>{{ cryptoCurrencyName }} -> {{ nationalCurrencyName }}</h2>
      <div v-if="cryptoData && cryptoData.length > 0">
        <label for="transactionsToCount">Transactions to count: </label>
        <input
          type="number"
          id="transactionsToCount"
          v-model="transactionsToCount"
        />
      </div>
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
import plotMixin from '@/components/Crypto/utils/plotMixin'
import CryptoHistory from '@/components/Crypto/CryptoHistory'

const findMinAsk = (p, v) => (p.data.ask < v.data.ask ? p : v)
const findMaxAsk = (p, v) => (p.data.ask > v.data.ask ? p : v)
const findMinBid = (p, v) => (p.data.bid < v.data.bid ? p : v)
const findMaxBid = (p, v) => (p.data.bid > v.data.bid ? p : v)
const findMaxVolume = (p, v) => (p.data.volume > v.data.volume ? p : v)

export default {
  name: 'CryptoCurrency',
  mixins: [plotMixin],
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
    transactionsToCount: 5,
    transactionsToShow: 5,
  }),
  computed: {
    stripedData() {
      if (!this.cryptoData) return
      const copiedData = [...this.cryptoData]

      return copiedData.length >= this.transactionsToShow
        ? copiedData.slice(1).slice(-this.transactionsToShow)
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
      const asksHistory = this.cryptoData
        .slice(startIndex - this.transactionsToCount, startIndex)
        .map((el) => el.data.ask)
      const bidsHistory = this.cryptoData
        .slice(startIndex - this.transactionsToCount, startIndex)
        .map((el) => el.data.bid)

      const askAvg =
        asksHistory.reduce((a, b) => a + b, 0) / this.transactionsToCount
      const bidAvg =
        bidsHistory.reduce((a, b) => a + b, 0) / this.transactionsToCount

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
    display: flex;
    justify-content: space-between;

    input {
      background: #555;
      color: white;
      border: 1px solid #333;
      border-radius: 10%;
      padding: 2px 4px;
      width: 50px;
    }
  }
}
</style>
