<template>
  <v-row no-gutters class="flex-nowrap justify-space-between tabs-row">
    <v-card @click="scrollTabs('left')" class="right-board-card"
            width="fit-content" color="#00897B" dark flat rounded="0">
      <v-card-actions><v-icon>mdi-arrow-left</v-icon></v-card-actions>
    </v-card>
    <v-row no-gutters class="overflow-x-auto flex-nowrap" id="row-tabs">
      <v-card
        v-for="object in workPlace" :key="object.tempId"
        @click="activeTab === object.tempId ? activateTab(null) : activateTab(object.tempId)"
        @contextmenu.stop="contextMenu = { event: $event, typeMenu: object.tempId }"
        dark flat rounded="0" min-width="fit-content" width="100%"
        :color="activeTab === object.tempId ? '#004D40' : '#00897B'"
      >
        <v-card-actions class="px-4 py-2 single-tab text-uppercase justify-center">
          <v-icon left size="20">{{ objectTemplates(object.objectId).icon }}</v-icon>
          {{ objectTemplates(object.objectId).title_single }}
        </v-card-actions>
      </v-card>
    </v-row>
    <v-card @click="scrollTabs('right')" class="left-board-card"
            width="fit-content" color="#00897B" dark flat rounded="0">
      <v-card-actions><v-icon>mdi-arrow-right</v-icon></v-card-actions>
    </v-card>
    <context-menu v-if="contextMenu.typeMenu === typeContextMenu">
      <v-card>
        <context-tab @selectMenuItem="selectMenuItem"></context-tab>
      </v-card>
    </context-menu>
  </v-row>
</template>

<script>
import contextMenu from "../../WebsiteShell/ContextMenu/contextMenu"
import toolsContextMenu from "../../WebsiteShell/ContextMenu/Mixins/toolsContextMenu"
import contextTab from "../ContextMenus/contextTab"
import { mapActions, mapGetters } from "vuex"

export default {
  name: "customAppBar",
  mixins: [ toolsContextMenu, ],
  components: { contextMenu, contextTab, },
  props: {
    workPlace: { type: Array, default: [], },
    activeTab: { type: Number, default: null, },
  },
  model: { prop: 'activeTab', event: 'activateTab', },
  data: () => ({
    contextMenu: { event: null, typeMenu: null, },
  }),
  computed: {
    ...mapGetters(['objectTemplates', ])
  },
  methods: {
    ...mapActions(['removeObjectInWorkAreaAboveObjects', ]),
    activateTab (position) { this.$emit('activateTab', position) },
    scrollTabs(direction) {
      if (direction === 'left') document.getElementById('row-tabs').scrollLeft -= 80
      else document.getElementById('row-tabs').scrollLeft += 80
    },
    selectMenuItem (item) {
      if (item.id === 0) this.removeObjectInWorkAreaAboveObjects(this.contextMenu.typeMenu)
      this.deactivateContextMenu()
    }
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

.right-board-card {
  border-right-style: solid;
  border-right-color: white !important;
}

.left-board-card {
  border-left-style: solid;
  border-left-color: white !important;
}

.tabs-row {
  background-color: #00897B;
}
</style>