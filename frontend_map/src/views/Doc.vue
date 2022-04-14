<template>
  <div>1111
  <LeafletEditor
    style="height: 70vh;"
    v-model="fc_edit"
    :modeEnabled="modeEnabled"
    :modeSelected="modeSelected"
  />
  </div>
</template>

<script>
//     @ok="on_edit_ok"


import LeafletEditor from '@/components/Map/Leaflet/LeafletEditor'

export default {
  name: 'Doc',
  components: { LeafletEditor },
  data() {
    return {
      fc_edit: { "type": "FeatureCollection", "features": []},
      modeEnabled: { marker: true , line: true, polygon: true, }, // доступные элементы
      modeSelected: null,
    }
  },
}
</script>
