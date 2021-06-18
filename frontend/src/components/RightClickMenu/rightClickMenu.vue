<template>
  <v-menu
    v-model="show"
    :position-x="positionsRightClickMenu.xRightClickMenuPosition"
    :position-y="positionsRightClickMenu.yRightClickMenuPosition"
    :close-on-content-click="false"
    min-width="20%" max-width="20%" max-height="50%"
    absolute offset-y no-action z-index="10001"
  >
    <v-window v-model="stepWindowStyle">
      <v-window-item v-for="window in bodyRightClickMenu" :key="window.type" :value="window.type"> <!-- transition="" reverse-transition="" -->
        <v-card v-if="window.type.startsWith('actions')" >
          <v-card-title v-if="'title' in window" class="pa-0 justify-center">{{window.title}}</v-card-title>
          <v-divider v-if="'title' in window"></v-divider>
          <v-card-text class="pa-0">
            <v-list rounded max-height="50%">
              <v-list-item
                  v-for="(item, key) in window.body" :key="key" link
                  v-if="item.type === 'action'"
                  @click="'next' in item ? stepNextWindow(item) : selectListItem(item)"
              >
                <v-list-item-title>{{item.title}}</v-list-item-title>
                <v-list-item-icon v-if="item.icon"><v-icon right>{{item.icon}}</v-icon></v-list-item-icon>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
        <v-card v-if="window.type.startsWith('lists')" >
          <v-card-title v-if="'title' in window" class="pa-0 justify-center">{{window.title}}</v-card-title>
          <v-divider v-if="'title' in window"></v-divider>
          <v-card-text v-for="(item, key) in window.body" :key="key">
            <v-autocomplete
              v-if="item.type === 'list'" color="teal"
              :items="item.list" item-text="title"
              @change="changeObject(window, $event)"
              return-object
            >
              <template v-slot:append-outer>
                <v-btn
                  icon v-if="'next' in item" @click="stepNextWindow(item)"
                  :disabled="!(window.type in listSelectedObjects)"
                ><v-icon>mdi-arrow-right</v-icon></v-btn>
                <v-btn icon v-else @click="confirmFillingSelectors()"><v-icon>mdi-check</v-icon></v-btn>
              </template>
              <template v-slot:prepend>
                <v-btn icon v-if="listSteps.length > 0" @click="stepBackWindow()"><v-icon>mdi-arrow-left</v-icon></v-btn>
              </template>
            </v-autocomplete>

          </v-card-text>
        </v-card>
      </v-window-item>
    </v-window>
  </v-menu>
</template>

<script>
import {mapActions, mapGetters} from "vuex";

export default {
  name: "rightClickMenu",
  data: () => ({
    stepWindowStyle: '',
    listSteps: [],
    listSelectedObjects: {},
  }),
  computed: {
    ...mapGetters(['showRightClickMenu', 'positionsRightClickMenu', 'bodyRightClickMenu', ]),
    show: {
      get: function () { return this.showRightClickMenu },
      set: function (val) { this.deactivateRightClickMenu() }
    },
  },
  methods: {
    ...mapActions(['deactivateRightClickMenu', ]),
    confirmFillingSelectors () {
      this.$emit('confirmFillingSelectors', this.listSelectedObjects)
      this.closeMenu()
    },
    changeObject(item, object) {
      this.listSelectedObjects[item.type] = object
      this.$emit('changeObject', { window: item, selected: this.listSelectedObjects[item.type] })
    },
    stepBackWindow() {
      this.listSteps.pop()
      this.stepWindowStyle = this.listSteps[this.listSteps.length - 1]
    },
    stepNextWindow(item) {
      this.stepWindowStyle = item.next
      this.listSteps.push(item.next)
    },
    selectListItem(item) {
      this.$emit('selectListItem', item)
      this.closeMenu()
    },
    closeMenu() {
      this.show=false
      this.stepWindowStyle = this.bodyRightClickMenu[0].type
      this.listSteps = [this.bodyRightClickMenu[0].type]
      this.listSelectedObjects = {}
    }
  },
  created() {
    this.stepWindowStyle = this.bodyRightClickMenu[0].type
    this.listSteps = [this.bodyRightClickMenu[0].type]
  }
}
</script>

<style scoped>

</style>