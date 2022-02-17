<script>
import ctxMenu from "@/components/Graph/WorkSpace/Modules/ctxMenu"
import {mapActions} from "vuex"

export default {
  name: "bodyContextMenu",
  data: () => ({
    objectCtxMenu: null,
  }),
  computed: {
    findRelationsStatus: function(){
      return this.selectedNodes.length === 2
    },
    relationCreateStatus: function(){
      return this.selectedNodes.length === 3
        && this.selectedNodes.find(o => o.ids.object_id === 20)
        || this.findRelationsStatus
    },
    relationTooltip: {
      get: function () { return this.objectCtxMenu.settings.showTooltip },
      set: function () { this.objectCtxMenu.settings.showTooltip = !this.objectCtxMenu.settings.showTooltip }
    },
    relationCreateDate: {
      get: function () { return this.objectCtxMenu.settings.showCreateDate },
      set: function () { this.objectCtxMenu.settings.showCreateDate = !this.objectCtxMenu.settings.showCreateDate }
    },
    objectTitle: {
      get: function () { return this.objectCtxMenu.settings.showTitle },
      set: function () { this.objectCtxMenu.settings.showTitle = !this.objectCtxMenu.settings.showTitle }
    },
    objectTooltip: {
      get: function () { return this.objectCtxMenu.settings.showTooltip },
      set: function () { this.objectCtxMenu.settings.showTooltip = !this.objectCtxMenu.settings.showTooltip }
    },
    objectCreateDate: {
      get: function () { return this.objectCtxMenu.settings.showCreateDate },
      set: function () { this.objectCtxMenu.settings.showCreateDate = !this.objectCtxMenu.settings.showCreateDate }
    },
    objectTriggers: {
      get: function () { return this.objectCtxMenu.settings.showTriggers },
      set: function () { this.objectCtxMenu.settings.showTriggers = !this.objectCtxMenu.settings.showTriggers }
    },
    contextMenu: function () {
      if(this.objectCtxMenu) {
        if(this.isNode(this.objectCtxMenu)) {
          return ctxMenu.getObjectCtxMenu([20, 30].includes(this.objectCtxMenu.ids.object_id))
        } else {
          return ctxMenu.RelationCtxMenu
        }
      }
      else {
        return ctxMenu.getSpaceCtxMenu(
          this.graphNodes.length,
          this.graphNodes.length > 1,
          this.relationCreateStatus,
          this.findRelationsStatus,
          this.selectedNodes.length,
        )
      }
    }
  },
  methods: {
    ...mapActions(['reorderNodes', 'setEditableRelation', 'setNavigationDrawerStatus', 'setToolStatus', 'setActiveTool',
    'setEditableObject', 'deleteObjectFromGraph', 'setRootSearchRelationTreeItem', 'getRelationsBtwObjects',
    'addToGraph', 'executeMapScript', 'clearGraph']),
    menuShow(event, object=null) {
      this.objectCtxMenu = object
      this.$refs.contextMenu.show_root(event.x, event.y)
    },
    reorderChoosingNodes() {
      this.reorderNodes(this.selectedNodes)
    },
    setSearchRelation(event) {
      this.setRootSearchRelationTreeItem(this.objectCtxMenu)
      this.setNavigationDrawerStatus(true)
      this.setActiveTool('searchRelationPage')
    },
    setChangeObject(event) {
      this.setEditableObject({
        objectId: this.objectCtxMenu.ids.object_id,
        recId: this.objectCtxMenu.ids.rec_id
      })
    },
    deleteObjects() {
      for(let choosingObject of this.selectedNodes)
        this.deleteObjectFromGraph(choosingObject)
      this.clearSelectedGraphObjects()
    },
    deleteObject() {
      this.deleteSelectedGraphObject(this.objectCtxMenu)
      this.deleteObjectFromGraph(this.objectCtxMenu)
    },
    createRelation(){
      let relations = []
      if(this.objectCtxMenu && !this.isNode(this.objectCtxMenu)) {
         relations = [this.objectCtxMenu.entity.o1, this.objectCtxMenu.entity.o2]
      }
      else {
        if(this.selectedNodes.length === 2)
          relations = this.selectedNodes
        else
          relations = this.selectedNodes.filter(o => o.ids.object_id !== 20)
      }
      this.setEditableRelation({
        relations: relations,
        document: this.selectedNodes.length === 3
          ? this.selectedNodes.find(o => o.ids.object_id === 20)
          : null
      })
      this.setNavigationDrawerStatus(true)
      this.setActiveTool('createRelationPage')
    },
    findRelations(){
      this.getRelationsBtwObjects(this.selectedNodes)
    },
    addGeometryToGraph(){
      this.$router.push({name: 'Map'})
      this.executeMapScript({ request: {id: 1, name: "Вывод геометрии", variables: {
        geometry_object: {
          type: {title: "search", value: null}, value: {
            title: this.objectCtxMenu.entity.title,
            objectId: this.objectCtxMenu.ids.object_id,
            recId: this.objectCtxMenu.ids.rec_id}}}},
        config: {}
      })
    },
    saveGraphInFile() {
      let a = document.createElement("a")
      const data = Array.from(this.graphNodes, node => {
        return {
          props: {x: node.x, y: node.y, size: node.size},
          object_id: node.object.object.id,
          rec_id: node.object.recId
        }
      })
      let file = new Blob([JSON.stringify(data)], {type: 'text/plain'})
      a.href = URL.createObjectURL(file)
      a.download = new Date().getTime().toString() + '.json'
      a.click()
      a.remove()
    },
    getGraphFromFile() {
      this.clearGraph()
      const addObjectToGraph = this.addToGraph
      let obj = document.createElement('input')
      obj.style.cssText = 'display:none'
      obj.type = 'file'
      obj.accept='.json'

      let input  = document.getElementById("app").appendChild(obj)
      input.click()
      const parseText = function (text) {
        addObjectToGraph({payload: JSON.parse(text), noMove: true})
      }
      input.addEventListener('change', function() {
        input.files[0].text()
        .then(text => { parseText(text) })
      })
      obj.remove()
    },
  },
}
</script>

