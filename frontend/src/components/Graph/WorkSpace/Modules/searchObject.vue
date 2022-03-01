<template>
  <v-toolbar dense absolute max-width="40%" style="right: 0" v-click-outside="deactivate" @click.right.stop="">
    <v-scroll-x-transition>
      <v-autocomplete
        v-if="showInputForm"
        v-model="selectedNode"
        @input="select"
        :items="sortedNodes"
        no-data-text="На графе нет объектов"
        item-value="id"
        item-color="teal"
        hide-details
        autofocus
        attach=""
        dense
        flat
        color="teal"
        autocomplete="off"
        append-icon=""
        class="search"
      >
        <template v-slot:item="{ item }">
          <v-icon left>{{item.entity.base.icon}}</v-icon>
          <v-list-item-title class="selector-item">{{item.entity.title}}</v-list-item-title>
        </template>
      </v-autocomplete>
    </v-scroll-x-transition>
    <v-btn v-if="!showInputForm" icon @click.stop="activate">
      <v-icon>mdi-magnify</v-icon>
    </v-btn>
  </v-toolbar>
</template>

<script>
export default {
  name: "searchObject",
  props: {
    nodes: Array,
  },
  data: () => ({
    selectedNode: null,
    showInputForm: false
  }),
  computed: {
    sortedNodes: function () {
      return this.nodes.sort((a, b) => {
        let fa = a.entity.title.toLowerCase()
        let fb = b.entity.title.toLowerCase()
        if (fa < fb) {
          return -1;
        }
        if (fa > fb) {
          return 1;
        }
        return 0;
      });
    }
  },
  methods: {
    activate() {
      this.showInputForm = true
    },
    deactivate() {
      this.showInputForm = false
    },
    select(id) {
      if(id) {
        this.$emit('findNode', this.nodes.find(o => o.id === id))
        this.selectedNode = null
        this.deactivate()
      }
    }
  }
}
</script>

<style scoped>
.search >>> .v-select__slot {
  cursor: pointer;
}
.search >>> .v-input__slot {
  cursor: pointer !important;
}
.search >>> input {
  padding: 0;
  cursor: pointer;
}
.selector-item {
  white-space: normal;
  width: 0;
}
</style>