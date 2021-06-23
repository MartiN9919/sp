<template>
  <v-text-field
    autocomplete="off"
    append-icon="mdi-format-color-text"
    v-model="variable.value"
    :label="variable.title"
    placeholder="Введите необходимое значение"
    hide-details class="pt-0 mt-0 leaflet-grab" color="teal" type="text"
  ></v-text-field>
</template>

<script>
export default {
  name: "textInput",
  props: {
    variable: Object,
  },
}
</script>

<style scoped>

</style>