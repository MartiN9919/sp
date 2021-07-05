<template>
  <v-window v-model="stepWindowStyle">
    <v-window-item key="menuItemSelection" value="menuItemSelection">
      <v-list rounded>
        <v-list-item
          v-for="(item, index) in bodyRightClickMenu" :key="index" dense
          @click="item.next ? stepWindowStyle = item.next : $emit('selectMenuItemTreeView', item)">
          <v-list-item-title style="font-size: 1em">{{ item.title }}</v-list-item-title>
          <v-list-item-icon>
            <v-icon right color="teal">{{ item.icon }}</v-icon>
          </v-list-item-icon>
        </v-list-item>
      </v-list>
    </v-window-item>
    <v-window-item key="selectObject" value="selectObject">
      <select-object
        :header='"Выберете объект для связи с объектом: \"" + titleObject(object.object_id) + "\""'
        :listItems="listOfPrimaryObjects" @isActual="isActualStatus = $event"
        :selected-object="selectedObject" @selectedObject="selectedObject =$event"
        @stepNext="checkObject" @stepBack="stepWindowStyle = 'menuItemSelection'"
      ></select-object>
    </v-window-item>
    <v-window-item key="selectRelation" value="selectRelation">
      <select-relation
        :header='"Выберете связь между: \"" + titleObject(object.object_id) + "\" и \"" + getTitleSelectedObject + "\""'
        :list-relations="getRelations" :list-relation-items="getListRelationItems"
        :selected-relation="selectedRelation" @selectedRelation="selectedRelation = $event"
        :selected-relation-item="selectedRelationListItem" @selectedRelationItem="selectedRelationListItem = $event"
        :date-time-start="dateTimeStart" @dateTimeStart="dateTimeStart = $event"
        :date-time-end="dateTimeEnd" @dateTimeEnd="dateTimeEnd = $event"
        @stepNext="createRelatedObject" @stepBack="stepWindowStyle = 'selectObject'"
      ></select-relation>
    </v-window-item>
<!--    <v-window-item key="changeObject" value="changeObject"> &lt;!&ndash; transition="" reverse-transition="" &ndash;&gt;-->
<!--      <select-object-->
<!--        header='Если вам необходимо - измените тип объекта' stepBack="menuItemSelection" stepNext="changeRelation"-->
<!--        :listItems="listOfPrimaryObjects" :importance="true"-->
<!--        @changeWindow="stepWindowStyle = $event" v-model="selectedObject"-->
<!--        @getSelectedObject="changeObject"-->
<!--      ></select-object>-->
<!--    </v-window-item>-->
<!--    <v-window-item key="changeRelation" value="changeRelation"> &lt;!&ndash; transition="" reverse-transition="" &ndash;&gt;-->
<!--      <select-object-->
<!--          header='Если вам необходимо - измените тип связи' :stepBack="object.rels.length ? null : 'changeObject'"-->
<!--          :listItems="getChangeRelations"-->
<!--          @changeWindow="stepWindowStyle = $event" v-model="selectedRelation"-->
<!--          @getSelectedObject="changeRelatedObject"-->
<!--      ></select-object>-->
<!--    </v-window-item>-->
  </v-window>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import selectObject from "./selectObject"
import selectRelation from "./selectRelation";

