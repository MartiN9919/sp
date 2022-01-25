<template>
  <div class="h-100 disable-optimize select-off" @mouseup.exact="clearSelectors" @contextmenu="menuShow">
    <screen id="screen" ref="screen" @selectNodes="setChoosingObjects" oncontextmenu="return false">
      <graph-relation
        v-for="relation in graphRelations"
        :key="relation.id"
        :in-hover="inHover(relation)"
        :relation="relation"
        :objects="graphObjects"
        @hover="hover"
        @unhover="unHover"
        @ctxMenu="menuShow(...$event)"
        @setChoosingRelated="setChoosingRelated"
      />
      <graph-object
        v-for="object in graphObjects"
        :key="object.id"
        v-if="object.object.show"
        :object="object"
        :in-selected="inSelectedGraphObject(object)"
        :in-hover="inHover(object)"
        :selected-objects="selectedGraphObjects"
        @setChoosingObject="setChoosingObject"
        @setChoosingRelated="setChoosingRelated"
        @hover="hover"
        @unhover="unHover"
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
    relationsObject: [],
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
    isObject(element) {
      return element.hasOwnProperty('object')
    },
    findNode(node) {
      this.$refs.screen.zoomNodes([node], { scale: 1.5 })
    },
    setChoosingRelated() {
      this.relatedObjects.map(o => this.addSelectedGraphObject(o))
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
    pickUp(element) {
      let ar = this.isObject(element) ? this.graphObjects : this.graphRelations
      ar.splice(ar.findIndex(r => r === element), 1)
      ar.push(element)
    },
    getRelatedForObject(object) {
      this.relatedObjects = [object]
      this.relationsObject = this.graphRelations.filter(r => [r.to, r.from].includes(object.id))
      for(const r of this.relationsObject) {
        const relatedObject = this.graphObjects.find(n => ([r.to, r.from].includes(n.id)) && n.id !== object.id)
        this.relatedObjects.push(relatedObject)
        this.pickUp(relatedObject)
      }
    },
    getRelatedForRelation(relation) {
      this.relationsObject = [relation]
      this.relatedObjects = Array.from(this.graphObjects.filter(o => [relation.from, relation.to].includes(o.id)))
      this.relatedObjects.map(o => this.pickUp(o))
    },
    hover(element) {
      this.pickUp(element)
      this.isObject(element) ? this.getRelatedForObject(element) : this.getRelatedForRelation(element)
    },
    unHover() {
      this.relatedObjects = []
      this.relationsObject = []
    },
    inHover(element) {
      return this.globalDisplaySettingValue('linkHighlighting')
        && this.isObject(element)
        ? this.relatedObjects.includes(element)
        : this.relationsObject.includes(element)
    },
    clearSelectors(evt) {
      if(!evt.button && !this.$refs.contextMenu.$children[0].isActive) {
        this.clearSelectedGraphObjects()
      }
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