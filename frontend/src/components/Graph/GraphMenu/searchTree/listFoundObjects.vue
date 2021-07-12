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
              <v-tooltip
                v-for="param in findObject.params" :key="param.id" bottom
                open-delay="1000" nudge-bottom="-15" transition="false" color="#00796B" z-index="10001" max-width="20%"
              >
                <template v-slot:activator="{ on }">
                  <v-textarea
                    v-if="!param.old.length" v-model="param.value" v-on="on"
                    :label="getClassifier(findObject.object_id, param.id).title"
                    readonly hide-details rows="1" auto-grow color="teal" class="py-2"
                  ></v-textarea>
                  <v-select
                    v-else v-model='param.date' :items="[{ value: param.value, date: param.date }].concat(param.old)"
                    attach hide-details class="pb-2" color="teal" type="text" item-color="teal" autocomplete="off"
                    :label="getClassifier(findObject.object_id, param.id).title" item-text="value" item-value="date"
                    :menu-props="{ offsetY: true, maxWidth: '100%', minWidth: '100%', closeOnClick: true }"
                    append-icon="mdi-format-list-bulleted" placeholder="Выберете необходимое значение"
                  >
                    <template v-slot:item="{ item }">
                      <v-list-item
                        @click="" :key="item.date"
                        :style="param.date !== item.date || { backgroundColor: '#E0F2F1' }"
                      >
                        <v-row no-gutters>
                          <v-col>{{item.value}}</v-col>
                          <v-col class="d-flex text-right align-center" cols="auto">{{item.date}}</v-col>
                        </v-row>
                      </v-list-item>
                    </template>
                  </v-select>
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