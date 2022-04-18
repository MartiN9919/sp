<template>
  <v-timeline-item :disabled="true" :color="actionParams.color" :icon="actionParams.icon">
    <v-card @mouseenter="hover" @mouseleave="leave" class="elevation-2" :color="actionParams.color" dark>
      <v-card-title class="text-body-1 text-no-wrap">{{ date }}</v-card-title>
      <v-card-subtitle>{{ actionParams.title }} {{ point.action.payload }}</v-card-subtitle>
    </v-card>
  </v-timeline-item>
</template>

<script>
export default {
  name: "TimeLinePoint",
  props: {
    point: Object
  },
  data: () => ({
    addObject: {
      color: 'green',
      icon: 'mdi-plus',
      title: 'Добавление объекта',
      alternative: {
        color: 'green darken-2',
        icon: 'mdi-plus',
        title: 'Обновление объекта'
      }
    },
    findObjects: {
      color: 'orange',
      icon: 'mdi-magnify',
      title: 'Поиск связей для'
    },
    saveObject: {
      color: 'blue',
      icon: 'mdi-pencil',
      title: 'Создание объекта'
    },
    editObject: {
      color: 'blue darken-2',
      icon: 'mdi-pencil',
      title: 'Изменение объекта'
    },
    BtwObjects: {
      color: 'orange',
      icon: 'mdi-magnify',
      title: 'Поиск связей между'
    },
    deleteNode: {
      color: 'red',
      icon: 'mdi-delete',
      title: 'Удаление объекта'
    },
    deleteNodes: {
      color: 'red darken-2',
      icon: 'mdi-delete',
      title: 'Удаление объектов'
    },
    load: {
      color: 'purple',
      icon: 'mdi-download',
      title: 'Загрузка графа с файла',
      alternative: {
        color: 'brown',
        icon: 'mdi-check',
        title: 'Откат на',
      }
    },
    actions: {
      addObjectToGraph: 'addObject',
      addGeometryToGraph: 'addObject',
      addDocumentToGraph: 'addObject',
      findRelationsOnServer: 'findObjects',
      saveEditableObject: 'editObject',
      saveObject: 'saveObject',
      getRelationsBtwObjects: 'BtwObjects',
      deleteNode: 'deleteNode',
      deleteSelectedNodes: 'deleteNodes',
      clearGraph: 'deleteNodes',
      getGraphFromFile: 'load',
      goToTimeline: 'load',
      saveFormFile: 'load'
    }
  }),
  computed: {
    actionParams: function () {
      if (this.point.updatedNodes.length) {
        return this[this.actions[this.point.action.name]].alternative || this[this.actions[this.point.action.name]]
      } else {
        return this[this.actions[this.point.action.name]]
      }
    },
    date: function () {
      return this.point.date.toLocaleString('ru-RU', {
        dateStyle: "medium",
        timeStyle: "medium"
      }).split(',').reverse().join(' ')
    },
  },
  methods: {
    hover() {
      this.$store.dispatch('setPoint', this.point.date)
      const diff = this.$store.getters.timelineDiff
      if (diff) {
        diff.nodes.map(n => n.state.added = true)
        diff.edges.map(e => e.state.added = true)
      }
    },
    leave() {
      const diff = this.$store.getters.timelineDiff
      if (diff) {
        diff.nodes.map(n => n.state.added = false)
        diff.edges.map(e => e.state.added = false)
      }
      this.$store.dispatch('setPoint', null)
    }
  }
}
</script>

<style scoped>

</style>