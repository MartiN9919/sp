<template>
  <div>
  1321
  <v-btn @click="dd">1</v-btn>
  </div>
</template>

<script>
export default {
  name: 'editor-nav-osm',
  props: {
    options2: Object,
    showSel: { type: Boolean, default: () => true, },
  },
  //emits: ['selectedGeometry', 'update:showSel'],

  methods: {
    dd() {
      console.log(555, this.options2)
      this.$emit('update:options2', {dat1: 5})
      //this.$emit('selectedGeometry', '111111');
      this.$emit('update:showSel', false)
    },
  },
}
</script>
