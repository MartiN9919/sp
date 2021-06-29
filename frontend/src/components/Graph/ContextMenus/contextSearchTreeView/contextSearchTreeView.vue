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
        stepBack="menuItemSelection" stepNext="selectRelation"
        :listItems="listOfPrimaryObjects" :importance="true"
        @changeWindow="stepWindowStyle = $event" v-model="selectedObject"
        @getSelectedObject="checkObject"
      ></select-object>
    </v-window-item>
    <v-window-item key="selectRelation" value="selectRelation">
      <select-object
        :header='"Выберете связь между: \"" + titleObject(object.object_id) + "\" и \"" + getTitleSelectedObject + "\""'
        stepBack="selectObject" :listItems="getRelations"
        @changeWindow="stepWindowStyle = $event" v-model="selectedRelation"
        @getSelectedObject="createRelatedObject"
      ></select-object>
    </v-window-item>
    <v-window-item key="changeObject" value="changeObject"> <!-- transition="" reverse-transition="" -->
      <select-object
        header='Если вам необходимо - измените тип объекта' stepBack="menuItemSelection" stepNext="changeRelation"
        :listItems="listOfPrimaryObjects" :importance="true"
        @changeWindow="stepWindowStyle = $event" v-model="selectedObject"
        @getSelectedObject="changeObject"
      ></select-object>
    </v-window-item>
    <v-window-item key="changeRelation" value="changeRelation"> <!-- transition="" reverse-transition="" -->
      <select-object
          header='Если вам необходимо - измените тип связи' :stepBack="object.rels.length ? null : 'changeObject'"
          :listItems="getChangeRelations"
          @changeWindow="stepWindowStyle = $event" v-model="selectedRelation"
          @getSelectedObject="changeRelatedObject"
      ></select-object>
    </v-window-item>
  </v-window>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import selectObject from "./selectObject"

export default {
  name: "contextSearchTreeView",
  components: {selectObject,},
  props: {
    object: Object,
    parentObject: { type: Object, default: null, },
  },
  data: () => ({
    stepWindowStyle: 'menuItemSelection',
    selectedObject: null,
    selectedRelation: null,
  }),
  computed: {
    ...mapGetters(['relationsBetweenTwoObjects', 'listOfPrimaryObjects', 'primaryObject', 'relationObject',]),
    bodyRightClickMenu: function () {
      let menuBody = [
        { id: 1, title: 'Добавить объект для поиска', icon: 'mdi-database-plus', next: 'selectObject' },
      ]
      if (this.parentObject) {
        menuBody.push({ id: 3, title: 'Изменить объект для поиска', icon: 'mdi-database-edit', next: !this.object.rels.length ? 'changeObject' : 'changeRelation', })
        menuBody.push({ id: 2, title: 'Удалить объект для поиска', icon: 'mdi-database-remove', next: ''})
      }
      return menuBody
    },
    getTitleSelectedObject: function () {
      return this.selectedObject ?  this.selectedObject.title_single : ''
    },
    getChangeRelations: function () {
      let relations = this.relationsBetweenTwoObjects({
        objectId1: this.parentObject?.object_id,
        objectId2: this.selectedObject?.id
      })
      if (Array.isArray(relations))
        return [{ id: 0, title: 'Без связи' }].concat(relations)
      return [{ id: 0, title: 'Без связи' }]
    },
    getRelations: function () {
      let relations = this.relationsBetweenTwoObjects({
        objectId1: this.object.object_id,
        objectId2: this.selectedObject?.id
      })
      if (Array.isArray(relations))
        return [{ id: 0, title: 'Без связи' }].concat(relations)
      return [{ id: 0, title: 'Без связи' }]
    },
  },
  methods: {
    ...mapActions(['getRelationsForObjects',]),
    checkObject(next) {
      this.getRelationsFromServer(this.object.object_id, this.selectedObject.id)
      this.stepWindowStyle = next
    },
    changeObject(next) {
      this.getRelationsFromServer(this.parentObject.object_id, this.selectedObject.id)
      this.stepWindowStyle = next
    },
    changeRelatedObject() {
      if (this.selectedObject) this.object.object_id = this.selectedObject.id
      this.object.rel_id = this.selectedRelation?.id
      this.closeContextMenu()
      this.$emit('selectMenuItemTreeView', 0)
    },
    createRelatedObject() {
      this.$emit('createNewRelation', {
        selectedObject: this.selectedObject,
        selectedRelation: this.selectedRelation,
      })
      this.closeContextMenu()
    },
    titleObject: function (id) {
      return this.primaryObject(id)?.title_single
    },
    closeContextMenu() {
      this.stepWindowStyle = 'menuItemSelection'
      this.selectedObject = null
      this.selectedRelation = null
    },
    getRelationsFromServer(firstObjectId, secondObjectId) {
      this.getRelationsForObjects({
        params: {
          object_1_id: firstObjectId,
          object_2_id: secondObjectId,
        },
      })
    },
  },
  watch: {
    stepWindowStyle: function (value) {
      if (value === 'selectObject') this.selectedObject = this.listOfPrimaryObjects[0]
      if (value === 'selectRelation') this.selectedRelation = this.getRelations[0]
      if (value === 'changeObject') this.selectedObject = this.primaryObject(this.object.object_id)
      if (value === 'changeRelation') {
        if (!this.selectedObject) {
          this.selectedObject = this.primaryObject(this.object.object_id)
          let findRelation = this.relationObject(this.object.rel_id)
          this.selectedRelation = findRelation ? findRelation : this.getChangeRelations[0]
        } else {
          if (this.selectedObject.id === this.object.object_id) {
            let findRelation = this.relationObject(this.object.rel_id)
            this.selectedRelation = findRelation ? findRelation : this.getChangeRelations[0]
          } else this.selectedRelation = this.getChangeRelations[0]
        }

      }
    },
    object: function () {
      this.closeContextMenu()
    }
  },
}
</script>

<style scoped>

</style>