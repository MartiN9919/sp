<template>
  <v-list rounded>
    <v-list-item
        v-for="(item, index) in bodyRightClickMenu" :key="index" dense
        @click="$emit('selectMenuItem', item.id)">
      <v-list-item-title style="font-size: 1em">{{ item.title }}</v-list-item-title>
      <v-list-item-icon><v-icon right color="teal">{{item.icon}}</v-icon></v-list-item-icon>
    </v-list-item>
  </v-list>
</template>

<script>
export default {
  name: "contextGraphWorkPlace",
  data: () => ({
    bodyRightClickMenu: [
      {
        id: 1,
        title: 'Добавить объект',
        icon: 'mdi-database-plus',
      },
      {
        id: 2,
        title: 'Удалить объект',
        icon: 'mdi-database-minus',
      },
    ],
  }),
  methods: {
    selectObject () {
      this.$emit('selectObject', this.selectedObject)
      this.selectedObject = null
    }
  }
}
</script>

<style scoped>

</style>