<template>
  <v-simple-table fixed-header class="elevation-20 simple-table" height="100%">
    <template v-slot:default>
      <thead>
        <tr>
          <th
            v-for="classifier in listOfClassifiersOfObjects(object.object_id)" :key="classifier.name"
            v-if="classifier.need === 1" class="text-left header-table"
          >
            <span class="font-weight-medium text-uppercase">{{classifier.title}}</span>
          </th>
          <th class="header-table text-right">
            <span class="font-weight-medium text-uppercase">Выбрать</span>
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
            <td class="text-right">
              <v-btn icon @click.stop="$emit('changeFindObject', findObject)">
                <v-icon>mdi-check</v-icon>
              </v-btn>
            </td>
          </tr>
          <tr v-if="opened.includes(key)">
            <td colspan="9999" class="context-row">
              <form-show-find-objects :object="findObject"></form-show-find-objects>
            </td>
          </tr>
        </template>
      </tbody>
    </template>
  </v-simple-table>
</template>

<script>
import { mapGetters } from "vuex"
import formShowFindObjects from "./formShowFindObjects"

export default {
  name: "listFoundObjects",
  props: { object: Object, },
  components: { formShowFindObjects, },
  computed: {
    ...mapGetters(['listOfClassifiersOfObjects', 'foundObjects']),
  },
  data: () => ({
    opened: [],
  }),
  methods: {
    checkClassifierForNeeded (valueForCheck, classifierId) {
      for (let value of valueForCheck)
        if (value.id === classifierId) return value.value
      return '-'
    },
    toggle(id) {
      const index = this.opened.indexOf(id);
      if (index > -1) this.opened.splice(index, 1)
      else this.opened.push(id)
    },
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
.header-table {
  background-color: #00796B !important;
  color: white !important;
}
.simple-table {
  border-radius: 0;
}

</style>