<template>
  <v-treeview
    :items="items"
    hoverable
    activatable
    transition
    dense
    open-on-click
    return-object
  >
    <template v-slot:prepend="{ item, open }">
      <v-icon
        :id="item.id"
        :size="$CONST.TREE.ICON_SIZE"
        :color="getColor(item)"
      >
        {{ getIcon(item, open) }}
      </v-icon>
    </template>
    <template v-slot:label="{ item, open }">
      <div
        class="v-treeview-node__label"
        :style="{'color': getColor(item)}"
      >
        {{ item.name }}
      </div>
    </template>
  </v-treeview>
</template>

<script>

export default {
  name: 'PaneTree',
  props: {
    items: Array,
    idSelect: Number,
  },
  methods: {
    getIcon(item, open) {
      if (!item.children) return 'mdi-vector-polygon'
      if (open)           return this.$CONST.TREE.ICON_FOLDER_OPEN
      return this.$CONST.TREE.ICON_FOLDER_CLOSE
    },

    getColor(item) {
      return (item.id == this.idSelect) ? this.$CONST.TREE.COLOR_SELECT : this.$CONST.TREE.COLOR_DEFAULT;
    },
  },
}
</script>
