<template>
  <div>
    <CryptoHistory
      v-if="cryptoData && cryptoData.length > 0"
      :cryptoData="cryptoData"
    />
  </div>
</template>

<script>
import { handleData } from '@/services/FinanceAPI'
import CryptoHistory from '@/components/CryptoHistory'

export default {
  name: 'CryptoCurrency',
  components: { CryptoHistory },
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
  methods: {
    async getCryptoData() {
      const downloadedData = await handleData(
        this.cryptoCurrencyName,
        this.nationalCurrencyName
      )
      this.cryptoData.push(downloadedData)
    },
  },
  created() {
    this.dataInterval = setInterval(() => {
      this.getCryptoData()
    }, 5000)
  },
  destroyed() {
    clearInterval(this.dataInterval)
  },
}
</script>

<style scoped></style>
