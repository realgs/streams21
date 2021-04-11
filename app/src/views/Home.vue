<template>
  <div class="home">
    <div class="section">
      <CryptoCurrency
        cryptoCurrencyName="BTC"
        nationalCurrencyName="USD"
        :fixDiff="10"
      />
    </div>
    <div class="section">
      <CryptoCurrency
        cryptoCurrencyName="ETH"
        nationalCurrencyName="USD"
        :fixDiff="1"
      />
    </div>
    <div class="section">
      <CryptoCurrency
        cryptoCurrencyName="XLM"
        nationalCurrencyName="USD"
        :fixDiff="0.001"
      />
    </div>
  </div>
</template>

<script>
import CryptoCurrency from '@/components/CryptoCurrency.vue'

export default {
  name: 'Home',
  components: { CryptoCurrency },
}
</script>

<style lang="scss" scoped>
.home {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.section {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
