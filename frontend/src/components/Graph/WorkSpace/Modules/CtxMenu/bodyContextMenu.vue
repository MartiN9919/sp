<script>
import ctxMenu from "@/components/Graph/WorkSpace/Modules/CtxMenu/ctxMenu"
import {mapActions} from "vuex"
import _ from 'lodash'

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
          return ctxMenu.getObjectCtxMenu([25, 30].includes(this.objectCtxMenu.ids.object_id))
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
    ...mapActions(['reorderNodes', 'setEditableRelation', 'setNavigationDrawerStatus', 'setActiveTool',
    'setEditableObject', 'setRootSearchRelationTreeItem', 'getRelationsBtwObjects',
    'addObjectsToGraph', 'executeMapScript', 'clearGraph', 'deleteSelectedNodes', 'deleteNode']),
    menuShow(event, object=null) {
      this.objectCtxMenu = object
      this.$refs.contextMenu.show_root(event.x, event.y)
    },
    reorderChoosingNodes() {
      this.reorderNodes(this.selectedNodes)
    },
    setSearchRelation() {
      this.setRootSearchRelationTreeItem(this.objectCtxMenu.entity)
      this.setNavigationDrawerStatus(true)
      this.setActiveTool('SearchRelationPage')
    },
    setChangeObject() {
      this.setEditableObject(this.objectCtxMenu.entity)
    },
    deleteObjects() {
      this.deleteSelectedNodes()
    },
    deleteObject() {
      this.deleteNode(this.objectCtxMenu)
    },
    createRelation(){
      let relation = []
      const edgeBtwNodes = nodes => {
        const findEdge = this.graphEdges.find(e => {
          return _.isEqual([e.entity.o1.id, e.entity.o2.id].sort(), nodes.map(n => n.entity.id).sort())
        })
        return findEdge ? findEdge.entity : nodes.map(n => n.entity)
      }
      if(this.objectCtxMenu) {
        if(!this.isNode(this.objectCtxMenu)) {
          relation = this.objectCtxMenu.entity
        }
      }
      else {
        if(this.selectedNodes.length === 2) {
          relation = edgeBtwNodes(this.selectedNodes)
        }
        else
          relation = edgeBtwNodes(this.selectedNodes.filter(o => o.ids.object_id !== 20))
      }
      this.setEditableRelation({
        relation: relation,
        document: this.selectedNodes.length === 3
          ? this.selectedNodes.find(o => o.ids.object_id === 20).entity
          : null
      })
      this.setNavigationDrawerStatus(true)
      this.setActiveTool('CreateRelationPage')
    },
    findRelations(){
      this.getRelationsBtwObjects(this.selectedNodes)
    },
    addGeometryToGraph(){
      this.$router.push({name: 'Map'}).then(() =>
        this.executeMapScript({
          request: {
            id: 1,
            name: "Вывод геометрии",
            variables: {
              geometry_object: {
                type: {title: "search", value: null},
                value: {
                  title: this.objectCtxMenu.entity.title,
                  objectId: this.objectCtxMenu.ids.object_id,
                  recId: this.objectCtxMenu.ids.rec_id
                }
              }
            }
            },
          config: {}
        })
      )
    },
    saveGraphInFile() {
      let a = document.createElement("a")
      const data = Array.from(this.graphNodes, node => {
        return {...node.ids, props: {x: node.x, y: node.y, size: node.size}}
      })
      let file = new Blob([JSON.stringify(data)], {type: 'text/plain'})
      a.href = URL.createObjectURL(file)
      a.download = new Date().getTime().toString() + '.json'
      a.click()
      a.remove()
    },
    getGraphFromFile() {
      const addObjectsToGraph = this.addObjectsToGraph
      const clearGraph = this.clearGraph
      let obj = document.createElement('input')
      obj.style.cssText = 'display:none'
      obj.type = 'file'
      obj.accept='.json'

      let input  = document.getElementById("app").appendChild(obj)
      input.click()
      const parseText = function (text, title) {
        addObjectsToGraph({payload: JSON.parse(text), action: {name: 'getGraphFromFile', payload: title}})
      }
      input.addEventListener('change', function() {
        clearGraph(false)
        input.files[0].text()
        .then(text => { parseText(text, input.value.split(/(\\|\/)/g).pop()) })
      })
      obj.remove()
    },
  },
}
</script>

