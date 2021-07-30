<template>
  <div>
  <v-btn @click="tt1">111</v-btn>
  <v-btn @click="tt2">222</v-btn>
  <v-btn @click="tt3">333</v-btn>
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
  </div>
</template>

<script>

export default {
  name: 'PaneTree',
  model: { prop: 'item_sel_prop', event: 'item_sel_change', },
  props: {
    items: Array,
    item_sel_prop: Number,
  },

  watch: {
    // при внешнем изменении model
    item_sel_prop: function(val) {
      console.log(111, val)
    },
  },

  mounted() {
    // this.model = this.item_sel_prop;
  },

  computed: {
    item_sel: {
      get() {
        console.log('item_sel get', this.item_sel_prop);
        return this.item_sel_prop;
      },
      // при внутреннем изменении model
      set(val) {
        console.log('item_sel set', val)
        this.$emit('item_sel_change', val);
        // this.model = val;
      },
    },
  },

  methods: {
    tt1() {
      console.log(1, this.model, this.item_sel)
    },
    tt2() {
      this.item_sel = 9;
    },
    tt3() {
      this.item_sel = 10;
    },
    getIcon(item, open) {
      if (!item.children) return 'mdi-vector-polygon'
      if (open)           return this.$CONST.TREE.ICON_FOLDER_OPEN
      return this.$CONST.TREE.ICON_FOLDER_CLOSE
    },

    getColor(item) {
      return (item.id == this.item_sel) ? this.$CONST.TREE.COLOR_SELECT : this.$CONST.TREE.COLOR_DEFAULT;
    },
  },
}
</script>
