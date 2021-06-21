<template>
  <v-window v-model="stepWindowStyle">
    <v-window-item key="menuItemSelection" value="menuItemSelection"> <!-- transition="" reverse-transition="" -->
      <v-card>
        <v-card-text class="pa-0">
          <v-list rounded>
            <v-list-item
                v-for="(item, index) in bodyRightClickMenu" :key="index"
                @click="'next' in item ? stepWindowStyle = item.next : $emit('selectMenuItem', item)">
              <v-list-item-title>{{ item.title }}</v-list-item-title>
              <v-list-item-icon><v-icon right>{{item.icon}}</v-icon></v-list-item-icon>
            </v-list-item>
          </v-list>
        </v-card-text>
      </v-card>
    </v-window-item>
    <v-window-item key="selectObject" value="selectObject"> <!-- transition="" reverse-transition="" -->
      <v-card flat>
        <v-card-title class="justify-center pa-0">
          Выберете объект
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pa-1">
          <v-autocomplete
              :items="listObjects" item-text="title"
              v-model="selectedObject" hide-selected
              return-object color="teal" hide-no-data
          >
            <template v-slot:append-outer>
              <v-btn icon color="teal" :disabled="!selectedObject" @click="getRelationAfterSelectedObject()">
                <v-icon>mdi-arrow-right</v-icon>
              </v-btn>
            </template>
            <template v-slot:prepend>
              <v-btn icon @click="stepWindowStyle = 'menuItemSelection'">
                <v-icon>mdi-arrow-left</v-icon>
              </v-btn>
            </template>
          </v-autocomplete>
        </v-card-text>
      </v-card>
    </v-window-item>
    <v-window-item key="selectRelation" value="selectRelation"> <!-- transition="" reverse-transition="" -->
      <v-card flat>
        <v-card-title class="justify-center pa-0">
<!--          <span>Выберете связь между {{titleObject(activeObject.objectId).title}} и {{selectedObject.title}}</span>-->
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pa-1">
          <v-autocomplete
              :items="relations" item-text="title"
              v-model="selectedRelation" hide-selected
              return-object color="teal" hide-no-data
          >
            <template v-slot:append-outer>
              <v-btn icon color="teal" :disabled="!selectedRelation" @click="$emit('selectObject', selectedRelation)">
                <v-icon>mdi-check</v-icon>
              </v-btn>
            </template>
            <template v-slot:prepend>
              <v-btn icon @click="stepWindowStyle = 'selectObject'">
                <v-icon>mdi-arrow-left</v-icon>
              </v-btn>
            </template>
          </v-autocomplete>
        </v-card-text>
      </v-card>
    </v-window-item>
  </v-window>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import ObjectFinder from "../../Graph/Mixins/ObjectFinder"

export default {
  name: "graphMenu",
  mixins: [ObjectFinder, ],
  props: {
    activeObject: Object,
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
    ...mapGetters(['relations', ]),
  },
  methods: {
    ...mapActions(['addRelations', ]),
    getRelationAfterSelectedObject () {
      this.addRelations({ params: {
          object_1_id: this.activeObject.objectId,
          object_2_id: this.selectedObject.id
        }
      })
      this.stepWindowStyle = 'selectRelation'
    },
  },
}
</script>

<style scoped>

</style>