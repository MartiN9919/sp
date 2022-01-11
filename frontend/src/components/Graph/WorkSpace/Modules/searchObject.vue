<template>
  <v-toolbar dense absolute max-width="40%" style="right: 0" v-click-outside="deactivate" @click.right.stop="">
    <v-scroll-x-transition>
      <v-autocomplete
        v-if="showInputForm"
        v-model="selectedObject"
        @input="select"
        :items="sortedObjects"
        item-text="object.title"
        no-data-text="На графе нет объектов"
        item-value="id"
        item-color="teal"
        hide-details
        attach=""
        dense
        flat
        color="teal"
        autocomplete="off"
        append-icon=""
        class="search"
      ></v-autocomplete>
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
    objects: Array,
  },
  data: () => ({
    selectedObject: null,
    showInputForm: false
  }),
  computed: {
    sortedObjects: function () {
      return this.objects.sort((a, b) => {
        let fa = a.object.title.toLowerCase()
        let fb = b.object.title.toLowerCase()
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
        this.$emit('findNode', this.objects.find(o => o.id === id))
        this.selectedObject = null
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
</style>