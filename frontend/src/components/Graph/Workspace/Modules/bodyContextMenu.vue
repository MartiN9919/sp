<script>
import {mapActions} from "vuex"

export default {
  name: "bodyContextMenu",
  data: () => ({
    objectCtxMenu: null,
  }),
  computed: {
    changeTitle: {
      get: function () { return this.objectCtxMenu.object.showTitle },
      set: function () { this.objectCtxMenu.object.showTitle = !this.objectCtxMenu.object.showTitle }
    },
    changeTooltip: {
      get: function () { return this.objectCtxMenu.object.showTooltip },
      set: function () { this.objectCtxMenu.object.showTooltip = !this.objectCtxMenu.object.showTooltip }
    },
    changeTriggers: {
      get: function () { return this.objectCtxMenu.object.showTriggers },
      set: function () {
        this.objectCtxMenu.object.showTriggers = !this.objectCtxMenu.object.showTriggers
      }
    },
    contextMenu: function () {
      if(this.objectCtxMenu && this.objectCtxMenu.hasOwnProperty('object')){
        return [
          {
            icon: 'mdi-vector-link',
            title: 'Поиск связей',
            subtitle: 'Поиск связей для данного объекта',
            action: 'setSearchRelation'
          },
          {
            icon: 'mdi-pencil',
            title: 'Изменить',
            subtitle: 'Редактировать данный объект',
            action: 'setChangeObject'
          },
          {
            icon: 'mdi-delete',
            title: 'Удалить',
            subtitle: 'Удалить объект с графа',
            action: 'deleteObject'
          },
          {
            icon: 'mdi-cog-outline',
            title: 'Настройки',
            subtitle: 'Индивидуальные настройки объекта',
            menu: [
              {
                title: 'Отображение',
                menu: [
                  {
                    title: 'Подпись',
                    model: 'changeTitle',
                  },
                  {
                    title: 'Заголовок',
                    model: 'changeTooltip'
                  },
                  {
                    title: 'Триггеры',
                    model: 'changeTriggers'
                  }
                ]
              },
              {
                title: 'Классификаторы',
                menu: []
              },
            ],
          }
        ]
      }
      if (this.objectCtxMenu && this.objectCtxMenu.hasOwnProperty('relation')){
        return [
          {
            icon: 'mdi-check',
            title: 'Редактировать связь',
            subtitle: 'Редактировать данную связь',
            action: 'createRelation'
          },
        ]
      }
      else {
        let array = [
          {
            icon: 'mdi-download',
            title: 'Загрузить граф',
            subtitle: 'Загрузить граф из файла',
            action: 'getGraphFromFile'
          },
        ]
        this.graphObjects.length ? array.push({
          icon: 'mdi-upload',
          title: 'Сохранить граф',
          subtitle: 'Сохранить граф в файл',
          action: 'saveGraphInFile'
        }) : null
        this.graphObjects.length > 1 ? array.push({
          icon: 'mdi-pencil',
          title: 'Переупорядочить граф',
          subtitle: 'Переупорядочить граф',
          action: 'reorderGraph'
        },) : null
        this.checkRelationCreateStatus() ? array.push({
            icon: 'mdi-check',
            title: 'Создать связь',
            subtitle: 'Связать выбранные объекты',
            action: 'createRelation'
        }) : null
        this.checkFindRelationsStatus() ? array.push({
            icon: 'mdi-check',
            title: 'Найти связи',
            subtitle: 'Найти все возможные связи между выбранными объектами',
            action: 'findRelations'
        }) : null
        return array
      }
    }
  },
  methods: {
    ...mapActions(['reorderGraph', 'setEditableRelation', 'setNavigationDrawerStatus', 'setToolStatus', 'setActiveTool',
    'setEditableObject', 'deleteObjectFromGraph', 'setRootSearchRelationTreeItem', 'getRelationsBtwObjects', 'addObjectToGraph']),
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
    deleteObject(event) {
      let removeIndex = this.choosingObjects.findIndex((o) => o.id === this.objectCtxMenu.id)
      if(removeIndex !== -1) {
        for(let choosingObject of this.choosingObjects)
          this.deleteObjectFromGraph(choosingObject)
        this.choosingObjects = []
      }
      else
        this.deleteObjectFromGraph(this.objectCtxMenu)
    },
    checkRelationCreateStatus(){
      return this.choosingObjects.length === 3
        && this.choosingObjects.findIndex(o => o.object.object.id === 20) !== -1
        || this.choosingObjects.length === 2
    },
    checkFindRelationsStatus(){
      return this.choosingObjects.length === 2
    },
    createRelation(){
      this.setEditableRelation({
        relations: this.choosingObjects.length > 0 ? this.choosingObjects.length === 2 ? this.choosingObjects :
          this.choosingObjects.filter(o => o.object.object.id !== 20) :
          [this.objectCtxMenu.relation.o1, this.objectCtxMenu.relation.o2],
        document: this.choosingObjects.length === 3 ? this.choosingObjects.find(o => o.object.object.id === 20) : null
      })
      this.setNavigationDrawerStatus(true)
      this.setActiveTool('createRelationPage')
    },
    findRelations(){
      this.getRelationsBtwObjects(this.graphObjects.filter(o => this.choosingObjects.includes(o.id)))
    },
    saveGraphInFile() {
      let a = document.createElement("a");
      let file = new Blob([JSON.stringify(Array.from(this.graphObjects, node => {return {
        x: node.x,
        y: node.y,
        size: node.size,
        objectId: node.object.object.id,
        recId: node.object.recId
      }}))], {type: 'text/plain'});
      a.href = URL.createObjectURL(file);
      a.download = new Date().getTime().toString() + '.json'
      a.click();
      a.remove()
    },
    getGraphFromFile() {
      this.graphObjects.map(obj => this.deleteObjectFromGraph(obj))
      const addObjectToGraph = this.addObjectToGraph
      let obj = document.createElement('input')
      obj.style.cssText = 'display:none'
      obj.type = 'file'
      obj.accept='.json'

      let input  = document.getElementById("app").appendChild(obj)
      input.click()
      const parseText = function (text) {
        JSON.parse(text).map(obj => addObjectToGraph(
          Object.assign(
            {recId: obj.recId, objectId: obj.objectId, position: {x: obj.x, y: obj.y}, size: obj.size},
            {'noMove': true}
          )
        ))
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

