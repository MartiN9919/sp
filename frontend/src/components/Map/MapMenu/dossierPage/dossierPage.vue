<template>
  <div>
    444
  <vue-pannellum
    :src="pannellumOptions()"
    :showFullscreen="true"
    :showZoomCtrl="false"
    :compass="true"
    style="height: 500px;">
  </vue-pannellum>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import VuePannellum from 'vue-pannellum'

export default {
  name:       "map-dossier",
  components: { VuePannellum, },
  methods: {
    pannellumOptions() {
      //return '/static/test/bma-1.jpg'
      return {
        default: {
          firstScene: 'b1',
          //showFullscreenCtrl: true,
          showZoomCtrl:       false,
        },
        scenes: {
          b1: {
            hfov: 110,
            pitch: -3,
            yaw: 117,
            type: 'equirectangular',
            panorama: '/static/test/bma-1.jpg',
            hotSpots: [
              {
                "type": "scene",
                "text": "Сюда не ходи",
                "sceneId": "b2",
                "pitch": 14.1,
                "yaw": 1.5,
              },
              {
                "type": "scene",
                "text": "Дорога Минск-Москва",
                "sceneId": "b3",
                "pitch": -9.4,
                "yaw": 222.6,
              },
              {
                "type": "info",
                "text": "Иди туда",
                "pitch": -0.9,
                "yaw": 144.4,
              },
            ],
          },
          b2: {
            hfov: 110,
            yaw: 5,
            type: 'equirectangular',
            panorama: '/static/test/bma-2.jpg',
            hotSpots: [
              {
                "type": "scene",
                "text": "Иди туда",
                "sceneId": "b3",
                "pitch": -0.9,
                "yaw": 144.4,
              },
            ],
          },
          b3: {
            hfov: 110,
            yaw: 5,
            type: 'equirectangular',
            panorama: '/static/test/bma-3.jpg',
            hotSpots: [
              {
                "type": "scene",
                "text": "Иди туда",
                "sceneId": "b2",
                "pitch": -0.9,
                "yaw": 144.4,
              },
            ],
          },
        },
      }
    }
  },
}
</script>

<style scoped>
</style>