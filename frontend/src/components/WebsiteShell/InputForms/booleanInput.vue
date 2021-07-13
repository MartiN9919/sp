<template>
  <v-menu
    :close-on-content-click="false" ref="menuBoolean" transition="slide-x-reverse-transition"
    offset-x offset-y bottom right fixed z-index="10001" min-width="auto" nudge-left="64"
  >
    <template v-slot:activator="{ on }">
      <v-textarea
        v-model="value" v-on="on" :rules="rules" :label="title"
        autocomplete="off" append-icon="mdi-order-bool-descending-variant" row-height="1" auto-grow
        hide-details readonly class="pt-0 mt-0" color="teal" type="text" placeholder="Выберете необходимое значение"
      ></v-textarea>
    </template>
      <v-list link>
        <v-list-item
          v-for="item in [{text: 'ДА', value: true}, {text: 'НЕТ', value: false}]"
          @click="value = item.value; $refs.menuBoolean.save()" :key="item.value"
        ><v-list-item-title>{{item.text}}</v-list-item-title></v-list-item>
      </v-list>
  </v-menu>
</template>

<script>
export default {
  name: "booleanInput",
  props: {
    rules: Array,
    title: String,
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