<template>
  <div>
    <span v-if="(title!=undefined)">{{ title }}</span>
    <LeafletViewer
      v-if="is_viewer"
      style="width: 10vh; height: 10vh; margin-left: auto; margin-right: auto;"
      :fc="fc"
      :controls="false"
    />
  </div>
</template>

<script>
  import { MAP_CONST }     from '@/components/Map/Leaflet/Lib/Const'
  import { str_copy_deep } from '@/components/Map/Leaflet/Lib/Lib'
  import LeafletViewer     from '@/components/Map/Leaflet/LeafletViewer'
  export default {
    name: 'EditorPreview',
    components: { LeafletViewer },
    props: {
      id:        { type: Number,   default: () => undefined, },
      name:      { type: String,   default: () => undefined, },
      funGetFC:  { type: Function, default: () => undefined, },
    },
    data: () => ({
      title:     undefined,
      fc:        undefined,
      is_viewer: false,
    }),

    mounted: function() {
      // запросить данные
      if ((this.id != undefined) && (this.funGetFC != undefined)) {
        let self = this;
        this.funGetFC(this.id, function(data){
          self.title     = undefined;
          self.fc        = data;
          self.is_viewer = (data?.features?.length > 0);
          if (!self.is_viewer)                                        { self.title = str_copy_deep(self.name); return; }
          if (JSON.stringify(data)?.length >= MAP_CONST.GEOMETRY.BIG) { self.title = 'Большой объект';         return; }
        });
      // иначе только имя
      } else {
        this.title = str_copy_deep(this.name);
      };
    },
  }
</script>

<style scoped lang="scss">

</style>
