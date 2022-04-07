<template>
  <object-selector-settings v-model="id">
    <item-classifier-settings
      v-for="classifier in classifiers"
      :key="classifier.id"
      :id="classifier.id"
      :status="classifier.status"
      :title="classifier.title"
    />
  </object-selector-settings>
</template>

<script>
import ObjectSelectorSettings from "@/components/Graph/GraphMenu/Settings/Modules/ObjectSelectorSettings"
import ItemClassifierSettings from "@/components/Graph/GraphMenu/Settings/Classifier/ItemClassifierSettings"
import {mapGetters} from "vuex"

export default {
  name: "ListClassifierSettings",
  components: {ItemClassifierSettings, ObjectSelectorSettings},
  data: () => ({
    id: null
  }),
  computed: {
    ...mapGetters(['baseClassifiers', 'classifiersSettings']),
    classifiers: function () {
      let classifiers = []
      for (let baseClassifier of this.baseClassifiers(this.id))
        classifiers.push(Object.assign({
          status: !this.classifiersSettings.includes(baseClassifier.id)
        }, baseClassifier))
      return classifiers
    }
  }
}
</script>

<style scoped>

</style>