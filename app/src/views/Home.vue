<template>
  <div class="home">
    <div v-for="(instance, $index) in instances" :key="$index" class="section">
      <CryptoCurrency
        :cryptoCurrencyName="instance.crypto"
        :nationalCurrencyName="instance.national"
        :fixDiff="instance.fixValue"
        :alert="toBeAlerted === `${instance.crypto}${instance.national}`"
        @volume="handleVolume"
      />
    </div>
    <div class="float-form">
      <CryptoForm />
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import CryptoForm from '@/components/Form/CryptoForm.vue'
import CryptoCurrency from '@/components/Crypto/CryptoCurrency.vue'

export default {
  name: 'Home',
  components: { CryptoCurrency, CryptoForm },
  watch: {
    instancesCount() {
      if (document) {
        document.body.style = `--instances-count: ${this.instancesCount}`
      }
    },
  },
  computed: {
    ...mapGetters({
      instances: 'getInstances',
    }),
    instancesCount() {
      return this.instances.length
    },
  },
  data: () => ({
    instancesData: {},
    toBeAlerted: '',
  }),
  methods: {
    handleVolume(e) {
      this.instancesData[`${e.cryptoCurrencyName}${e.nationalCurrencyName}`] = {
        name: `${e.cryptoCurrencyName}${e.nationalCurrencyName}`,
        volume: e.volume,
        trend: e.trend,
      }

      this.runAlert()
    },
    runAlert() {
      const candidates = []
      for (let instance in this.instancesData) {
        if (!this.instancesData[instance].trend)
          candidates.push(this.instancesData[instance])
      }

      if (candidates.length === 0) this.toBeAlerted = ''
      else if (candidates.length === 1) this.toBeAlerted = candidates[0].name
      else
        this.toBeAlerted = candidates.sort(
          (a, b) => b.volume - a.volume
        )[0].name
    },
  },
}
</script>

<style lang="scss">
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

.float-form {
  position: fixed;
  right: 0;
  top: 0;
  background: #444;
  margin: 2rem 2rem 2rem 2rem;
  padding: 2rem 2rem 2rem 2rem;
  color: #fff;
  border-radius: 0.5rem;
  text-align: center;

  &--inner {
    display: flex;
    flex-direction: column;
  }

  &__field {
    margin-bottom: 6px;
    text-align: center;

    select,
    input {
      background: #555;
      color: white;
      border: 1px solid #333;
      border-radius: 10%;
      padding: 2px 4px;
    }

    input {
      width: 50px;
    }

    button {
      background: #555;
      color: white;
      border: 1px solid #333;
      border-radius: 10%;
      padding: 4px 16px;
    }
  }
}
</style>
