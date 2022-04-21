<template>
  <div v-if="line.length" class="pr-4 h-100 overflow-y-auto overflow-x-hidden timeline">
    <v-timeline dense align-top>
      <time-line-point
          v-for="(point, key) in line"
          :key="key"
          :point="point"
          @contextmenu.native="show($event, point)"
      ></time-line-point>
    </v-timeline>
    <v-menu v-model="showMenu" :position-x="x" :position-y="y" absolute offset-y max-width="min-content">
      <v-card>
        <v-card-title class="text-no-wrap">Переключиться на данную позицию?</v-card-title>
        <v-card-subtitle>При согласии, все последующие этапы вашей работы будут стерты.</v-card-subtitle>
        <v-divider></v-divider>
        <v-card-actions class="justify-space-between">
          <v-btn @click="checkIn" text color="teal">Да</v-btn>
          <v-btn @click="closeMenu" text color="error">Нет</v-btn>
        </v-card-actions>
      </v-card>
    </v-menu>
  </div>
  <v-card flat v-else>
    <v-card-subtitle class="text-center text-no-wrap">
      Еще не было произведено никаких действий
    </v-card-subtitle>
  </v-card>
</template>

<script>
import {mapGetters} from "vuex";
import TimeLinePoint from "@/components/Graph/GraphMenu/Timeline/TimeLinePoint";

export default {
  name: "TimeLinePage",
  components: {TimeLinePoint},
  data: () => ({
    selectedPoint: null,
    showMenu: false,
    x: 0,
    y: 0,
  }),
  computed: {
    ...mapGetters(['timeline']),
    line: function () {
      return [...this.timeline].reverse()
    }
  },
  methods: {
    show(e, point) {
      e.preventDefault()
      this.closeMenu()
      this.x = e.clientX
      this.y = e.clientY
      this.$nextTick(() => {
        this.showMenu = true
        this.selectedPoint = point
      })
    },
    closeMenu() {
      this.showMenu = false
      this.selectedPoint = null
    },
    checkIn() {
      this.$store.dispatch('goToTimeline', this.selectedPoint)
    }
  }
}
</script>

<style scoped>
.timeline {
  margin-left: -16px;
  min-width: 200px;
}
</style>