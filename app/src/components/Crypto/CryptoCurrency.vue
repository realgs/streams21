<template>
  <div class="crypto-currency" :class="{ glow: alert }">
    <div class="crypto-currency--header">
      <div v-if="tickerData && tickerData.length > 0">
        <label for="transactionsToShow">Transactions to show: </label>
        <input
          type="number"
          id="transactionsToShow"
          v-model.number="transactionsToShow"
        />
      </div>
      <div v-if="tickerData && tickerData.length > 0">
        <label for="minSpread">min spread %: </label>
        <input type="number" id="minSpread" v-model.number="minSpread" />
      </div>
      <h2>{{ cryptoCurrencyName }} -> {{ nationalCurrencyName }}</h2>
      <div v-if="tickerData && tickerData.length > 0">
        <label for="diffAskBid">Ask/Bid lower than %: </label>
        <input type="number" id="diffAskBid" v-model.number="maxDiffAskBid" />
      </div>
      <div v-if="tickerData && tickerData.length > 0">
        <label for="transactionsToCount">Transactions to count: </label>
        <input
          type="number"
          id="transactionsToCount"
          v-model.number="transactionsToCount"
        />
      </div>
    </div>
    <template v-if="tickerData && tickerData.length > 0">
      <div class="crypto-currency__chart">
        <Apexchart
          width="1500"
          height="600"
          type="line"
          :options="chartOptions"
          :series="chartSeries"
        />
      </div>
      <div class="crypto-currency__status">
        <h2>RSI Status: {{ RSIStatus }}</h2>
        <h2 v-if="spread > minSpread">Volatile Asset</h2>
        <h2 v-if="diffAskBid < maxDiffAskBid">Liquid Asset</h2>
      </div>
      <CryptoHistory
        :cryptoData="tickerData"
        :sign="signs[nationalCurrencyName]"
      />
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
    alert: [Boolean],
  },
  data: () => ({
    tickerData: [],
    dataInterval: null,
    transactionsToCount: 5,
    transactionsToShow: 5,
    signs: {
      USD: '$',
      EUR: '€',
    },
    minSpread: 1,
    maxDiffAskBid: 1,
  }),
  computed: {
    stripedData() {
      if (!this.tickerData) return

      const copiedTickerData = [...this.tickerData]

      return copiedTickerData.length >= this.transactionsToShow
        ? copiedTickerData.slice(1).slice(-this.transactionsToShow)
        : copiedTickerData
    },
    enoughtData() {
      return 2 * this.transactionsToCount < this.tickerData.length
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
    RSIStatus() {
      if (!this.currentRSI && !this.enoughtData) return 'not enough data'

      const status = (val) => {
        if (val === 100)
          return 'The probability of a reversal to a downward trend'
        else if (val >= 70) return 'Sell signal'
        else if (val <= 30 && val > 0) return 'Buy signal'
        else if (val === 0)
          return 'The probability of a trend reversal to an upward trend'
        else return val
      }

      return status(parseInt(this.currentRSI))
    },
    RSIUpTrend() {
      return this.currentRSI && this.enoughtData ? this.currentRSI >= 30 : false
    },
    spread() {
      if (
        !this.tickerData ||
        this.tickerData.length <= this.transactionsToCount
      )
        return 0

      const asksHistory = this.tickerData
        .slice(1)
        .slice(-this.transactionsToCount)
        .map((el) => el.data.ask)
      const bidsHistory = this.tickerData
        .slice(1)
        .slice(-this.transactionsToCount)
        .map((el) => el.data.bid)

      const spreadHistory = []
      for (let i = 0; i < asksHistory.length - 1; i++) {
        const current = (asksHistory[i] + bidsHistory[i]) / 2
        const next = (asksHistory[i + 1] + bidsHistory[i + 1]) / 2

        spreadHistory.push((Math.abs(current - next) / current) * 100)
      }

      return Math.max(...spreadHistory)
    },
    diffAskBid() {
      if (!this.tickerData) return 100

      return this.tickerData[this.tickerData.length - 1].data.difference
    },
  },
  methods: {
    async getData() {
      const [tickerData, transactionData] = await handleData(
        this.cryptoCurrencyName,
        this.nationalCurrencyName
      )
      const time = new Date()
      this.tickerData.push({
        time: time.toLocaleString(),
        data: { ...tickerData, ...transactionData },
      })
    },
    countAvgs(startIndex) {
      const asksHistory = this.tickerData
        .slice(startIndex - this.transactionsToCount, startIndex)
        .map((el) => el.data.ask)
      const bidsHistory = this.tickerData
        .slice(startIndex - this.transactionsToCount, startIndex)
        .map((el) => el.data.bid)

      const askAvg =
        asksHistory.reduce((a, b) => a + b, 0) / this.transactionsToCount
      const bidAvg =
        bidsHistory.reduce((a, b) => a + b, 0) / this.transactionsToCount

      return { askAvg, bidAvg }
    },
    countRSI(startIndex) {
      const closeHistory = this.tickerData
        .slice(startIndex - this.transactionsToCount - 1, startIndex)
        .map((el) => el.data.close)

      const increase = []
      const decrease = []

      for (let i = 0; i < closeHistory.length - 1; i++) {
        const calc = closeHistory[i] - closeHistory[i + 1]

        if (calc >= 0) {
          increase.push(calc)
          decrease.push(0)
        } else if (calc < 0) {
          decrease.push(calc * -1)
          increase.push(0)
        }
      }

      const avgIncrease =
        increase.reduce((a, b) => a + b, 0) /
        (increase.length ? increase.length : 1)

      const avgDecrease =
        decrease.reduce((a, b) => a + b, 0) /
        (decrease.length ? decrease.length : 1)

      const RS = avgIncrease / avgDecrease

      const RSI = 100 - 100 / (1 + RS)

      return isNaN(RSI) ? 0 : RSI
    },
  },
  created() {
    this.dataInterval = setInterval(async () => {
      await this.getData()
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

  &__status {
    width: 100%;
    text-align: center;
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

.glow {
  -webkit-animation: glow 1s ease-in-out infinite alternate;
  -moz-animation: glow 1s ease-in-out infinite alternate;
  animation: glow 1s ease-in-out infinite alternate;
}

@keyframes glow {
  from {
    box-shadow: 0 0 10px rgb(255, 0, 0), 0 0 20px #fff, 0 0 30px #e60000,
      0 0 40px #e60013, 0 0 50px #e60013, 0 0 60px #e60073, 0 0 70px #e60073;
  }
  to {
    box-shadow: 0 0 20px rgb(255, 0, 0), 0 0 30px #ff4da6, 0 0 40px #ff4da6,
      0 0 50px #ff4d5c, 0 0 60px #ff4d6b, 0 0 70px #ff4d4d, 0 0 80px #ff4d5c;
  }
}
</style>
