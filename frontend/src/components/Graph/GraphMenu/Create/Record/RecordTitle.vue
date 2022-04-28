<template>
  <v-hover v-slot="{ hover }">
    <v-expansion-panel-header class="py-0 px-2 header select-off cursor-pointer" :color="colorHeader" expand-icon="">
      <template v-slot:actions="">
        <v-icon v-if="hover && opened" @click.stop="create" :color="colorIcon" tabindex="-1">mdi-plus</v-icon>
      </template>
      <template v-slot:default="">
        <span :class="colorText">{{ title }}</span>
      </template>
    </v-expansion-panel-header>
  </v-hover>
</template>

<script>
export default {
  name: "RecordTitle",
  props: {
    title: String,
    opened: Boolean,
  },
  computed: {
    colorHeader: function () {
      return this.opened ? '#bfbfbf' : '#f2f2f2'
    },
    colorIcon: function () {
      return this.opened ? 'white' : 'black'
    },
    colorText: function () {
      return this.opened ? 'dark' : 'light'
    }
  },
  methods: {
    create() {
      this.$emit('create')
    }
  }
}
</script>

<style scoped>
.dark {
  color: white;
}
.light {
  color: black;
}
.header:focus-visible {
  background-color: #7a7979 !important;
}
</style>