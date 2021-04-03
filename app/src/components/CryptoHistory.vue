<template>
  <div class="crypto-history">
    <div class="crypto-history__table">
      <div class="crypto-history__header">
        <div class="crypto-history__header--row">
          <div class="crypto-history__header--cell">Ask</div>
          <div class="crypto-history__header--cell">Bid</div>
          <div class="crypto-history__header--cell">Difference</div>
        </div>
      </div>
      <div class="crypto-history__body">
        <div class="crypto-history__body--wrapper">
          <div
            class="crypto-history__body--row"
            v-for="(row, $index) in cryptoData"
            :key="$index"
          >
            <div class="crypto-history__body--cell">{{ row.ask }} $</div>
            <div class="crypto-history__body--cell">{{ row.bid }} $</div>
            <div class="crypto-history__body--cell">{{ row.difference }} %</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CryptoHistory',
  props: {
    cryptoData: {
      type: Array,
      required: true,
    },
  },
}
</script>

<style lang="scss" scoped>
.crypto-history {
  &__table {
    display: flex;
    flex-direction: column;
  }

  &__header,
  &__body {
    &--row {
      display: flex;
      flex-direction: row;
    }

    &--cell {
      width: 90px;
    }
  }

  &__body {
    &--wrapper {
      overflow-y: auto;
      max-height: 90px;
    }
  }
}
</style>
