<template>
  <v-container class="pt-0 select_off" fluid>
    <v-tabs v-model="activeTab" color="teal" show-arrows="always" align-with-title>
      <v-tab v-for="(object, key) in workPlace" :key="key">{{ titleObject(object.objectId).title }}</v-tab>
    </v-tabs>
    <v-tabs-items v-model="activeTab">
      <v-tab-item v-for="(object, key) in workPlace" :key="key">
        <search-list></search-list>
<!--      <v-card flat>-->
<!--        <v-card-title><block-header :text-header="object.objectName" class="pb-3"></block-header></v-card-title>-->
<!--        <settingsAnalytics-->
<!--            v-for="classifier in object.classifiers"-->
<!--            :variable="classifier"-->
<!--            :key="classifier.id"-->
<!--        ></settingsAnalytics>-->

<!--        <div class="text-center pt-2">-->
<!--          <v-btn-->
<!--              outlined color="teal" class="mx-2 mb-2"-->
<!--          >Выполнить</v-btn>-->
<!--          <v-btn-->
<!--              outlined color="teal" class="mx-2 mb-2"-->
<!--          >Отключить</v-btn>-->
<!--        </div>-->
<!--        <right-click-menu-->
<!--            v-if="showRightClickMenu"-->
<!--            v-model="menuSettings.showRightClickMenu"-->
<!--            :menuSettings="menuWatcher"-->
<!--            @selectedItem="menuSettings.classifier.bodyRightClickMenu[0].items.push({-->
<!--              id: $event.id,-->
<!--              title: $event.title,-->
<!--            })"-->
<!--        ></right-click-menu>-->
<!--      </v-card>-->
      </v-tab-item>
    </v-tabs-items>
  </v-container>
</template>

<script>
import {mapGetters} from "vuex";
import settingsAnalytics from '../NavigationDrawer/ConstructorBlocks/settingsAnalytics'
import searchList from "../NavigationDrawer/ConstructorBlocks/BlocksForEnteringValues/searchList";
import blockHeader from "../NavigationDrawer/ConstructorBlocks/blockHeader";
import rightClickMenu from "./rightClickMenu";

export default {
  name: "graphMenu",
  components: { settingsAnalytics, blockHeader, rightClickMenu, searchList, },
  computed: {
    ...mapGetters(['classifiers', 'workPlace', 'listObjects', ]),
  },
  data: () => ({
    activeTab: null,
    menuWatcher: null,
    showRightClickMenu: false,
    classifier: {
      xRightClickMenuPosition: 0,
      yRightClickMenuPosition: 0,
      bodyRightClickMenu: [
        {
          title: 'Добавить классификатор',
          icon: 'mdi-database-plus',
          items: [],
        },
      ],
    },
    windowSize: {
      x: 0,
      y: 0,
    },
  }),
  mounted () {
    this.onResize()
  },
  methods: {
    onResize () {
      this.windowSize = { x: window.innerWidth, y: window.innerHeight }
      console.log(this.windowSize)
    },
    titleObject (objectId) {
      return this.listObjects.find(object => object.id === objectId)
    },
    activateRightClickMenu (menu, e) {
      e.preventDefault()
      this.menuWatcher = menu
      this.showRightClickMenu = false
      menu.xRightClickMenuPosition = e.clientX
      menu.yRightClickMenuPosition = e.clientY
      this.$nextTick(() => {
        this.showRightClickMenu = true
      })
    },
  },
}
</script>

<style scoped>

</style>