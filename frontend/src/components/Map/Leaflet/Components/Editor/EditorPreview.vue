<template>
  <div>
    <span v-if="(title!=undefined)">{{ title }}</span>
    <LeafletViewer
      v-if="is_viewer() && (fc != undefined)"
      style="width: 10vh; height: 10vh; margin-left: auto; margin-right: auto;"
      :fc="fc"
      :controls="false"
    />
  </div>
</template>

<script>
  import LeafletViewer from "@/components/Map/Leaflet/LeafletViewer"
  import { str_copy_deep } from "@/components/Map/Leaflet/Lib/Lib"
  export default {
    name: 'EditorPreview',
    components: { LeafletViewer },
    props: {
      id:        { type: Number,   default: () => undefined, },
      name:      { type: String,   default: () => undefined, },
      funGetFC:  { type: Function, default: () => undefined, },
    },
    data: () => ({
      title: undefined,
      fc:    undefined,
    }),

    mounted: function() {
      let self = this;
      this.funGetFC(this.id, function(data){
        self.fc    = data;
        self.title = undefined;

        if (data?.features?.length == 0)           { self.title = str_copy_deep(self.name); return; }
        if (JSON.stringify(data)?.length > 100000) { self.title = 'Большой объект';         return; }
      });
    },

    methods: {
      is_viewer() {
        if (
          (this?.fc?.features == undefined) ||
          (this.fc.features.length == 0)
        ) return false;
        let s = JSON.stringify(this.fc);
        return ((s != undefined) && (s?.length < 10000000))
      },
    },

  }
</script>

<style scoped lang="scss">

</style>
