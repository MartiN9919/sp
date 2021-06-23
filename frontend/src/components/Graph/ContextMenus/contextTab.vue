<template>
  <v-list rounded>
    <v-list-item
      v-for="(item, index) in bodyRightClickMenu" :key="index" dense
      @click="$emit('selectMenuItem', item)">
      <v-list-item-title style="font-size: 1em">{{ item.title }}</v-list-item-title>
      <v-list-item-icon><v-icon right color="teal">{{item.icon}}</v-icon></v-list-item-icon>
    </v-list-item>
  </v-list>
</template>

<script>
export default {
  name: "customAppBarCM",
  data: () => ({
    bodyRightClickMenu: [
      {
        id: 0,
        title: 'Закрыть вкладку',
        icon: 'mdi-close',
      },
      {
        id: 1,
        title: 'Удалить объект',
        icon: 'mdi-delete',
      },
    ],
  })
}
</script>

<style scoped>

</style>