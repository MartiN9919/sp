<template>
  <EditorNavObj
    v-bind="$attrs"
    :selReset="selReset"
    @selectedGeometry="selected_geometry"
  />

</template>

<script>
import EditorNavObj from '@/components/Map/Leaflet/Components/EditorNavObj';
import EditorNavOsm from '@/components/Map/Leaflet/Components/EditorNavOsm';

export default {
  name: 'EditorNav',
  components: { EditorNavObj, EditorNavOsm, },
  inheritAttrs: false,

}


</script>