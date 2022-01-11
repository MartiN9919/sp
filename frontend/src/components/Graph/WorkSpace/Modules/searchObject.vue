<template>
  <v-toolbar dense absolute max-width="40%" style="right: 0" v-click-outside="deactivate" @click.right.stop="">
    <v-scroll-x-transition>
      <v-autocomplete
          v-if="showInputForm"
          v-model="selectedObject"
          @input="select"
          :items="objects"
          item-text="object.title"
          item-value="id"
          item-color="teal"
          hide-details
          attach=""
          dense
          flat
          clearable
          color="teal"
          autocomplete="off"
          append-icon=""
          class="search"
      ></v-autocomplete>
    </v-scroll-x-transition>
    <v-btn icon @click.stop="activate">
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