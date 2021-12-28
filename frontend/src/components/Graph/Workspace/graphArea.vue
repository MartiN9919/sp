<template>
  <div class="h-100 disable-optimize" @click="clearSelectors" @click.right.prevent="menuShow" >
    <screen id="screen" ref="screen">
      <graph-relation
        v-for="relation in graphRelations"
        :key="relation.id"
        :relation="relation"
        :objects="graphObjects"
      />
      <graph-object
        v-for="object in graphObjects"
        :key="object.id"
        v-if="object.object.show"
        :object="object"
        :choosing="choosingObjects.includes(object.id)"
        @setChoosingObject="setChoosingObject"
        @setRelatedObjects="setRelatedObjects"
        @selectObject="selectObject"
      />
      <group
        v-if="relatedObjects.length"
        :nodes="relatedObjects"
        @click.native.stop=""
      />
    </screen>
    <context-menu-nested ref="contextMenu" :form="this" :items="contextMenu" :color="$CONST.APP.COLOR_OBJ"/>
  </div>
</template>

<script>
import Screen from '@/components/Graph/lib/components/Screen'
import Group from '@/components/Graph/lib/components/Group'
import GraphObject from "@/components/Graph/Workspace/graphObject"
import GraphRelation from "@/components/Graph/Workspace/graphRelation"
const ContextMenuNested = () => import("@/components/WebsiteShell/UIMainComponents/contextMenuNested")
import bodyContextMenu from "@/components/Graph/Workspace/bodyContextMenu"
import {mapActions, mapGetters} from "vuex"

export default {
  name: "graphArea",
  mixins: [bodyContextMenu],
  components: {GraphRelation, GraphObject, Screen, Group, ContextMenuNested},
  data: () => ({
    choosingObjects: [],
    relatedObjects: [],
  }),
  computed: mapGetters(['graphObjects', 'graphRelations']),
  methods: {
    ...mapActions(['setScreen']),
    setChoosingObject(id) {
      const positionObject = this.choosingObjects.findIndex(objectId => objectId === id)
      if (positionObject === -1)
        this.choosingObjects.push(id)
      else this.choosingObjects.splice(positionObject, 1)
    },
    setRelatedObjects(object) {
      this.relatedObjects = [object]
      let relations = this.graphRelations.filter(relation => relation.to === object.id || relation.from === object.id)
      for (let relation of relations) {
        let relatedObject = this.graphObjects.find(n => (n.id === relation.to || n.id === relation.from) && n.id !== object.id)
        this.relatedObjects.push(relatedObject)
        this.selectObject(relatedObject)
      }
    },
    clearSelectors() {
      this.choosingObjects = []
      this.relatedObjects = []
    },
    selectObject(object) {
      this.graphObjects.splice(this.graphObjects.findIndex(o => o === object), 1)
      this.graphObjects.push(object)
    },
    menuShow(event, object=null) {
      this.objectWithActivatedMenu = object
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