<template>
  <span>Tooltip3 {{ id }} {{ fc }} </span>
</template>

<script>
  export default {
    name: 'EditorPreview',
    props: {
      id:        { type: Number,   default: () => undefined, },
      funGetFC:  { type: Function, default: () => undefined, },
    },
    data: () => ({
      fc: undefined,
    }),

    mounted: async function() {
      let self = this;
      this.funGetFC(this.id, function(data){ self.fc = data; });
    },

      // this.funGetFC(this.id, function(data){ console.log(2222, data); });
      //   .then(function(data){
      //     console.log('Preview_b', data)
      // });

    // async on_nav_preview(id)       {
    //   console.log(1111, id)
    //   let self = this;
    //   let ret  = undefined;
    //   await this.on_nav(id, function(data){ console.log(2222, data); ret = data; })
    //   return ret;
    // },

    // watch: {
    //   funGetFC: function(val){
    //     console.log('Preview_b', val)
    //   }
    // },
  }
</script>

<style scoped lang="scss">

</style>
