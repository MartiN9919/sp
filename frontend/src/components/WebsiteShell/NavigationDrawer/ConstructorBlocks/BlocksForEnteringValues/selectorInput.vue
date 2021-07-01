<template>
  <v-menu
    :close-on-content-click="false"
    offset-y z-index="10001" bottom right
    min-width="auto" fixed
    transition="slide-x-reverse-transition"
  >
    <template v-slot:activator="{ on }">
      <v-text-field
        slot="activator"
        autocomplete="off"
        append-icon="mdi-order-bool-descending-variant"
        v-model="value"
        :label="title"
        placeholder="Выберете необходимое значение"
        hide-details readonly class="pt-0 mt-0" color="teal" type="text"
        v-on="on"
      ></v-text-field>
    </template>
    <v-list link>
      <v-list-item v-for="item in list" :key="item" @click="value = item">
        <v-list-item-title>{{item}}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>
  export default {
    name: "selectorInput",
    props: {
      title: String,
      list: Array,
      inputString: Boolean,
    },
    model: { prop: 'inputString', event: 'changeInputString', },
    computed: {
      value: {
        get: function () { return this.inputString === null ? '' : this.inputString ? 'ДА' : 'НЕТ' },
        set: function (value) { this.$emit('changeInputString', value) }
      }
    },
  }
</script>

<style scoped>

</style>
