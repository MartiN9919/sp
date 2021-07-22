<template>
  <v-simple-table fixed-header class="simple-table" height="100%">
    <template v-slot:default>
      <thead>
        <tr>
          <th
              v-for="classifier in listOfClassifiersOfObjects" :key="classifier.name"
              v-if="classifier.need === 1" class="text-left header-table"
          >
            <span class="font-weight-medium text-uppercase">{{classifier.title}}</span>
          </th>
        </tr>
      </thead>
      <tbody>
        <template v-for="findObject in foundObjects">
          <tr @click.stop="$emit('changeFindObject', findObject)">
            <td
              v-for="classifier in listOfClassifiersOfObjects"
              v-if="classifier.need === 1" :key="classifier.name" class="text-left"
            >
              <span>{{checkClassifierForNeeded(findObject.params, classifier.id)}}</span>
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
  components: { formShowFindObjects, },
  props: {
    objectId: Number,
    foundObjects: Array,
  },
  computed: {
    ...mapGetters(['listOfClassifiersOfObjects',]),
  },
  methods: {
    checkClassifierForNeeded (valueForCheck, classifierId) {
      for (let value of valueForCheck)
        if (value.id === classifierId) return value.value
      return '-'
    },
  },
}
</script>

<style scoped>
tr:hover {
  background-color: transparent !important;
  cursor: pointer;
}
.header-table {
  background-color: #00796B !important;
  color: white !important;
}
.simple-table {
  border-radius: 0;
}

</style>