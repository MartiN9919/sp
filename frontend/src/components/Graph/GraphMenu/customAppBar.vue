<template>
  <v-row no-gutters class="flex-nowrap justify-space-between custom-app-bar">
    <v-card @click="scrollTabs('left')" class="right-board-card"
            width="fit-content" color="#00796B" dark flat rounded="0">
      <v-card-actions><v-icon>mdi-arrow-left</v-icon></v-card-actions>
    </v-card>
    <v-row no-gutters class="overflow-x-auto flex-nowrap tabs-row" id="row-tabs">
      <v-card
        v-for="object in workPlace" :key="object.tempId"
        @click="checkForActive(object) ? activateTab(null) : activateTab(object.tempId)"
        @contextmenu.stop="contextMenu = { event: $event, typeMenu: object.tempId }"
        dark flat rounded="0" min-width="fit-content" width="100%"
        :class="checkForActive(object) ? 'active-custom-tab' : 'custom-tab'"
      >
        <v-card-actions class="px-4 py-2 single-tab text-uppercase justify-center">
          <v-icon left size="20" :color="checkForActive(object) ? '#00796B' : 'white'">
            {{ primaryObject(object.object_id).icon }}
          </v-icon>
          {{ primaryObject(object.object_id).title_single }}
        </v-card-actions>
      </v-card>
    </v-row>
    <v-card @click="scrollTabs('right')" class="left-board-card"
            width="fit-content" color="#00796B" dark flat rounded="0">
      <v-card-actions><v-icon>mdi-arrow-right</v-icon></v-card-actions>
    </v-card>
    <context-menu v-if="contextMenu.typeMenu === typeContextMenu">
      <v-card>
        <context-tab :activatedObject="!!activeObject.rec_id" @selectMenuItem="selectMenuItem"></context-tab>
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
    windows: {
      2: 'createObject',
      3: 'searchTree',
    }
  }),
  computed: {
    ...mapGetters(['primaryObject', 'activeObject', ])
  },
  methods: {
    ...mapActions(['removeObjectInWorkArea', ]),
    checkForActive (object) {
      return this.activeTab === object.tempId
    },
    activateTab (position) { this.$emit('activateTab', position) },
    scrollTabs(direction) {
      if (direction === 'left') document.getElementById('row-tabs').scrollLeft -= 80
      else document.getElementById('row-tabs').scrollLeft += 80
    },
    selectMenuItem (item) {
      if (item.id === 0) {
        this.removeObjectInWorkArea(this.contextMenu.typeMenu)
      }
      if (item.id === 2 || item.id === 3) {
        let findObject = this.workPlace.find(object => object.tempId === this.contextMenu.typeMenu)
        findObject.activeWindow = this.windows[item.id]
        this.activateTab(findObject.tempId)
        this.$emit('selectMenuItem', {window: this.windows[item.id], object: findObject})
      }
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
  height: 0px;
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
  background-color: #00796B;
}

.active-custom-tab {
  background-color: white;
  color: #00796B;
}

.custom-tab {
  background-color: #00796B;
  color: white;
}

.custom-app-bar {
  border-top-style: solid;
  border-top-color:#FFFFFF;
  border-top-width: 1px;
}
</style>