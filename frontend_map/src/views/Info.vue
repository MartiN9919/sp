<template>
  <LeafletEditor
    v-model="fc_edit"
  />
</template>

<script>
//     @ok="on_edit_ok"


import LeafletEditor from '@/components/Map/Leaflet/LeafletEditor'

export default {
  name: 'Doc',
  components: { LeafletEditor },
  data() {
    return {
      fc_edit: undefined,
    }
  },
}
</script>
