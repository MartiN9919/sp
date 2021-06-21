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
              <v-btn icon color="teal" :disabled="!selectedObject" @click="$emit('selectObject', selectedObject)">
                <v-icon>mdi-check</v-icon>
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
  </v-window>
</template>

<script>
import ObjectFinder from "../../Graph/Mixins/ObjectFinder";

export default {
  name: "workSpaceContextMenu",
  mixins: [ObjectFinder, ],
  data: () => ({
    stepWindowStyle: 'menuItemSelection',
    selectedObject: null,
    bodyRightClickMenu: [
      {
        title: 'Создать объект',
        icon: 'mdi-database-plus',
        next: 'selectObject',
      },
    ],
  }),
}
</script>

<style scoped>

</style>