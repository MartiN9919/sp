<template>
  <v-menu
    v-model="show"
    :position-x="menuSettings.xRightClickMenuPosition"
    :position-y="menuSettings.yRightClickMenuPosition"
    :close-on-content-click="false"
    absolute offset-y no-action z-index="10001"
  >
    <v-list rounded>
      <v-list-group v-for="(item, itemIndex) in menuSettings.bodyRightClickMenu" v-if="'items' in item"  :key="'group_'+itemIndex">
        <template v-slot:activator>
          <v-list-item-content>
            <v-list-item-title><v-icon left>{{item.icon}}</v-icon> {{item.title}}</v-list-item-title>
          </v-list-item-content>
        </template>
        <v-list-item
          v-for="(itemGroup, groupIndex) in item.items"
          @click="$emit('selectedItem', itemGroup); show=false"
          :key="groupIndex" link>
          <v-list-item-icon v-if="itemGroup.icon"><v-icon right>{{itemGroup.icon}}</v-icon></v-list-item-icon>
          <v-list-item-title>{{itemGroup.title}}</v-list-item-title>
        </v-list-item>
      </v-list-group>
      <v-list-item v-else v-for="(item, index) in menuSettings.bodyRightClickMenu" :key="index">
        <v-list-item-title>{{ item.title }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>
export default {
  name: "rightClickMenu",
  model: { prop: 'showRightClickMenu', event: 'changeShowRightClickMenu' },
  props: {
    menuSettings: Object,
    showRightClickMenu: Boolean,
  },
  computed: {
    show: {
      get: function () { return this.showRightClickMenu },
      set: function (val) { this.$emit('changeShowRightClickMenu', val) }
    }
  }
}
</script>

<style scoped>

</style>