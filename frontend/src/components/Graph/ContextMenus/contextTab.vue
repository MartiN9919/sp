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
        id: 2,
        title: 'Создать новый объект',
        icon: 'mdi-plus',
      },
      {
        id: 3,
        title: 'Найти объект',
        icon: 'mdi-magnify',
      },
      {
        id: 0,
        title: 'Закрыть вкладку',
        icon: 'mdi-close',
      },
    ],
  }),
}
</script>

<style scoped>

</style>