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
  props: { activatedObject: Boolean },
  computed: {
    bodyRightClickMenu: function () {
      let bodyMenu = [{ id: 0, title: 'Закрыть вкладку', icon: 'mdi-close' }]
      if (!this.activatedObject) {
        bodyMenu.push({ id: 2, title: 'Создать новый объект', icon: 'mdi-plus' })
        bodyMenu.push({ id: 3, title: 'Найти объект', icon: 'mdi-magnify' })
      }
      return bodyMenu
    }
  }
}
</script>

<style scoped>

</style>