<template>
  <v-list rounded v-if="stepWindowStyle === 'menuItemSelection'">
    <v-list-item
      v-for="(item, index) in bodyRightClickMenu" :key="index" dense
      @click="selectMenuItem(item)">
      <v-list-item-title style="font-size: 1em">{{ item.title }}</v-list-item-title>
      <v-list-item-icon>
        <v-icon right color="teal">{{ item.icon }}</v-icon>
      </v-list-item-icon>
    </v-list-item>
  </v-list>
  <select-object
    v-else-if="stepWindowStyle === 'selectObject'"
    :object="object"
    :new-object="newObject"
    @cancel="cancel"
    @confirm="confirm"
  ></select-object>
  <select-object
    v-else-if="stepWindowStyle === 'changeObject'"
    :object="parentObject"
    :new-object="object"
    @cancel="cancel"
    @change="change"
  ></select-object>
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
    parentObject:  Object,
    newObject: Object,
  },
  data: () => ({
    stepWindowStyle: 'menuItemSelection',
  }),
  computed: {
    ...mapGetters(['relationsTwoObjects', 'listOfPrimaryObjects', 'primaryObject', 'relationObject',]),
    bodyRightClickMenu: function () {
      let menuBody = [{ id: 1, title: 'Добавить объект для поиска', icon: 'mdi-database-plus', next: 'selectObject' }]
      if (this.parentObject) {
        menuBody.push({ id: 3, title: 'Изменить объект для поиска', icon: 'mdi-database-edit', next: 'changeObject' })
        menuBody.push({ id: 2, title: 'Удалить объект для поиска', icon: 'mdi-database-remove', next: '' })
      }
      return menuBody
    },
  },
  methods: {
    cancel () {
      this.stepWindowStyle = 'menuItemSelection'
      this.$emit('deleteNewRelation')
    },
    confirm () {
      this.stepWindowStyle = 'menuItemSelection'
      this.$emit('createNewRelation')
    },
    change () {
      this.stepWindowStyle = 'menuItemSelection'
      this.$emit('changeNewRelation')
    },
    selectMenuItem (item) {
      if (item.hasOwnProperty('next'))
        this.stepWindowStyle = item.next
      this.$emit('selectMenuItemTreeView', item.id)
    }
  },
  watch: {
    object: function () {
      this.stepWindowStyle = 'menuItemSelection'
    }
  }
}
</script>

<style scoped>

</style>