<template>
  <v-textarea
    row-height="1" auto-grow
    autocomplete="off"
    append-icon="mdi-numeric"
    :label="title"
    v-model="value"
    @keypress="isNumber($event)"
    placeholder="Введите необходимое значение"
    hide-details class="pt-0 mt-0" color="teal" type="text"
  ></v-textarea>
</template>

<script>
export default {
  name: "numberInput",
  props: {
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
  methods: {
    isNumber(event) {
      if(!this.value) {
        if (!Number(event.key) && !(event.key === '-'))
          return event.preventDefault()
      } else
        if (!Number(this.value + event.key))
          return event.preventDefault()
    }
  }
}
</script>

<style scoped>

</style>