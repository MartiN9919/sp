<template>
  <v-row no-gutters class="menu">
    <v-list :color="$CONST.APP.COLOR_OBJ" :width="$CONST.APP.TOOL_MENU.WIDTH" height="100%" dark dense>
      <v-list-item-group v-model="activeItem">
        <custom-tooltip v-for="tool in items" :key="tool.name" :body-text="tool.description" right>
          <template v-slot:activator="{ on }">
            <v-list-item v-on="on" :value="tool.name">
              <v-list-item-content>
                <v-list-item-icon>
                  <v-icon>{{tool.icon}}</v-icon>
                </v-list-item-icon>
              </v-list-item-content>
            </v-list-item>
          </template>
        </custom-tooltip>
      </v-list-item-group>
    </v-list>
    <div :style="stylesComponent">
      <slot></slot>
    </div>
  </v-row>
</template>

<script>
import CustomTooltip from "@/components/WebsiteShell/CustomComponents/customTooltip"
import {mapActions, mapGetters} from "vuex"
import router from '@/router'

export default {
  name: "toolsMenu",
  components: {CustomTooltip},
  computed: {
    ...mapGetters(['activeTool', 'toolsMenu']),
    stylesComponent: function () {
      return { 'width': `calc(100% - ${this.$CONST.APP.TOOL_MENU.WIDTH}px)`}
    },
    items: function () {
      return this.toolsMenu(router.currentRoute.name)
    },
    activeItem: {
      get: function () {
        return this.activeTool(router.currentRoute.name)
      },
      set: function (item) {
        if(item) {
          this.setActiveTool(item)
        }
      }
    }
  },
  methods: mapActions(['setActiveTool'])
}
</script>

<style scoped>
.menu {
  flex-wrap: nowrap;
  height: 100%;
}</style>