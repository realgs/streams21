<template>
  <div class="home">
    <CryptoCurrency cryptoCurrencyName="BTC" nationalCurrencyName="USD" />
    <CryptoCurrency cryptoCurrencyName="ETH" nationalCurrencyName="USD" />
    <CryptoCurrency cryptoCurrencyName="XLM" nationalCurrencyName="USD" />
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
</style>
