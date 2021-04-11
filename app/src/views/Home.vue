<template>
  <div class="home">
    <div class="section">
      <CryptoCurrency
        cryptoCurrencyName="BTC"
        nationalCurrencyName="USD"
        :min="59450"
        :max="59600"
      />
    </div>
    <div class="section">
      <CryptoCurrency
        cryptoCurrencyName="ETH"
        nationalCurrencyName="USD"
        :min="2138"
        :max="2143"
      />
    </div>
    <div class="section">
      <CryptoCurrency
        cryptoCurrencyName="XLM"
        nationalCurrencyName="USD"
        :min="0.579"
        :max="0.6"
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
