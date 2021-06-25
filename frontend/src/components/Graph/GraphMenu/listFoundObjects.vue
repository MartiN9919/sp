<template>
  <div>
    <v-expansion-panels disabled tile>
      <v-expansion-panel>
        <v-expansion-panel-header hide-actions color="teal" style="color: white" class="pa-0">
          <v-row no-gutters class="text-center ma-0 pa-0">
            <v-col cols="1"><span class="text-uppercase">id</span></v-col>
            <v-col
              v-for="classifier in templatesClassifiersForObjects(object.objectId)"
              v-if="classifier.need === 1" :key="classifier.name"
            >
              <span class="text-uppercase">{{classifier.title}}</span>
            </v-col>
          </v-row>
        </v-expansion-panel-header>
      </v-expansion-panel>
    </v-expansion-panels>
    <v-expansion-panels focusable multiple style="background-color: #009688">
      <v-expansion-panel v-for="findObject in foundObjects(object.tempId)" :key="findObject.rec_id">
        <v-expansion-panel-header hide-actions class="pa-0">
          <v-row no-gutters class="text-center">
            <v-col cols="1">{{findObject.rec_id}}</v-col>
            <v-col
                v-for="classifier in templatesClassifiersForObjects(object.objectId)"
                v-if="classifier.need === 1" :key="classifier.name"
            >
              {{checkClassifierForNeeded(findObject.params, classifier.id)}}
            </v-col>
          </v-row>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-text-field
            v-for="param in findObject.params"
            readonly hide-details :label="titleClassifier(findObject.object_id, param.id)"
            v-model="param.val" color="teal"
          ></v-text-field>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>

<script>
import {mapGetters} from "vuex";

export default {
  name: "listFoundObjects",
  props: {
    object: Object,
  },
  computed: {
    ...mapGetters(['templatesClassifiersForObjects', 'foundObjects']),
  },
  methods: {
    titleClassifier(objectId, classifierId) {
      return this.templatesClassifiersForObjects(objectId).find(classifier => classifier.id === classifierId).title
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

</style>