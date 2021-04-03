<template>
  <div class="home">
    <CryptoCurrency cryptoCurrencyName="BTC" nationalCurrencyName="USD" />
  </div>
</template>

<script>
import CryptoCurrency from '@/components/CryptoCurrency.vue'

export default {
  name: 'Home',
  components: { CryptoCurrency },
}
</script>
