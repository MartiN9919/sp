<template>
  <div>
    <span v-if="!is_show()">{{ name }}</span>
    <LeafletViewer
      v-if="is_show()"
      style="width: 20vh; height: 20vh;"
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
      name:      { type: String,   default: () => undefined, },
      funGetFC:  { type: Function, default: () => undefined, },
    },
    data: () => ({
      fc: undefined,
    }),

    mounted: function() {
      let self = this;
      this.funGetFC(this.id, function(data){ self.fc = data; console.log(data); });
    },

    methods: {
      is_show() {
        if (
          (this?.fc?.features == undefined) ||
          (this.fc.features.length == 0)
        ) return false;
        let s = JSON.stringify(this.fc);
        if (s == undefined) return false;
        return (s.length<1000)
      },
    },

  }
</script>

<style scoped lang="scss">

</style>
