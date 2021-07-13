<template>
  <v-autocomplete
    :items="list" autocomplete="off" :label="title" v-model="value" :rules="rules"
    :menu-props="{ offsetY: true, maxWidth: '100%', minWidth: '100%' }" attach
    append-icon="mdi-format-list-bulleted" placeholder="Выберете необходимое значение"
    hide-details class="pt-0 mt-0" color="teal" type="text" item-color="teal"
  >
    <template v-slot:item="{ item }">
      <div class="py-1">{{item}}</div>
    </template>
  </v-autocomplete>
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
