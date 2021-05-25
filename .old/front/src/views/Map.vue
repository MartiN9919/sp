<template>
  <div class="map" style="height: 100%; width: 100%">
    <Leaflet></Leaflet>
  </div>
</template>

<script>
import Leaflet from '@/components/Leaflet/Leaflet.vue'

export default {
  name: 'Map',
  components: {
    Leaflet,
  }
}
</script>
