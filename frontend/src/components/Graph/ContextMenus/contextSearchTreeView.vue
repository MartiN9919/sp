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
    <v-window-item key="selectObject" value="selectObject"> <!-- transition="" reverse-transition="" -->
      <v-card flat>
        <v-card-subtitle class="text-uppercase py-2 text-center text-break block-card-subtitle">
          Выберете объект для связи с объектом: &laquo{{getTitleActiveObjectById}}&raquo
        </v-card-subtitle>
        <v-divider></v-divider>
        <v-card-actions class="pa-1">
          <v-btn icon @click="stepWindowStyle = 'menuItemSelection'" color="teal">
            <v-icon>mdi-arrow-left</v-icon>
          </v-btn>
          <v-autocomplete
            :items="listObjectTemplates" item-text="title"
            v-model="selectedObject" hide-details
            return-object color="teal" hide-no-data
            class="pa-0 ma-0 pb-2" item-color="teal"
          ></v-autocomplete>
          <v-btn icon color="teal" :disabled="!selectedObject" @click="getRelationAfterSelectedObject()">
            <v-icon>mdi-arrow-right</v-icon>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-window-item>
    <v-window-item key="selectRelation" value="selectRelation"> <!-- transition="" reverse-transition="" -->
      <v-card flat>
        <v-card-subtitle class="text-uppercase py-2 text-center text-break block-card-subtitle">
          <span>Выберете связь между
            &laquo{{getTitleActiveObjectById}}&raquo и
            &laquo{{getTitleSelectedObjectById}}&raquo</span>
        </v-card-subtitle>
        <v-divider></v-divider>
        <v-card-actions class="pa-1">
          <v-btn icon @click="stepWindowStyle = 'selectObject'" color="teal">
            <v-icon>mdi-arrow-left</v-icon>
          </v-btn>
          <v-autocomplete
            :items="getRelations" item-text="title"
            v-model="selectedRelation" hide-details
            return-object color="teal" hide-no-data
            class="pa-0 ma-0 pb-2" item-color="teal"
          ></v-autocomplete>
          <v-btn icon color="teal" @click="returnChangeObjectRelation">
            <v-icon>mdi-check</v-icon>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-window-item>
  </v-window>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  name: "contextSearchTreeView",
  props: {
    object: Object,
  },
  data: () => ({
    stepWindowStyle: 'menuItemSelection',
    selectedObject: null,
    selectedRelation: null,
    bodyRightClickMenu: [
      {
        title: 'Добавить объект',
        icon: 'mdi-database-plus',
        next: 'selectObject',
      },
    ],
  }),
  computed: {
    ...mapGetters(['relationsBetweenTwoObjects', 'listObjectTemplates', 'objectTemplates', ]),
    getTitleActiveObjectById: function () {
      return this.objectTemplates(this.object.object_id).title_single
    },
    getTitleSelectedObjectById: function () {
      if(this.selectedObject)
        return this.selectedObject.title_single
      else return ''
    },
    getRelations: function () {
      let listRelations = this.relationsBetweenTwoObjects({
        objectId1: this.object.object_id,
        objectId2: this.selectedObject?.id
      })
      if (listRelations)
        return listRelations.relations
      else return []
    },
  },
  methods: {
    ...mapActions(['getRelationsForObjects', ]),
    returnChangeObjectRelation () {
      this.$emit('createNewRelation', {
        selectedObject: this.selectedObject,
        selectedRelation: this.selectedRelation,
      })
      this.closeContextMenu()
    },
    getRelationAfterSelectedObject () {
      this.getRelationsForObjects({ params: {
          object_1_id: this.object.object_id,
          object_2_id: this.selectedObject.id
        }
      })
      this.stepWindowStyle = 'selectRelation'
    },
    closeContextMenu () {
      this.stepWindowStyle = 'menuItemSelection'
      this.selectedObject = null
      this.selectedRelation = null
    },
  },
  watch: {
    object: function (value) {
      this.closeContextMenu()
    }
  }
}
</script>

<style scoped>
.block-card-subtitle {
  background-color: #009688;
  color: white !important;
}

</style>