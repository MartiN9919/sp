<template>
  <v-card class="pa-4">
    <v-expansion-panels disabled>
      <v-expansion-panel>
        <v-expansion-panel-header hide-actions color="teal" style="color: white">
          <v-row no-gutters class="text-center">
            <v-col cols="1">id</v-col>
            <v-col
              v-for="classifier in templatesClassifiersForObjects(object.objectId)"
              v-if="classifier.need === 1" :key="classifier.name"
            >
              {{classifier.title}}
            </v-col>
          </v-row>
        </v-expansion-panel-header>
      </v-expansion-panel>
    </v-expansion-panels>
    <v-expansion-panels focusable multiple>
      <v-expansion-panel v-for="findObject in foundObjects(object.tempId)" :key="findObject.rec_id">
        <v-expansion-panel-header hide-actions>
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
  </v-card>
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
        if (Number(value.id) === classifierId) return value.val
      return '-'
    },
  },
}
</script>

<style scoped>

</style>