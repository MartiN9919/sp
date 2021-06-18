<template>
  <v-row no-gutters class="flex-nowrap justify-space-between tabs-row">
    <v-card @click="scrollTabs('left')" width="fit-content" color="#00897B" dark flat rounded="0">
      <v-card-actions><v-icon>mdi-arrow-left</v-icon></v-card-actions>
    </v-card>
    <v-row no-gutters class="overflow-x-auto flex-nowrap" id="row-tabs">
      <v-card
        v-for="(object, key) in workPlace" :key="key"
        :color="activeTab === key ? '#004D40' : '#00897B'"
        @click="activeTab === key ? activateTab(null) : activateTab(key)"
        dark flat rounded="0" min-width="fit-content"
      >
        <v-card-actions class="px-4 py-2 single-tab text-uppercase">
          <v-icon left size="20">{{ titleObject(object.objectId).icon }}</v-icon>
          {{ titleObject(object.objectId).title }}
        </v-card-actions>
      </v-card>
    </v-row>
    <v-card @click="scrollTabs('right')" width="fit-content" color="#00897B" dark flat rounded="0">
      <v-card-actions><v-icon>mdi-arrow-right</v-icon></v-card-actions>
    </v-card>
  </v-row>
</template>

<script>
import ObjectFinder from "./Mixins/ObjectFinder";

export default {
  name: "customAppBar",
  mixins: [ ObjectFinder, ],
  props: {
    workPlace: { type: Array, default: [], },
    activeTab: { type: Number, default: null, },
  },
  model: { prop: 'activeTab', event: 'activateTab', },
  methods: {
    activateTab (position) { this.$emit('activateTab', position) },
    scrollTabs(direction) {
      if (direction === 'left') document.getElementById('row-tabs').scrollLeft -= 80
      else document.getElementById('row-tabs').scrollLeft += 80
    },
  },
}
</script>

<style scoped>
.single-tab {
  letter-spacing: 0.1em;
}

::-webkit-scrollbar {
  height: 0;
}

.tabs-row {
  background-color: #00897B;
}
</style>