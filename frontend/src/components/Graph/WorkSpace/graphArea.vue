<template>
  <div class="h-100 disable-optimize" @click.shift="clearSelectors" @click.right.prevent="menuShow">
    <screen id="screen" ref="screen" @selectNodes="setChoosingObjects">
      <graph-relation
        v-for="relation in graphRelations"
        :key="relation.id"
        v-if="globalDisplaySettingValue('showRelations')"
        :relation="relation"
        :objects="graphObjects"
        @ctxMenu="menuShow(...$event)"
      />
      <graph-object
        v-for="object in graphObjects"
        :key="object.id"
        v-if="object.object.show"
        :object="object"
        :in-selected="inSelectedGraphObject(object)"
        :selected-objects="selectedGraphObjects"
        @setChoosingObject="setChoosingObject"
        @setRelatedObjects="setRelatedObjects"
        @selectObject="selectObject"
        @ctxMenu="menuShow(...$event)"
      />

    </screen>
    <search-object v-if="graphObjects.length" :objects="graphObjects" @findNode="findNode"/>
    <context-menu-nested ref="contextMenu" :form="this" :items="contextMenu" :color="$CONST.APP.COLOR_OBJ"/>
  </div>
</template>

<script>
import Screen from '@/components/Graph/WorkSpace/lib/components/Screen'
import GraphObject from "@/components/Graph/WorkSpace/graphObject"
import GraphRelation from "@/components/Graph/WorkSpace/graphRelation"
import bodyContextMenu from "@/components/Graph/WorkSpace/Modules/bodyContextMenu"
import SearchObject from "@/components/Graph/WorkSpace/Modules/searchObject"
const ContextMenuNested = () => import("@/components/WebsiteShell/UIMainComponents/contextMenuNested")
import {mapActions, mapGetters} from "vuex"

export default {
  name: "graphArea",
  mixins: [bodyContextMenu],
  components: {SearchObject, GraphRelation, GraphObject, Screen, ContextMenuNested},
  data: () => ({
    relatedObjects: [],
  }),
  computed: {
    ...mapGetters([
      'graphObjects',
      'graphRelations',
      'selectedGraphObjects',
      'inSelectedGraphObject',
      'globalDisplaySettingValue',
    ]),
  },
  methods: {
    ...mapActions([
      'setScreen',
      'addSelectedGraphObject',
      'deleteSelectedGraphObject',
      'clearSelectedGraphObjects'
    ]),
    findNode(node) {
      this.$refs.screen.zoomNodes([node], { scale: 1.5 })
    },
    setRelatedObjects(object) {
      this.addSelectedGraphObject(object)
      let relations = this.graphRelations.filter(relation => relation.to === object.id || relation.from === object.id)
      for (let relation of relations) {
        const relatedObject = this.graphObjects.find(n => (n.id === relation.to || n.id === relation.from) && n.id !== object.id)
        this.addSelectedGraphObject(relatedObject)
        this.selectObject(relatedObject)
      }
    },
    setChoosingObject(object) {
      if(this.inSelectedGraphObject(object))
        this.deleteSelectedGraphObject(object)
      else
        this.addSelectedGraphObject(object)
    },
    setChoosingObjects(frame) {
      const xMax = frame.x + frame.width
      const yMax = frame.y + frame.height
      for(const object of this.graphObjects){
        const x = object.x + object.size / 6
        const y = object.y + object.size / 6
        if(x > frame.x && x < xMax && y > frame.y && y < yMax){
          if(!this.inSelectedGraphObject(object))
            this.addSelectedGraphObject(object)
        }
      }
    },
    clearSelectors() {
      this.clearSelectedGraphObjects()
      this.relatedObjects = []
    },
    selectObject(object) {
      this.graphObjects.splice(this.graphObjects.findIndex(o => o === object), 1)
      this.graphObjects.push(object)
    },
    menuShow(event, object=null) {
      this.objectCtxMenu = object
      this.$refs.contextMenu.show_root(event.x, event.y)
    },
  },
  mounted() {
    this.setScreen(this.$refs.screen)
  }
}
</script>

<style scoped>
.disable-optimize {
  will-change: transform;
}
</style>