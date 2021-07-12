<template>
  <v-textarea
    row-height="1" auto-grow
    autocomplete="off"
    append-icon="mdi-format-color-text"
    v-model="value"
    :label="title"
    :rules="rules"
    placeholder="Введите необходимое значение"
    hide-details class="pt-0 mt-0" color="teal" type="text"
  ></v-textarea>
</template>

<script>
export default {
  name: "textInput",
  props: {
    rules: Array,
    title: String,
    inputString: String,
  },
  model: { prop: 'inputString', event: 'changeInputString', },
  computed: {
    value: {
      get: function () { return this.inputString },
      set: function (value) { this.$emit('changeInputString', value) }
    }
  },
}
</script>

<style scoped>

</style>