<template>
  <div class="float-form--outer">
    <form class="float-form--inner" @submit.prevent="addInstance(instanceForm)">
      <div class="float-form__field">
        <label for="formCrypto">Crypto: </label>
        <select id="formCrypto" v-model="instanceForm.crypto">
          <option v-for="crypto in cryptos" :value="crypto" :key="crypto">
            {{ crypto }}
          </option>
        </select>
      </div>
      <div class="float-form__field">
        <label for="formNational">National: </label>
        <select id="formNational" v-model="instanceForm.national">
          <option
            v-for="national in nationals"
            :value="national"
            :key="national"
          >
            {{ national }}
          </option>
        </select>
      </div>
      <div class="float-form__field">
        <button type="submit">Add!</button>
      </div>
    </form>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import { v4 as uuidv4 } from 'uuid'

export default {
  name: 'CryptoForm',
  data: () => ({
    cryptos: ['BTC', 'ETH', 'XLM'],
    nationals: ['USD', 'EUR'],
    instanceForm: {
      crypto: '',
      national: '',
    },
  }),
  methods: {
    ...mapActions({
      createInstance: 'createInstance',
    }),
    addInstance(form) {
      this.createInstance({ ...form, id: uuidv4() })

      this.instanceForm.crypto = ''
      this.instanceForm.national = ''
    },
  },
}
</script>

<style lang="scss" scoped></style>
