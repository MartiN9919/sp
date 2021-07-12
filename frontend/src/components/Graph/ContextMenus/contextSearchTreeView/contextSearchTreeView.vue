<template>
  <v-window v-model="stepWindowStyle">
    <v-window-item key="menuItemSelection" value="menuItemSelection" eager>
      <v-list rounded>
        <v-list-item
          v-for="(item, index) in bodyRightClickMenu" :key="index" dense
          @click="item.next ? changeWindow(item.next) : $emit('selectMenuItemTreeView', item)">
          <v-list-item-title style="font-size: 1em">{{ item.title }}</v-list-item-title>
          <v-list-item-icon>
            <v-icon right color="teal">{{ item.icon }}</v-icon>
          </v-list-item-icon>
        </v-list-item>
      </v-list>
    </v-window-item>
    <v-window-item key="selectObject" value="selectObject" eager>
      <select-object
        :header='"Выберете объект для связи с объектом: \"" + titleObject(object.object_id) + "\""'
        :listItems="filteredListOfPrimaryObjects(object.object_id)"
        :is-actual="isActualStatus" @isActual="isActualStatus = $event"
        :selected-object="selectedObject" @selectedObject="selectedObject = $event"
        @stepNext="getRelationsForSelectObject(object.object_id, 'selectRelation')"
        @stepBack="changeWindow('menuItemSelection', true)"
      ></select-object>
    </v-window-item>
    <v-window-item key="selectRelation" value="selectRelation" eager>
      <select-relation
        :header='"Выберете связь между: \"" + titleObject(object.object_id) + "\" и \"" + getTitleSelectedObject + "\""'
        :list-relations="getRelations(object.object_id)" :list-relation-items="getListRelationItems"
        :selected-relation="selectedRelation" @selectedRelation="selectedRelation = $event"
        :selected-relation-item="selectedRelationListItem" @selectedRelationItem="selectedRelationListItem = $event"
        :date-time-start="dateTimeStart" @dateTimeStart="dateTimeStart = $event"
        :date-time-end="dateTimeEnd" @dateTimeEnd="dateTimeEnd = $event"
        @stepNext="createRelatedObject" @stepBack="changeWindow('selectObject', true)"
      ></select-relation>
    </v-window-item>
    <v-window-item key="changeObject" value="changeObject" v-if="parentObject" eager>
      <select-object
        header='Если вам необходимо - измените тип объекта' stepBack="menuItemSelection"
        :listItems="filteredListOfPrimaryObjects(parentObject.object_id)"
        :is-actual="isActualStatus" @isActual="isActualStatus = $event"
        :selected-object="selectedObject" @selectedObject="selectedObject = $event"
        :disable-selected-object="!!object.rels.length"
        @stepNext="getRelationsForSelectObject(parentObject.object_id, 'changeRelation')"
        @stepBack="changeWindow('menuItemSelection', true)"
      ></select-object>
    </v-window-item>
    <v-window-item key="changeRelation" value="changeRelation" v-if="parentObject" eager>
      <select-relation
        :header='"Если вам необходимо - измените тип связи"'
        :list-relations="getRelations(parentObject.object_id)" :list-relation-items="getListRelationItems"
        :selected-relation="selectedRelation" @selectedRelation="selectedRelation = $event"
        :selected-relation-item="selectedRelationListItem" @selectedRelationItem="selectedRelationListItem = $event"
        :date-time-start="dateTimeStart" @dateTimeStart="dateTimeStart = $event"
        :date-time-end="dateTimeEnd" @dateTimeEnd="dateTimeEnd = $event"
        @stepNext="changeRelatedObject" @stepBack="changeWindow('changeObject', true)"
      ></select-relation>
    </v-window-item>
  </v-window>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import selectObject from "./selectObject"
import selectRelation from "./selectRelation";

