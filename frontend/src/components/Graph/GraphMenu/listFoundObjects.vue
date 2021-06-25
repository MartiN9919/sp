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
    <v-expansion-panels focusable multiple>
      <v-expansion-panel v-for="findObject in foundObjects(object.tempId)" :key="findObject.rec_id">
        <v-expansion-panel-header hide-actions class="pa-0">
          <v-row no-gutters class="text-center">
            <v-col cols="1">{{findObject.rec_id}}</v-col>
            <v-col
                v-for="classifier in templatesClassifiersForObjects(object.objectId)"
                v-if="classifier.need === 1"
            >
              {{checkClassifierForNeeded(findObject.params, classifier.id)}}
            </v-col>
          </v-row>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
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