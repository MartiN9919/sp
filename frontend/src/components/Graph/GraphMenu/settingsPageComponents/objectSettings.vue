<template>
  <body-block-settings :icon="icon" :title="title" :sub-title="subTitle">
    <slot></slot>
    <v-list-item v-for="classifier in classifiers" @click="setClassifier(classifier.id)" dense v-ripple="{ class: 'teal--text' }">
      <v-list-item-subtitle>{{classifier.title}}</v-list-item-subtitle>
      <v-list-item-action>
        <v-switch disabled color="teal" v-model="classifier.status"></v-switch>
      </v-list-item-action>
    </v-list-item>
  </body-block-settings>
</template>

<script>
import BodyBlockSettings from "./bodyBlockSettings"
import SelectorObject from "../createPageComponents/selectorObject"

export default {
  name: "objectSettings",
  components: {SelectorObject, BodyBlockSettings},
  props: {
    classifiers: Array,
  },
  data: () => ({
    icon: 'mdi-text-box-outline',
    title: 'Настройки объектов',
    subTitle: 'Настройка отображения классификаторов объекта',
  }),
  methods: {
    setClassifier(id) {
      this.$emit('setClassifier', id)
    }
  }
}
</script>

<style scoped>
.v-list-item {
  height: 30px;
  min-height: 30px;
}
</style>