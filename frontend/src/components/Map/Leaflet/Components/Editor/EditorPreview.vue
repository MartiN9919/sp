<template>
  <div v-if="is_show()">
    <LeafletViewer
      style="width: 10vh; height: 10vh;"
      :fc_parent_prop="fc"
      :dop_controls="false"
    />
  </div>
</template>

<script>
  import LeafletViewer from "@/components/Map/Leaflet/LeafletViewer"
  export default {
    name: 'EditorPreview',
    components: { LeafletViewer },
    props: {
      id:        { type: Number,   default: () => undefined, },
      funGetFC:  { type: Function, default: () => undefined, },
    },
    data: () => ({
      fc: undefined,
    }),

    mounted: function() {
      let self = this;
      this.funGetFC(this.id, function(data){ self.fc = data; });
    },

    methods: {
      is_show() {
        if (this == undefined) return false;
        if (this.fc == undefined) return false;
        let s = JSON.stringify(this.fc);
        if (s == undefined) return false;
        return (s.length<1000)
      },
    },

  }
</script>

<style scoped lang="scss">

</style>
