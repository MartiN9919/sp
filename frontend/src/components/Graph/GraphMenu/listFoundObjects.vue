<template>
  <v-simple-table class="mx-3 my-5 elevation-13" fixed-header>
    <template v-slot:default>
      <thead>
        <tr>
          <th
            v-for="classifier in listOfClassifiersOfObjects(object.object_id)"
            v-if="classifier.need === 1" :key="classifier.name" class="text-left"
          >
            <span class="font-weight-medium text-uppercase">{{classifier.title}}</span>
          </th>
        </tr>
      </thead>
      <tbody>
        <template v-for="(findObject, key) in foundObjects(object.tempId)">
          <tr @click="toggle(key)" :class="{ opened: opened.includes(key) }">
            <td
              v-for="classifier in listOfClassifiersOfObjects(object.object_id)"
              v-if="classifier.need === 1" :key="classifier.name" class="text-left"
            >
              <span>{{checkClassifierForNeeded(findObject.params, classifier.id)}}</span>
            </td>
          </tr>
          <tr v-if="opened.includes(key)" >
            <td colspan="9999" class="context-row">
              <v-tooltip
                v-for="param in findObject.params" :key="param.id" open-delay="1000" nudge-bottom="-15"
                bottom transition="false" color="#00796B" z-index="10001" max-width="20%"
              >
                <template v-slot:activator="{ on }">
                  <v-textarea
                    readonly hide-details rows="1" auto-grow
                    :label="getClassifier(findObject.object_id, param.id).title"
                    v-model="param.value" color="teal" class="pb-2" v-on="on"
                  ></v-textarea>
                </template>
                <p class="text-formatter-for-window-size additional-text text-justify ma-0">
                  {{getClassifierHint(findObject.object_id, param.id)}}
                </p>
              </v-tooltip>
            </td>
          </tr>
        </template>
      </tbody>
    </template>
  </v-simple-table>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "listFoundObjects",
  props: { object: Object, },
  computed: {
    ...mapGetters(['listOfClassifiersOfObjects', 'foundObjects']),
  },
  data: () => ({
    opened: [],
  }),
  methods: {
    getClassifier(objectId, classifierId) {
      return this.listOfClassifiersOfObjects(objectId).find(classifier => classifier.id === classifierId)
    },
    getClassifierHint(objectId, classifierId) {
      let classifier =  this.getClassifier(objectId, classifierId)
      return classifier.hint ?  classifier.hint : 'Описание отсутствует'
    },
    checkClassifierForNeeded (valueForCheck, classifierId) {
      for (let value of valueForCheck)
        if (value.id === classifierId) return value.value
      return '-'
    },
    toggle(id) {
      const index = this.opened.indexOf(id);
      if (index > -1) {
        this.opened.splice(index, 1)
      } else {
        this.opened.push(id)
      }
    }
  },
}
</script>

<style scoped>
tr:hover {
  background-color: transparent !important;
  cursor: pointer;
}
.opened {
  color: #00796B;
}
.context-row {
  border-left: 6px outset #00796B;
}
</style>