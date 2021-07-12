<template>
  <v-window v-model="stepWindowStyle">
    <v-window-item key="menuItemSelection" value="menuItemSelection"> <!-- transition="" reverse-transition="" -->
      <v-list rounded>
        <v-list-item
            v-for="(item, index) in bodyRightClickMenu" :key="index" dense
            @click="'next' in item ? stepWindowStyle = item.next : $emit('selectMenuItem', item)">
          <v-list-item-title style="font-size: 1em">{{ item.title }}</v-list-item-title>
          <v-list-item-icon><v-icon right color="teal">{{item.icon}}</v-icon></v-list-item-icon>
        </v-list-item>
      </v-list>
    </v-window-item>
    <v-window-item key="selectClassifier" value="selectClassifier"> <!-- transition="" reverse-transition="" -->
      <v-card flat>
        <v-card-subtitle class="text-uppercase py-2 text-center text-break" style="background-color: #009688; color: white">
          Выберете Классификатор
        </v-card-subtitle>
        <v-divider></v-divider>
        <v-card-text class="pa-1">
          <v-card-actions>
            <v-btn icon @click="stepWindowStyle = 'menuItemSelection'" color="teal">
              <v-icon>mdi-arrow-left</v-icon>
            </v-btn>
            <v-autocomplete
              :items="items" item-text="title"
              v-model="selectedClassifier" hide-details
              return-object color="teal" hide-no-data
              class="pa-0 ma-0 pb-2" item-color="teal"
            ></v-autocomplete>
            <v-btn icon color="teal" :disabled="!selectedClassifier" @click="selectClassifier">
              <v-icon>mdi-check</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card-text>
      </v-card>
    </v-window-item>
  </v-window>
</template>

<script>
import {mapGetters} from "vuex";

export default {
  name: "contextCreatorObject",
  props: { objectId: Number, classifiers: Array, },
  data: () => ({
    stepWindowStyle: 'menuItemSelection',
    selectedClassifier: null,
    bodyRightClickMenu: [
      {
        title: 'Добавить классификатор',
        icon: 'mdi-database-plus',
        next: 'selectClassifier',
      },
    ],
  }),
  computed: {
    ...mapGetters(['classifiersForObjects', ]),
    items: function () {
      let resultClassifiers = []
      let allClassifiers = this.classifiersForObjects(this.objectId)
      for (let item of allClassifiers)
        if (!this.classifiers.find(cl => cl.id === item.id))
          resultClassifiers.push(item)
      return resultClassifiers
    },
  },
  methods: {
    selectClassifier() {
      this.$emit('selectClassifier', this.selectedClassifier)
      this.selectedClassifier = null
    },
  },
}
</script>

<style scoped>

</style>