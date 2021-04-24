<template>
  <div class="crypto-history">
    <div class="crypto-history__table">
      <div class="crypto-history__header">
        <div class="crypto-history__header--row">
          <div class="crypto-history__header--cell">Ask</div>
          <div class="crypto-history__header--cell">Bid</div>
          <div class="crypto-history__header--cell">Difference</div>
          <div class="crypto-history__header--cell">Volume</div>
        </div>
      </div>
      <div class="crypto-history__body">
        <div class="crypto-history__body--wrapper">
          <div
            class="crypto-history__body--row"
            v-for="(row, $index) in reverseData"
            :key="$index"
          >
            <div class="crypto-history__body--cell">{{ row.data.ask }} $</div>
            <div class="crypto-history__body--cell">{{ row.data.bid }} $</div>
            <div class="crypto-history__body--cell">
              {{ row.data.difference }} %
            </div>
            <div class="crypto-history__body--cell">{{ row.data.volume }}</div>
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
  computed: {
    reverseData() {
      const copiedData = [...this.cryptoData]

      return copiedData.reverse()
    },
  },
}
</script>

<style lang="scss" scoped>
.crypto-history {
  --width: 100rem;
  &__table {
    display: flex;
    flex-direction: column;
  }

  &__header,
  &__body {
    width: var(--width);
    &--row {
      display: flex;
      flex-direction: row;
      width: var(--width);
    }

    &--cell {
      width: calc(var(--width) / 4);
    }
  }

  &__body {
    &--wrapper {
      overflow-y: auto;
      overflow-x: hidden;
      height: 90px;
      max-height: 90px;
    }
  }
}
</style>
