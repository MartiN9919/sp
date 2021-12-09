<template>
  <div>
    <span v-if="!is_show()">{{ name }}</span>
    <LeafletViewer
      v-if="is_show() && (fc != undefined)"
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
      name:      { type: String,   default: () => undefined, },
      funGetFC:  { type: Function, default: () => undefined, },
    },
    data: () => ({
      fc: undefined,
    }),

    mounted: function() {
      let self = this;
      //if (this.name.includes('', undefined)) this.name = 'Без названия'
      this.funGetFC(this.id, function(data){
        self.fc = data;
        console.log(1, data);
      });
    },

    methods: {
      is_show() {
        if (
          (this?.fc?.features == undefined) ||
          (this.fc.features.length == 0)
        ) return false;
        let s = JSON.stringify(this.fc);
        return ((s != undefined) && (s?.length < 10000))
      },
    },

  }
</script>

<style scoped lang="scss">

</style>
