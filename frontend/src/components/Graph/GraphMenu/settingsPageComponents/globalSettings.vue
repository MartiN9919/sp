<template>
  <body-block-settings :icon="icon" :title="title" :sub-title="subTitle">
    <v-list-item
        v-for="(value, key) in settings" :key="key"
        @click="$emit('changeSettings', {id: key, value: !value.state})"
        v-ripple="{ class: 'teal--text' }"
    >
      <v-list-item-content>
        <v-list-item-title>{{ value.title }}</v-list-item-title>
        <v-list-item-subtitle v-if="value.subTitle">{{ value.subTitle }}</v-list-item-subtitle>
      </v-list-item-content>
      <v-list-item-action>
        <v-switch disabled v-model="value.state" color="teal"></v-switch>
      </v-list-item-action>
    </v-list-item>
  </body-block-settings>
</template>

<script>
import BodyBlockSettings from "./bodyBlockSettings"

export default {
  name: "globalSettings",
  components: {BodyBlockSettings},
  props: {
    settings: Object,
  },
  data: () => ({
    icon: 'mdi-graph-outline',
    title: 'Общие настройки графа',
    subTitle: 'Настройка отображения связей и объектов на графе',
  })
}
</script>

<style scoped>

</style>