<template>
  <span>Tooltip3 {{ id }} {{ fcPreview }}</span>
</template>

<script>
  export default {
    name: 'EditorPreview',
    props: {
      id:        { type: Number,  default: () => undefined, },
      fcPreview: { type: Object,  default: () => undefined, },
    },
    emits: [
      'onNavPreview',
    ],

    mounted: function() {
      console.log('Preview_a', this.id)
      this.$emit('onNavPreview', this.id);
    },

    watch: {
      fcPreview: function(val){
        console.log('Preview_b', val)
      }
    },
  }
</script>

<style scoped lang="scss">

</style>
