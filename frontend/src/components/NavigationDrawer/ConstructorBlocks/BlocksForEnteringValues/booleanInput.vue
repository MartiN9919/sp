<template>
  <v-text-field
    v-model="variable.value === null ? '' : variable.value ? 'ДА' : 'НЕТ'"
    :label="variable.title"
    placeholder="Выберете необходимое значение"
    hide-details readonly class="pt-0 mt-0" color="teal" type="text"
  >
    <template v-slot:append>
      <v-menu offset-x z-index="10001" left transition="slide-x-reverse-transition">
        <template v-slot:activator="{ on, attrs }">
          <v-icon
            v-bind="attrs" v-on="on"
            :color="attrs['aria-expanded'] === 'true' ? 'teal' : ''"
          >mdi-menu-down-outline</v-icon>
        </template>
        <v-list link>
          <v-list-item v-for="item in [{text: 'ДА', value: true}, {text: 'НЕТ', value: false}]" @click="variable.value = item.value">
            <v-list-item-title>
              {{item.text}}
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </template>
  </v-text-field>
</template>

<script>
export default {
  name: "booleanInput",
  props: {
    variable: Object,
  }
}
</script>

<style scoped>

</style>