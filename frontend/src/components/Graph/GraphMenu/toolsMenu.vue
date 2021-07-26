<template>
  <v-list
    color="#00796B"
    height="100%"
    width="56"
    dark
  >
    <v-list-item-group
      v-model="activeItem"
    >
      <v-list-item
        v-for="tool in toolsMenu"
        :key="tool.name"
        :value="tool.name"
        :disabled="tool.name === activeItem"
      >
        <v-list-item-content>
          <v-list-item-icon>
            <v-icon>{{tool.icon}}</v-icon>
          </v-list-item-icon>
        </v-list-item-content>
      </v-list-item>
    </v-list-item-group>
  </v-list>
</template>

<script>
export default {
  name: "toolsMenu",
  props: {
    toolsMenu: Array,
    activeTool: String,
  },
  model: {
    prop: 'activeTool',
    event: 'setActiveTool',
  },
  computed: {
    activeItem: {
      get: function () { return this.activeTool },
      set: function (item) { this.$emit('setActiveTool', item) }
    },
  },
}
</script>

<style scoped>

</style>