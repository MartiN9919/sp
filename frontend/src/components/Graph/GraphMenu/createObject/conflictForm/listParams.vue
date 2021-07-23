<template>
  <v-col>
    <v-card flat height="100%" style="display: flex; flex-direction: column; justify-content: space-between">
      <div style="height: calc(100% - 4em)">
        <v-card-title class="headline justify-center overflow-hidden pt-2" style="height: 1.9em">
          <span>Объект, который вы пытаетесь создать</span>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="px-3 overflow-y-auto" style="height: calc(100% - 3em)">
          <v-textarea
            v-for="classifier in object.newClassifiers" :key="classifier.id"
            v-model="classifier.value"
            :label="getClassifier(object.object_id, classifier.id).title"
            readonly hide-details rows="1" auto-grow color="teal" class="py-2"
          >
            <template v-slot:prepend="">
              <v-btn icon small @click="moveClassifier(classifier)" v-if="getClassifier(object.object_id, classifier.id).need !== 1">
                <v-icon color="teal">mdi-arrow-left</v-icon>
              </v-btn>
            </template>
          </v-textarea>
        </v-card-text>
      </div>
      <v-card-actions class="justify-end" style="height: 3.5em">
        <v-btn outlined color="teal">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-col>
</template>

<script>
export default {
  name: "listParams",
  props: {
    object: Object,
  },
  methods: {
    getClassifier (objectId, classifierId) {
      return this.$store.getters.listOfClassifiersOfObjects(objectId).find(classifier => classifier.id === classifierId)
    },
    moveClassifier (classifier) {
      this.$emit('moveClassifier', classifier)
    },
  }
}
</script>

<style scoped>

</style>