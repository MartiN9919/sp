<template>
  <v-simple-table class="ma-3 elevation-13" fixed-header height="40em">
    <template v-slot:default>
      <thead>
        <tr>
          <th
            v-for="classifier in listOfClassifiersOfObjects(object.object_id)"
            v-if="classifier.need === 1" :key="classifier.name" class="text-left"
          >
            {{classifier.title}}
          </th>
        </tr>
      </thead>
      <tbody>
      <template v-for="findObject in foundObjects(object.tempId)">
        <tr>
          <td
            v-for="classifier in listOfClassifiersOfObjects(object.object_id)"
            v-if="classifier.need === 1" :key="classifier.name"
          >
            {{checkClassifierForNeeded(findObject.params, classifier.id)}}
          </td>
        </tr>
        <tr>
          <td colspan="9999">
            <v-text-field
                v-for="param in findObject.params" :key="param.id"
                readonly hide-details :label="titleClassifier(findObject.object_id, param.id)"
                v-model="param.value" color="teal"
            ></v-text-field>
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
  props: {
    object: Object,
  },
  computed: {
    ...mapGetters(['listOfClassifiersOfObjects', 'foundObjects']),
  },
  data () {
    return {
      desserts: [
        {
          name: 'Frozen Yogurt',
          calories: 159, asdsadaasdsadasdasdasdasdasd: "ASDDDDDDDDDASDDDDDDDDDDDDDDD"
        },
        {
          name: 'Ice cream sandwich asdasd asd asd asd asd asd asd asd',
          calories: 237, asdsadaasdsadasdasdasdasdasd: "ASDDDDDDDDDASDDDDDDDDDDDDDDD"
        },
        {
          name: 'Eclair',
          calories: 262, asdsadaasdsadasdasdasdasdasd: "ASDDDDDDDDDASDDDDDDDDDDDDDDD"
        },
        {
          name: 'Cupcake',
          calories: 305,
        },
        {
          name: 'Gingerbread',
          calories: 356, asdsadaasdsadasdasdasdasdasd: "ASDDDDDDDDDASDDDDDDDDDDDDDDD"
        },
        {
          name: 'Jelly bean',
          calories: 375, asdsadaasdsadasdasdasdasdasd: "ASDDDDDDDDDASDDDDDDDDDDDDDDD"
        },
        {
          name: 'Lollipop',
          calories: 392, asdsadaasdsadasdasdasdasdasd: "ASDDDDDDDDDASDDDDDDDDDDDDDDD"
        },
        {
          name: 'Honeycomb',
          calories: 408, asdsadaasdsadasdasdasdasdasd: "ASDDDDDDDDDASDDDDDDDDDDDDDDD"
        },
        {
          name: 'Donut',
          calories: 452, asdsadaasdsadasdasdasdasdasd: "ASDDDDDDDDDASDDDDDDDDDDDDDDD"
        },
        {
          name: 'KitKat',
          calories: 518, asdsadaasdsadasdasdasdasdasd: "ASDDDDDDDDDASDDDDDDDDDDDDDDD"
        },
      ],
    }
  },
  methods: {
    titleClassifier(objectId, classifierId) {
      return this.listOfClassifiersOfObjects(objectId).find(classifier => classifier.id === classifierId).title
    },
    checkClassifierForNeeded (valueForCheck, classifierId) {
      for (let value of valueForCheck)
        if (value.id === classifierId) return value.value
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