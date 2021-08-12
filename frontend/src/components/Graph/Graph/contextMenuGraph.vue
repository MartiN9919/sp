<template>
  <div>
  <contextMenuNested
    ref="menuGraph"
    :form="form"
    :items='menu_items'
  />
  </div>
</template>


<script>
import contextMenuNested from '@/components/WebsiteShell/ContextMenu/contextMenuNested';

export default {
  name: "menuGraph",
  components: {
    contextMenuNested,
  },
  props: {
    params: Object,
  },
  computed: {
    form: vm => vm,
    menu_items: function () {
      console.log(111)
      let menu = [
      ]
      if(!this.params?.node){
        menu.push({
          icon:     'mdi-refresh',
          title:    'Упорядочить граф',
          subtitle: 'Провести упорядочивание всех объектов по кластерам',
          action:   'updateGraph',
        })
        return menu
      }
      if(this.params?.node){
        menu.push({
            icon:     'mdi-cart-off',
            title:    'Удалить выбранные объекты',
            subtitle: 'Удалить данные объекты с графа (не из базы данных)',
            action:   'removeNode',
         })
      }
      if(this.params?.creationEdge !== 'no'){
        let relationTitle = ''
        if(this.params?.creationEdge === 'oneNode') {
          relationTitle = 'Связать с выделенным объектом'
        }
        if(this.params?.creationEdge === 'twoNodes'){
          relationTitle = 'Связать выбранные объекты'
        }
        menu.push({
          icon:     'mdi-vector-polyline-edit',
            title:     relationTitle,
            subtitle: 'Добавить связь для данного объекта',
            action:   'addRelation',
        })
      }
      return menu
    }
  },
  methods: {
    addRelation() {
      this.$emit('startRelationCreate')
    },
    removeNode(){
      this.$emit('removeNode')
    },
    updateGraph(){
      this.$emit('updateGraph')
    },
  },
  watch: {
    params: function (value) {
      this.$refs.menuGraph.show_root(value.x, value.y)
    }
  }
}
</script>

<style scoped>

</style>