export default {
  name: "contextSearchTreeView",
  components: { selectObject, selectRelation, },
  props: {
    object: Object,
    parentObject: { type: Object, default: null, },
  },
  data: () => ({
    stepWindowStyle: 'menuItemSelection',
    isActualStatus: false,
    selectedObject: null,
    selectedRelation: null,
    selectedRelationListItem: null,
    dateTimeStart: { date: '', time: '' },
    dateTimeEnd: { date: '', time: '' },
  }),
  computed: {
    ...mapGetters(['relationsTwoObjects', 'listOfPrimaryObjects', 'primaryObject', 'relationObject',]),
    getTitleSelectedObject: function () { return this.selectedObject ?  this.selectedObject.title_single : '' },
    bodyRightClickMenu: function () {
      let menuBody = [{ id: 1, title: 'Добавить объект для поиска', icon: 'mdi-database-plus', next: 'selectObject' },]
      if (this.parentObject) {
        menuBody.push({ id: 3, title: 'Изменить объект для поиска', icon: 'mdi-database-edit',
          next: !this.object.rels.length ? 'changeObject' : 'changeRelation', })
        menuBody.push({ id: 2, title: 'Удалить объект для поиска', icon: 'mdi-database-remove', next: ''})
      }
      return menuBody
    },
    // getChangeRelations: function () {
    //   let relations = this.relationsBetweenTwoObjects({
    //     objectId1: this.parentObject?.object_id,
    //     objectId2: this.selectedObject?.id
    //   })
    //   if (Array.isArray(relations))
    //     return [{ id: 0, title: 'Без связи' }].concat(relations)
    //   return [{ id: 0, title: 'Без связи' }]
    // },
    getRelations: function () {
      let relations = this.relationsTwoObjects({ firstId: this.object.object_id, secondId: this.selectedObject?.id })
      let defaultRelations = [{ id: 0, title: 'Без связи' }]
      return Array.isArray(relations) ? defaultRelations.concat(relations) : defaultRelations
    },
    getListRelationItems: function () {
      let relationList = this.selectedRelation?.list
      let defaultRelationList = [{ id: 0, value: 'Не выбрано' }]
      return Array.isArray(relationList) ? defaultRelationList.concat(relationList) : defaultRelationList
    },
  },
  methods: {
    ...mapActions(['getRelationsForObjects',]),
    titleObject: function (id) { return this.primaryObject(id)?.title_single },
    checkObject() {
      this.getRelationsForObjects({
        params: { object_1_id: this.object.object_id, object_2_id: this.selectedObject.id, },
      })
      this.stepWindowStyle = 'selectRelation'
    },
    getDateTimeEnd: function () {
      let dateTime = new Date()
      let time = dateTime.toLocaleTimeString().split(':')
      let date = dateTime.toLocaleDateString().split('/')
      return {
        date: date[2] + '-' + date[1] + '-' + date[0],
        time: time[0] + ':' + time[1],
      }
    },
    // changeObject(next) {
    //   this.getRelationsForObjects({
    //     params: { object_1_id: this.parentObject.object_id, object_2_id: this.selectedObject.id, },
    //   })
    //   this.stepWindowStyle = next
    // },
    // changeRelatedObject() {
    //   if (this.selectedObject) this.object.object_id = this.selectedObject.id
    //   this.object.rel_id = this.selectedRelation?.id
    //   this.setDefaultValues()
    //   this.$emit('selectMenuItemTreeView', 0)
    // },
    createRelatedObject() {
      this.$emit('createNewRelation', {
        actual: this.isActualStatus,
        selectedObject: this.selectedObject,
        selectedRelation: this.selectedRelation,
        value: this.selectedRelationListItem.id,
        date_time_start: this.dateTimeStart,
        date_time_end: this.dateTimeEnd,
      })
      this.setDefaultValues()
    },
    setDefaultValues() {
      this.stepWindowStyle = 'menuItemSelection'
      this.isActualStatus = false
      this.selectedObject = this.listOfPrimaryObjects[0]
      this.selectedRelation = this.getRelations[0]
      this.selectedRelationListItem = this.getListRelationItems[0]
      this.dateTimeStart = { date: '', time: '' }
      this.dateTimeEnd = this.getDateTimeEnd()
    },
    // getRelationsFromServer(firstObjectId, secondObjectId) {
    //   this.getRelationsForObjects({ params: { object_1_id: firstObjectId, object_2_id: secondObjectId, }, })
    // },
  },
  watch: {
    object: function () {
      this.setDefaultValues()
    },
    selectedRelation: function () {
      this.selectedRelationListItem = this.getListRelationItems[0]
    },
  },
  created() {
    this.setDefaultValues()
  }
}
</script>

<style scoped>

</style>