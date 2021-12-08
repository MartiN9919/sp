<template>
  <div>
    <span>Tooltip3 {{ id }} </span>
    <LeafletViewer
      v-if="(fc!=undefined)"
      class="dd"
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
      funGetFC:  { type: Function, default: () => undefined, },
    },
    data: () => ({
      fc: undefined,
    }),

    mounted: function() {
      let self = this;
      this.funGetFC(this.id, function(data){
        console.log(data)
        self.fc = data;
      });
    },

  }
</script>

<style scoped lang="scss">

</style>
