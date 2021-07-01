<template>
  <v-window v-model="stepWindowStyle">
    <v-window-item key="menuItemSelection" value="menuItemSelection">
      <v-list rounded>
        <v-list-item
            v-for="(item, index) in bodyRightClickMenu" :key="index" dense
            @click="'next' in item ? stepWindowStyle = item.next : $emit('selectMenuItem', item)">
          <v-list-item-title style="font-size: 1em">{{ item.title }}</v-list-item-title>
          <v-list-item-icon><v-icon right color="teal">{{item.icon}}</v-icon></v-list-item-icon>
        </v-list-item>
      </v-list>
    </v-window-item>
    <v-window-item key="selectObject" value="selectObject">
      <v-card flat tile>
        <v-card-subtitle class="text-uppercase py-2 text-center text-break custom-card-subtitle">
          Выберете объект, который хотите создать
        </v-card-subtitle>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn icon @click="stepWindowStyle = 'menuItemSelection'" color="teal">
            <v-icon>mdi-arrow-left</v-icon>
          </v-btn>
          <v-autocomplete
            :items="$store.getters.listOfPrimaryObjects" item-text="title"
            v-model="selectedObject" hide-details
            return-object color="teal" hide-no-data
            class="pa-0 ma-0 pb-2" item-color="teal"
          ></v-autocomplete>
          <v-btn icon color="teal" :disabled="!selectedObject" @click="$emit('selectObject', selectedObject)">
            <v-icon>mdi-check</v-icon>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-window-item>
  </v-window>
</template>

<script>
export default {
  name: "contextD3WorkSpace",
  data: () => ({
    stepWindowStyle: 'menuItemSelection',
    selectedObject: null,
    bodyRightClickMenu: [
      {
        title: 'Добавить объект',
        icon: 'mdi-database-plus',
        next: 'selectObject',
      },
      {
        title: 'Удалить объект',
        icon: 'mdi-database-minus',
      },
    ],
  }),
}
</script>

<style scoped>
  .custom-card-subtitle {
    background-color: #00796B;
    color: white !important;
  }
</style>