<template>
  <v-card flat dark color="#00796B" height="80%" class="overflow-hidden">
    <v-row no-gutters style="height: 100%">
      <v-col cols="auto">
        <v-tabs vertical dark background-color="#00796B" v-model="activeObjectTab">
          <v-tab v-for="object in copyConflictingObjects" :key="object.rec_id">
            <v-icon right>{{ primaryObject(activeObject.object_id).icon }}</v-icon>
            <span>№{{object.rec_id}}</span>
          </v-tab>
        </v-tabs>
      </v-col>
      <v-col>
        <v-tabs-items v-model="activeObjectTab">
          <v-tab-item v-for="(object, key) in copyConflictingObjects" :key="object.rec_id" :transition="false">
            <v-row no-gutters style="height: 100%">
              <conflicting-object
                :object="object"
                @saveObject="saveObject"
              ></conflicting-object>
              <v-divider vertical class="mx-0"></v-divider>
              <list-params
                :ref="'listParams' + key.toString()"
                :object="object"
                @moveClassifier="moveClassifier($event, object)"
              ></list-params>
            </v-row>
          </v-tab-item>
        </v-tabs-items>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import { mapGetters } from "vuex"
import conflictingObject from "./conflictingObject"
import listParams from "./listParams"

export default {
  name: "conflictForm",
  components: { conflictingObject, listParams, },
  data: () => ({
    activeObjectTab: null,
  }),
  computed: {
    ...mapGetters(['conflictingObjects', 'primaryObject', 'activeObject', 'conflictingObjects', ]),
    copyConflictingObjects: {
      get: function () {
        this.activeObjectTab = 0
        let objects = this.conflictingObjects
        for (let object of objects)
          object.newClassifiers = JSON.parse(JSON.stringify(this.activeObject.params))
        return objects
      },
      set: function (value) { this.$store.dispatch('changeConflictingObjects', value) },
    },
  },
  methods: {
    moveClassifier(classifier, object) {
      let hasClassifier = object.params.find(item => item.id === classifier.id)
      if (hasClassifier) {
        let oldClassifier = { date: hasClassifier.date, value: hasClassifier.value, }
        hasClassifier.old.push(oldClassifier)
        hasClassifier.date = ''
        hasClassifier.value = classifier.value
      } else {
        object.params.push({ id: classifier.id, date: '', value: classifier.value, old: [] })
      }
      object.newClassifiers.splice(object.newClassifiers.findIndex(prop => prop === classifier), 1)
      this.$nextTick(function () {
        this.$refs['listParams' + this.activeObjectTab.toString()][0].$forceUpdate()
      })

    },
    saveObject (object) {
      delete object.newClassifiers
      console.log(object)
      this.$store.dispatch('createNewObjectFromServer', object)
    }
  },
}
</script>

<style scoped>

</style>