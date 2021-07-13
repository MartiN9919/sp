<template>
  <div>
    <v-tooltip
      v-for="param in object.params" :key="param.id" bottom
      open-delay="1000" nudge-bottom="-15" transition="false" color="#00796B" z-index="10001" max-width="20%"
    >
      <template v-slot:activator="{ on }">
        <v-textarea
          v-if="!param.old.length" v-model="param.value" v-on="on"
          :label="getClassifier(object.object_id, param.id).title"
          readonly hide-details rows="1" auto-grow color="teal" class="py-2"
        ></v-textarea>
        <v-select
          v-else v-model='param.date' :items="[{ value: param.value, date: param.date }].concat(param.old)"
          attach hide-details class="py-2" color="teal" type="text" item-color="teal" autocomplete="off"
          :label="getClassifier(object.object_id, param.id).title" item-text="value" item-value="date"
          :menu-props="{ offsetY: true, maxWidth: '100%', minWidth: '100%', closeOnClick: true }"
          append-icon="mdi-format-list-bulleted" placeholder="Выберете необходимое значение"
        >
          <template v-slot:item="{ item }">
            <v-list-item
              @click="" :key="item.date" :style="param.date !== item.date || { backgroundColor: '#E0F2F1' }"
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
        {{getClassifierHint(object.object_id, param.id)}}
      </p>
    </v-tooltip>
  </div>
</template>

<script>
export default {
  name: "formShowFindObjects",
  props: {
    object: Object,
  },
  methods: {
    getClassifier(objectId, classifierId) {
      return this.$store.getters.listOfClassifiersOfObjects(objectId).find(classifier => classifier.id === classifierId)
    },
    getClassifierHint(objectId, classifierId) {
      let classifier =  this.getClassifier(objectId, classifierId)
      return classifier.hint ?  classifier.hint : 'Описание отсутствует'
    },
  },
}
</script>

<style scoped>

</style>