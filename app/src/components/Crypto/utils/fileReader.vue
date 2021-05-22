<template>
  <label class="text-reader">
    <input type="file" @change="loadTextFromFile" />
  </label>
</template>

<script>
export default {
  methods: {
    loadTextFromFile(ev) {
      const file = ev.target.files[0]
      const reader = new FileReader()

      reader.onload = (e) => this.$emit('load', e.target.result)
      reader.readAsText(file)
    },
  },
}
</script>

<style>
input {
  background: #555;
  color: white;
  border: 1px solid #333;
  border-radius: 10%;
  padding: 4px 16px;
}
</style>
