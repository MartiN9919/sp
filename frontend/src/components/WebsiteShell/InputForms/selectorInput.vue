<template>
  <v-select
    :items="list" autocomplete="off" :label="title" attach v-model="value" :rules="rules"
    :menu-props="{ offsetY: true, maxWidth: '100%', minWidth: '100%' }"
    append-icon="mdi-format-list-bulleted" placeholder="Выберете необходимое значение"
    hide-details class="pt-0 mt-0 leaflet-grab" color="teal" type="text" item-color="teal"
  >
    <template v-slot:item="{ item }">
      <div class="py-1">{{item}}</div>
    </template>
  </v-select>
</template>

<script>
  export default {
    name: "selectorInput",
    props: {
      rules: Array,
      title: String,
      list: Array,
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
