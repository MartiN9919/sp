<template>
  <v-menu
    :close-on-content-click="false"
    offset-x offset-y z-index="10001" bottom right
    nudge-left="64" min-width="auto" fixed
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
    <v-card>
      <v-list link>
        <v-list-item
          v-for="item in [{text: 'ДА', value: true}, {text: 'НЕТ', value: false}]"
          @click="value = item.value"
          :key="item.value"
        >
          <v-list-item-title>
            {{item.text}}
          </v-list-item-title>
        </v-list-item>
      </v-list>
    </v-card>
  </v-menu>
</template>

<script>
export default {
  name: "booleanInput",
  props: {
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