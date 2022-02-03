<script>
import ctxMenu from "@/components/Graph/WorkSpace/Modules/ctxMenu"
import {mapActions} from "vuex"

export default {
  name: "bodyContextMenu",
  data: () => ({
    objectCtxMenu: null,
  }),
  computed: {
    relationCreateStatus: function(){
      return this.selectedGraphObjects.length === 3
        && this.selectedGraphObjects.findIndex(o => o.object.object.id === 20) !== -1
        || this.selectedGraphObjects.length === 2
    },
    findRelationsStatus: function(){
      return this.selectedGraphObjects.length === 2
    },
    relationTooltip: {
      get: function () { return this.objectCtxMenu.relation.showTooltip },
      set: function () { this.objectCtxMenu.relation.showTooltip = !this.objectCtxMenu.relation.showTooltip }
    },
    relationCreateDate: {
      get: function () { return this.objectCtxMenu.relation.showCreateDate },
      set: function () { this.objectCtxMenu.relation.showCreateDate = !this.objectCtxMenu.relation.showCreateDate }
    },
    objectTitle: {
      get: function () { return this.objectCtxMenu.object.showTitle },
      set: function () { this.objectCtxMenu.object.showTitle = !this.objectCtxMenu.object.showTitle }
    },
    objectTooltip: {
      get: function () { return this.objectCtxMenu.object.showTooltip },
      set: function () { this.objectCtxMenu.object.showTooltip = !this.objectCtxMenu.object.showTooltip }
    },
    objectCreateDate: {
      get: function () { return this.objectCtxMenu.object.showCreateDate },
      set: function () { this.objectCtxMenu.object.showCreateDate = !this.objectCtxMenu.object.showCreateDate }
    },
    objectTriggers: {
      get: function () { return this.objectCtxMenu.object.showTriggers },
      set: function () {
        this.objectCtxMenu.object.showTriggers = !this.objectCtxMenu.object.showTriggers
      }
    },
    contextMenu: function () {
      if(this.objectCtxMenu) {
        if(this.objectCtxMenu.hasOwnProperty('object')) {
          return ctxMenu.getObjectCtxMenu(
            this.objectCtxMenu.object.object.id === 25 || this.objectCtxMenu.object.object.id === 30
          )
        } else {
          if (this.objectCtxMenu.hasOwnProperty('relation')) {
            return ctxMenu.RelationCtxMenu
          }
        }
      }
      else {
        return ctxMenu.getSpaceCtxMenu(
          this.graphObjects.length,
          this.graphObjects.length > 1,
          this.relationCreateStatus,
          this.findRelationsStatus,
          this.selectedGraphObjects.length,
        )
      }
    }
  },
  methods: {
    ...mapActions(['reorderGraph', 'reorderChoosingObjects', 'setEditableRelation', 'setNavigationDrawerStatus', 'setToolStatus', 'setActiveTool',
    'setEditableObject', 'deleteObjectFromGraph', 'setRootSearchRelationTreeItem', 'getRelationsBtwObjects',
    'addToGraphFromServer', 'executeMapScript', 'clearGraph']),
    menuShow(event, object=null) {
      this.objectCtxMenu = object
      this.$refs.contextMenu.show_root(event.x, event.y)
    },
    setSearchRelation(event) {
      this.setRootSearchRelationTreeItem(this.objectCtxMenu)
      this.setNavigationDrawerStatus(true)
      this.setActiveTool('searchRelationPage')
    },
    setChangeObject(event) {
      this.setEditableObject({
        objectId: this.objectCtxMenu.object.object.id,
        recId: this.objectCtxMenu.object.recId
      })
    },
    deleteObjects() {
      for(let choosingObject of this.selectedGraphObjects)
        this.deleteObjectFromGraph(choosingObject)
      this.clearSelectedGraphObjects()
    },
    deleteObject() {
      this.deleteSelectedGraphObject(this.objectCtxMenu)
      this.deleteObjectFromGraph(this.objectCtxMenu)
    },
    createRelation(){
      let relations = []
      if(this.objectCtxMenu && this.objectCtxMenu.hasOwnProperty('relation')) {
         relations = [this.objectCtxMenu.relation.o1, this.objectCtxMenu.relation.o2]
      }
      else {
        if(this.selectedGraphObjects.length === 2)
          relations = this.selectedGraphObjects
        else
          relations = this.selectedGraphObjects.filter(o => o.object.object.id !== 20)
      }
      this.setEditableRelation({
        relations: relations,
        document: this.selectedGraphObjects.length === 3
          ? this.selectedGraphObjects.find(o => o.object.object.id === 20)
          : null
      })
      this.setNavigationDrawerStatus(true)
      this.setActiveTool('createRelationPage')
    },
    findRelations(){
      this.getRelationsBtwObjects(this.graphObjects.filter(o => this.inSelectedGraphObject(o)))
    },
    addGeometryToGraph(){
      this.$router.push({name: 'Map'})
      this.executeMapScript({ request: {id: 1, name: "Вывод геометрии", variables: {
        geometry_object: {
          type: {title: "search", value: null}, value: {
            title: this.objectCtxMenu.object.title,
            objectId: this.objectCtxMenu.object.object.id,
            recId: this.objectCtxMenu.object.recId}}}},
        config: {}
      })
    },
    saveGraphInFile() {
      let a = document.createElement("a");
      let file = new Blob([JSON.stringify(Array.from(this.graphObjects, node => {return {
        props: {
          x: node.x,
          y: node.y,
          size: node.size
        },
        object_id: node.object.object.id,
        rec_id: node.object.recId
      }}))], {type: 'text/plain'});
      a.href = URL.createObjectURL(file);
      a.download = new Date().getTime().toString() + '.json'
      a.click();
      a.remove()
    },
    getGraphFromFile() {
      this.clearGraph()
      const addObjectToGraph = this.addToGraphFromServer
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

