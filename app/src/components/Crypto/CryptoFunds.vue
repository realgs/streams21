<template>
  <div class="crypto-fund">
    <div class="crypto-fund--wrapper crypto-fund--data">
      <div class="crypto-fund--form">
        <h3>Buy</h3>
        <form class="crypto-fund--form" @submit.prevent="buyUnits(form)">
          <div class="crypto-fund__field">
            <label for="formUnits">Units: </label>
            <input type="number" id="formUnits" v-model.number="form.units" />
          </div>
          <div class="crypto-fund__field">
            <label for="formValue">Value: </label>
            <input
              type="number"
              id="formValue"
              v-model.number="form.buyPrice"
            />
          </div>
          <button type="submit">Add</button>
        </form>
      </div>
      <div class="crypto-fund--bought">
        <h3>Bought</h3>
        <template v-if="buyData && buyData.length">
          <div
            v-for="row in buyData"
            :key="row.id"
            class="crypto-fund--unit"
            @dblclick="sellUnits(row.id)"
          >
            Units: {{ row.units }}, purchase value: {{ row.buyPrice }}
          </div>
        </template>
      </div>
      <div class="crypto-fund--sold">
        <h3>Sold</h3>
        <template v-if="sellData && sellData.length">
          <div v-for="row in sellData" :key="row.id" class="crypto-fund--unit">
            Units: {{ row.units }}, purchase value: {{ row.buyPrice }}, sell
            value: {{ row.sellPrice }}, earnings: {{ row.earnings || 0 }}
          </div>
        </template>
      </div>
    </div>
    <div class="crypto-fund--wrapper">
      <div>Avg purchase price: {{ avgPurchasePrice || 0 }}</div>
      <button @click.prevent="saveData">Download data</button>
      <FileReader @load="loadData" />
      <div>Total earnings: {{ totalEarnings || 0 }}</div>
    </div>
  </div>
</template>

<script>
import { v4 as uuidv4 } from 'uuid'
import FileReader from '@/components/Crypto/utils/fileReader'

export default {
  name: 'CryptoFunds',
  components: {
    FileReader,
  },
  props: {
    name: [String],
  },
  watch: {
    avgPurchasePrice(val) {
      this.$emit('avgPurchasePrice', val)
    },
  },
  data: () => ({
    form: {
      units: 0,
      buyPrice: 0,
    },
    buyData: [],
    sellData: [],
  }),
  computed: {
    avgPurchasePrice() {
      if (!this.buyData) return 0

      return (
        this.buyData.reduce((a, b) => a + b.buyPrice, 0) / this.buyData.length
      )
    },
    totalEarnings() {
      if (!this.sellData) return 0

      return this.sellData.reduce((a, b) => a + b.earnings, 0)
    },
  },
  methods: {
    buyUnits(form) {
      this.buyData.push({ ...form, id: uuidv4() })

      this.form.units = 0
      this.form.buyPrice = 0
    },
    sellUnits(id) {
      const sellPrice = prompt('Sell price')
      if (sellPrice === null || sellPrice === '') return

      const buyData = this.buyData.find((el) => el.id === id)
      const earnings = (sellPrice ? +sellPrice : 0) - buyData.buyPrice

      this.sellData.push({ ...buyData, sellPrice, earnings })
      this.buyData = this.buyData.filter((el) => el.id !== id)
    },
    saveData() {
      const { buyData, sellData } = this

      const data = JSON.stringify({ buyData, sellData })
      const blob = new Blob([data], { type: 'text/plain' })
      const e = document.createEvent('MouseEvents')
      const a = document.createElement('a')
      a.download = `${this.name}.json`
      a.href = window.URL.createObjectURL(blob)
      a.dataset.downloadurl = ['text/json', a.download, a.href].join(':')
      e.initEvent(
        'click',
        true,
        false,
        window,
        0,
        0,
        0,
        0,
        0,
        false,
        false,
        false,
        false,
        0,
        null
      )
      a.dispatchEvent(e)
    },
    loadData(e) {
      const { buyData, sellData } = JSON.parse(e)

      this.buyData = buyData
      this.sellData = sellData
    },
  },
}
</script>

<style lang="scss" scoped>
.crypto-fund {
  display: flex;
  flex-direction: column;
  margin-top: 16px;

  &--data {
    height: 200px;
    max-height: 200px;
    overflow-y: auto;
  }

  &--wrapper {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }

  &--form {
    text-align: center;
  }

  &__field {
    input {
      background: #555;
      color: white;
      border: 1px solid #333;
      border-radius: 10%;
      padding: 2px 4px;
      width: 50px;
    }
  }

  button {
    background: #555;
    color: white;
    border: 1px solid #333;
    border-radius: 10%;
    padding: 4px 16px;
  }
}
</style>
