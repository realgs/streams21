<template>
  <div class="crypto-currency">
    <LineChart v-if="parsedCryptoData" :chartData="parsedCryptoData" />
    <CryptoHistory
      v-if="cryptoData && cryptoData.length > 0"
      :cryptoData="cryptoData"
    />
  </div>
</template>

<script>
import LineChart from '@/utils/LineChart'
import { handleData } from '@/services/FinanceAPI'
import CryptoHistory from '@/components/CryptoHistory'

export default {
  name: 'CryptoCurrency',
  components: { CryptoHistory, LineChart },
  props: {
    cryptoCurrencyName: {
      type: String,
      required: true,
    },
    nationalCurrencyName: {
      type: String,
      required: true,
    },
  },
  data: () => ({
    cryptoData: [],
    dataInterval: null,
  }),
  computed: {
    parsedCryptoData() {
      if (!this.cryptoData) return
      const copiedData = [...this.cryptoData]

      const labels = []

      const asks = {
        label: 'Asks',
        borderColor: 'rgb(0, 103, 255)',
        backgroundColor: 'rgba(0, 103, 255, 0.5)',
        fill: false,
        data: [],
      }
      const bids = {
        label: 'Bids',
        borderColor: 'rgb(39, 255, 0)',
        backgroundColor: 'rgba(39, 255, 0, 0.5)',
        fill: false,
        data: [],
      }

      for (const data of copiedData) {
        labels.push(data.time)
        asks.data.push(data.data.ask)
        bids.data.push(data.data.bid)
      }

      return { labels, datasets: [asks, bids] }
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
  display: flex;
  flex-direction: column;
}
</style>