export default {
  name: "contextSearchTreeView",
  components: { selectObject, selectRelation, },
  props: { object: Object, parentObject:  Object, },
  data: () => ({
    stepWindowStyle: 'menuItemSelection',
    isActualStatus: false,
    selectedObject: null,
    selectedRelation: null,
    selectedRelationListItem: null,
    dateTimeStart: null,
    dateTimeEnd: null,
  }),
  computed: {
    ...mapGetters(['relationsTwoObjects', 'listOfPrimaryObjects', 'primaryObject', 'relationObject',]),
    getTitleSelectedObject: function () { return this.selectedObject ?  this.selectedObject.title_single : '' },
    bodyRightClickMenu: function () {
      let menuBody = [{ id: 1, title: 'Добавить объект для поиска', icon: 'mdi-database-plus', next: 'selectObject' }]
      if (this.parentObject) {
        menuBody.push({ id: 3, title: 'Изменить объект для поиска', icon: 'mdi-database-edit', next: 'changeObject' })
        menuBody.push({ id: 2, title: 'Удалить объект для поиска', icon: 'mdi-database-remove', next: '' })
      }
      return menuBody
    },
    getListRelationItems: function () {
      let relationList = this.selectedRelation?.list
      let defaultRelationList = [{ id: 0, value: 'Не выбрано' }]
      return Array.isArray(relationList) ? defaultRelationList.concat(relationList) : defaultRelationList
    },
  },
  methods: {
    ...mapActions(['getRelationsForObjects',]),
    changeWindow (stepNext, stepBack=false) {
      if (stepNext === 'menuItemSelection') {
        this.isActualStatus = false
        this.selectedObject = this.filteredListOfPrimaryObjects(this.object.object_id)[0]
        this.selectedRelation = this.getRelations(this.object.object_id)[0]
        this.selectedRelationListItem = this.getListRelationItems[0]
        this.dateTimeStart = null
        this.dateTimeEnd = this.getDateTimeEnd()
      }
      if (stepNext === 'selectRelation') {
        let relations = this.getRelations(this.object.object_id)
        if (!relations.find(relation => relation === this.selectedRelation)) {
          this.selectedRelation = relations[0]
          this.selectedRelationListItem = this.getListRelationItems[0]
          this.dateTimeStart = null
          this.dateTimeEnd = this.getDateTimeEnd()
        }
      }
      if (stepNext === 'changeObject' && !stepBack) {
        let filteredList = this.filteredListOfPrimaryObjects(this.parentObject.object_id)
        this.isActualStatus = this.object.actual
        this.selectedObject = filteredList.find(primary => primary.id === this.object.object_id)
      }
      if (stepNext === 'changeRelation') {
        let findRelation = this.relationObject(this.object.rel.id)
        let relations = this.getRelations(this.parentObject.object_id)
        if (findRelation) this.selectedRelation = findRelation
        else this.selectedRelation = relations[0]
        this.$nextTick(function () {
          if (!relations.find(relation => relation === this.selectedRelation)) {
            this.selectedRelation = relations[0]
            this.selectedRelationListItem = this.getListRelationItems[0]
            this.dateTimeStart = null
            this.dateTimeEnd = this.getDateTimeEnd()
          } else {
            this.dateTimeStart = this.object.rel.date_time_start
            this.dateTimeEnd = this.object.rel.date_time_end
            if (this.selectedRelation?.list) {
              let findValue = this.selectedRelation.list.find(item => item.id === this.object.rel.value)
              if (findValue)
                this.selectedRelationListItem = this.selectedRelation.list.find(item => item.id === this.object.rel.value)
              else this.selectedRelationListItem = this.getListRelationItems[0]
            }
            else
              this.selectedRelationListItem = this.getListRelationItems[0]
          }
        })
      }
      this.stepWindowStyle = stepNext
    },
    titleObject: function (id) { return this.primaryObject(id)?.title_single },
    filteredListOfPrimaryObjects (objectId) {
      let filteredListOfPrimaryObjects = []
      for (let item of this.listOfPrimaryObjects)
        if (item.rels.includes(objectId))
          filteredListOfPrimaryObjects.push(item)
      return filteredListOfPrimaryObjects
    },
    getRelationsForSelectObject(parentObjectId, stepNext) {
      this.getRelationsForObjects({
        params: { object_1_id: parentObjectId, object_2_id: this.selectedObject.id, },
      })
      this.changeWindow(stepNext)
    },
    getRelations (parentObjectId) {
      let relations = this.relationsTwoObjects({ firstId: parentObjectId, secondId: this.selectedObject?.id })
      let defaultRelations = [{ id: 0, title: 'Без связи' }]
      return Array.isArray(relations) ? defaultRelations.concat(relations) : defaultRelations
    },
    getDateTimeEnd: function () {
      let dateTime = new Date()
      let time = dateTime.toLocaleTimeString().split(':')
      let date = dateTime.toLocaleDateString().split('/')
      return date[2] + '-' + date[1] + '-' + date[0] + ' ' + time[0] + ':' + time[1]
    },
    createRelatedObject() {
      this.$emit('createNewRelation', {
        actual: this.isActualStatus,
        selectedObject: this.selectedObject,
        selectedRelation: this.selectedRelation,
        value: this.selectedRelationListItem.id,
        date_time_start: this.dateTimeStart,
        date_time_end: this.dateTimeEnd,
      })
      this.changeWindow('menuItemSelection')
    },
    changeRelatedObject () {
      this.object.object_id = this.selectedObject.id
      this.object.actual = this.isActualStatus
      this.object.rel.id = this.selectedRelation.id
      this.object.rel.value = this.selectedRelationListItem.id
      this.object.rel.date_time_start = this.dateTimeStart
      this.object.rel.date_time_end = this.dateTimeEnd
      this.changeWindow('menuItemSelection')
      this.$emit('selectMenuItemTreeView', {id: null})
    }
  },
  watch: {
    object: function () { this.changeWindow('menuItemSelection') },
    selectedRelation: function () { this.selectedRelationListItem = this.getListRelationItems[0] },
  },
  created() { this.changeWindow('menuItemSelection') },
}
</script>

<style scoped>

</style>