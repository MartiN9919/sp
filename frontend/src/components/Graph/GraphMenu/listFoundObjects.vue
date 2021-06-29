<template>
  <div>
    <v-row no-gutters class="header-panel py-2">
      <v-col
          v-for="classifier in listOfClassifiersOfObjects(object.object_id)"
          v-if="classifier.need === 1" :key="classifier.name" class="pl-4"
      >
        <span class="text-uppercase">{{classifier.title}}</span>
      </v-col>
      <v-col cols="1"></v-col>
    </v-row>
    <v-expansion-panels tile focusable multiple hover class="overflow-y-auto">
      <v-expansion-panel v-for="findObject in foundObjects(object.tempId)" :key="findObject.rec_id">
        <v-expansion-panel-header class="pa-0 border-item-header" disable-icon-rotate>
          <v-row no-gutters>
            <v-col
              v-for="classifier in listOfClassifiersOfObjects(object.object_id)"
              v-if="classifier.need === 1" :key="classifier.name" class="pl-4"
            >
              {{checkClassifierForNeeded(findObject.params, classifier.id)}}
            </v-col>
          </v-row>
          <template v-slot:actions>
            <v-btn icon class="mr-3" @click.stop="">
              <v-icon color="teal">
                mdi-check
              </v-icon>
            </v-btn>
          </template>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-text-field
            v-for="param in findObject.params" :key="param.id"
            readonly hide-details :label="titleClassifier(findObject.object_id, param.id)"
            v-model="param.val" color="teal"
          ></v-text-field>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "listFoundObjects",
  props: {
    object: Object,
  },
  computed: {
    ...mapGetters(['listOfClassifiersOfObjects', 'foundObjects']),
  },
  methods: {
    titleClassifier(objectId, classifierId) {
      return this.listOfClassifiersOfObjects(objectId).find(classifier => classifier.id === classifierId).title
    },
    checkClassifierForNeeded (valueForCheck, classifierId) {
      for (let value of valueForCheck)
        if (value.id === classifierId) return value.val
      return '-'
    },
  },
}
</script>

<style scoped>

.header-panel {
  background-color: #00796B;
  color: white;
  height: 2.6em;
  align-content: center;
}
</style>