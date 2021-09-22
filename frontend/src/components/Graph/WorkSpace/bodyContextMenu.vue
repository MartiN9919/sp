<script>
import {mapActions, mapGetters} from "vuex";

export default {
  name: "bodyContextMenu",
  data: () => ({
    objectWithActivatedMenu: null,
  }),
  computed: {
    ...mapGetters(['baseClassifiers']),
    changeTitle: {
      get: function () {
        return this.objectWithActivatedMenu.object.showTitle
      },
      set: function () {
        this.objectWithActivatedMenu.object.showTitle = !this.objectWithActivatedMenu.object.showTitle
      }
    },
    changeTooltip: {
      get: function () {
        return this.objectWithActivatedMenu.object.showTooltip
      },
      set: function () {
        this.objectWithActivatedMenu.object.showTooltip = !this.objectWithActivatedMenu.object.showTooltip
      }
    },
    changeTriggers: {
      get: function () {
        return this.objectWithActivatedMenu.object.showTriggers
      },
      set: function () {
        this.objectWithActivatedMenu.object.showTriggers = !this.objectWithActivatedMenu.object.showTriggers
      }
    },
    contextMenu: function () {
      if(this.objectWithActivatedMenu){
        return [
          {
            icon: 'mdi-pencil',
            title: 'Изменить',
            subtitle: 'Редактировать данный объект',
            action: 'setChangeObject'
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
      } else {
        let array = [{
            icon: 'mdi-pencil',
            title: 'Переупорядочить граф',
            subtitle: 'Переупорядочить граф',
            action: 'reorderGraph'
          }]
        this.checkRelationCreateStatus() ? array.push({
            icon: 'mdi-check',
            title: 'Создать связь',
            subtitle: 'Связать выбранные объекты',
            action: 'createRelation'
        }) : null
        return array
      }
    }
  },
  methods: {
    ...mapActions(['reorderGraph', 'setEditableRelation', 'setNavigationDrawerStatus', 'setToolStatus', 'setActiveTool']),
    menuShow(event, object=null) {
      this.objectWithActivatedMenu = object
      this.$refs.contextMenu.show_root(event.x, event.y)
    },
    setChangeObject(event) {

    },
    checkRelationCreateStatus(){
      return this.choosingObjects.length === 3
        && this.choosingObjects.findIndex(o => o.object.object.id === 20) !== -1
        || this.choosingObjects.length === 2
    },
    createRelation(){
      let edge = this.graphRelations.find(
          e =>  this.choosingObjects.includes(e.relation.o1) && this.choosingObjects.includes(e.relation.o2)
      )
      if(edge)
        this.setEditableRelation(edge.relation)
      else
        this.setEditableRelation({o1: this.choosingObjects[0], o2: this.choosingObjects[1], params: []})
      this.setNavigationDrawerStatus(true)
      this.setToolStatus({tool: 'createRelationPage', status: false})
      this.setActiveTool('createRelationPage')
    },
  },

}
</script>

