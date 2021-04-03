<template>
  <div></div>
</template>

<script>
import { handleData } from '@/services/FinanceAPI'

export default {
  name: 'CryptoCurrency',
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
      console.log(downloadedData)
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
