<template>
  <v-list :color="$CONST.APP.COLOR_OBJ" :width="$CONST.APP.TOOL_MENU.WIDTH" height="100%" dark dense>
    <v-list-item-group v-model="activeItem">
      <v-list-item v-for="tool in items" :key="tool.name" :value="tool.name" :disabled="itemStatus(tool)">
        <v-list-item-content>
          <v-list-item-icon>
            <v-icon :color="itemTextColor(tool)">{{tool.icon}}</v-icon>
          </v-list-item-icon>
        </v-list-item-content>
      </v-list-item>
    </v-list-item-group>
  </v-list>
</template>

<script>
import {mapActions, mapGetters} from "vuex"
import router from '@/router'

export default {
  name: "toolsMenu",
  computed: {
    ...mapGetters([
      'activeTool',
      'toolsMenu'
    ]),
    items: function () {
      return this.toolsMenu(router.currentRoute.name)
    },
    activeItem: {
      get: function () {
        return this.activeTool(router.currentRoute.name)
      },
      set: function (item) {
        this.setActiveTool(item)
      }
    }
  },
  methods: {
    ...mapActions(['setActiveTool']),
    itemStatus(tool) {
      return tool.name === this.activeItem || tool.disabled
    },
    itemTextColor(tool) {
      return tool.disabled ? this.$CONST.APP.TOOL_MENU.DISABLED_COLOR : this.$CONST.APP.TOOL_MENU.ACTIVE_COLOR
    }
  }
}
</script>

<style scoped>

</style>