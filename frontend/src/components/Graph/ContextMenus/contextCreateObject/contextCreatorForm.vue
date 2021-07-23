<template>
  <v-list rounded>
    <v-list-item
        v-for="(item, index) in bodyRightClickMenu" :key="index" dense
        @click="$emit('deleteClassifier', item)">
      <v-list-item-title style="font-size: 1em">{{ item.title }}</v-list-item-title>
      <v-list-item-icon><v-icon right color="teal">{{item.icon}}</v-icon></v-list-item-icon>
    </v-list-item>
  </v-list>
</template>

<script>
export default {
  name: "contextCreatorForm",
  data: () => ({
    bodyRightClickMenu: [
      {
        title: 'Удалить классификатор',
        icon: 'mdi-database-plus',
      },
    ]
  }),
}
</script>

<style scoped>

</style>