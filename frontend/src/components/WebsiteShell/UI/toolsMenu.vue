<template>
  <v-list color="#00796B" height="100%" width="56" dark dense>
    <v-list-item-group v-model="activeItem">
      <v-list-item
        v-for="tool in items"
        :key="tool.name"
        :value="tool.name"
        :disabled="tool.name === activeItem || tool.disabled"
      >
        <v-list-item-content>
          <v-list-item-icon>
            <v-icon :color="tool.disabled ? 'grey' : 'white'">{{tool.icon}}</v-icon>
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
    ...mapGetters(['activeTool', 'toolsMenu']),
    items: function () { return this.toolsMenu(router.currentRoute.name) },
    activeItem: {
      get: function () { return this.activeTool(router.currentRoute.name) },
      set: function (item) { this.setActiveTool(item) },
    },
  },
  methods: mapActions(['setActiveTool', ])
}
</script>

<style scoped>

</style>