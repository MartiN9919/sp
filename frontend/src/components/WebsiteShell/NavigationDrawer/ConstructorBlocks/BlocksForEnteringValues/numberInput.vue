<template>
  <v-text-field
    autocomplete="off"
    append-icon="mdi-numeric"
    :label="variable.title"
    v-model="variable.value"
    @keypress="isNumber($event)"
    placeholder="Введите необходимое значение"
    hide-details class="pt-0 mt-0" color="teal" type="text"
  ></v-text-field>
</template>

<script>
export default {
  name: "numberInput",
  props: {
    variable: Object,
  },
  methods: {
    isNumber(event) {
      if(!this.variable.value) {
        if (!Number(event.key) && !(event.key === '-'))
          return event.preventDefault()
      } else
        if (!Number(this.variable.value + event.key))
          return event.preventDefault()
    }
  }
}
</script>

<style scoped>

</style>