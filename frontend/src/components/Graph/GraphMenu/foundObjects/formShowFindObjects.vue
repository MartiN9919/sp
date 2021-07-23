<template>
  <div>
    <v-tooltip
      v-for="param in object.params" :key="param.id" bottom
      open-delay="1000" nudge-bottom="-15" transition="false" color="#00796B" z-index="10001" max-width="20%"
    >
      <template v-slot:activator="{ on }">
        <div v-on="on">
          <found-object-param
              :param="param" :label="getClassifier(object.object_id, param.id).title"
          ></found-object-param>
        </div>
      </template>
      <p class="text-formatter-for-window-size additional-text text-justify ma-0">
        {{ getClassifierHint(object.object_id, param.id) }}
      </p>
    </v-tooltip>
  </div>
</template>

<script>
import FoundObjectParam from "./foundObjectParam";
export default {
  name: "formShowFindObjects",
  components: {FoundObjectParam},
  props: {
    object: Object,
  },
  methods: {
    getClassifier(objectId, classifierId) {
      let classifiers = this.$store.getters.listOfClassifiersOfObjects(objectId)
      return classifiers.find(classifier => classifier.id === classifierId)
    },
    getClassifierHint(objectId, classifierId) {
      let classifier =  this.getClassifier(objectId, classifierId)
      return classifier.hint ?  classifier.hint : 'Описание отсутствует'
    },
  },
}
</script>

<style scoped>

</style>