<template>
  <v-card flat>
    <v-card-text v-if="newObject">
      <selector-input
        v-model="selectedObjectId"
        :items="filteredObjects"
        :disabled="!checkChildrenChangeObject"
        item-text="title"
      />
      <selector-input
        v-model="selectedRelationId"
        :items="listRelations"
        :disabled="listRelations.length === 1"
        item-text="title"
      />
      <selector-input
        v-model="selectedRelationItemId"
        :items="listRelationItems"
        :disabled="listRelationItems.length === 1"
        item-text="value"
      />
    </v-card-text>
    <template v-else>
      <v-card-title>Невозможно создать объект</v-card-title>
      <v-card-subtitle>Данный тип объектов не может содержать дочерние</v-card-subtitle>
    </template>
    <additional-settings v-if="newObject" :object="newObject" relation-setting/>
    <control-menu :buttons="buttons" @confirm="confirm" @cancel="cancel"/>
  </v-card>
</template>

<script>
import AdditionalSettings from "@/components/Graph/GraphMenu/Search/SearchTree/ControllForms/AdditionalSettings"
import SelectorInput from "@/components/WebsiteShell/InputForms/selectorInput"
import ControlMenu from "@/components/Graph/GraphMenu/Create/Modules/ControlMenu"
import {SearchTreeItem} from "@/store/modules/graph/searchTree"
import {mapGetters} from "vuex"
import _ from 'lodash'

export default {
  name: "FormCreate",
  components: {ControlMenu, AdditionalSettings, SelectorInput},
  props: {
    objectId: Number,
    changeObject: {
      type: Object,
      default: () => null
    }
  },
  data: () => ({
    newObject: null,
  }),
  computed: {
    ...mapGetters(['baseObjects', 'baseRelations', 'baseList']),
    buttons: function () {
      return [
        {action: 'cancel', title: 'Отмена', disabled: true},
        {action: 'confirm', title: 'Готово', disabled: this.newObject},
      ]
    },
    selectedObjectId: {
      get: function () {
        return this.newObject?.objectId
      },
      set: function (id) {
        this.newObject.objectId = id
        this.selectedRelationId = this.listRelations[0].id
      },
    },
    selectedRelationId: {
      get: function () {
        return this.newObject?.relId
      },
      set: function (id) {
        this.newObject.relId = id
        this.selectedRelationItemId = this.listRelationItems[0].id
      },
    },
    selectedRelationItemId: {
      get: function () {
        return this.newObject?.relValue
      },
      set: function (id) {
        this.newObject.relValue = id
      },
    },
    filteredObjects: function () {
      let listObjects = []
      for (let item of this.baseObjects) {
        if (item.rels.includes(this.objectId)) {
          listObjects.push(item)
        }
      }
      return listObjects
    },
    listRelations: function () {
      let relations = this.baseRelations({ f_id: this.objectId, s_id: this.selectedObjectId })
      let defaultRelations = [{ id: 0, title: 'Все связи' }]
      return Array.isArray(relations) ? defaultRelations.concat(relations) : defaultRelations
    },
    listRelationItems: function () {
      let relationObject = this.listRelations.find(relation => relation.id === this.selectedRelationId)
      let defaultRelationList = [{ id: 0, value: 'Все значения' }]
      if(relationObject && relationObject.hasOwnProperty('type') && relationObject.type.value) {
        return defaultRelationList.concat(this.baseList(relationObject.type.value).values)
      }
      return defaultRelationList
    },
    checkChildrenChangeObject: function () {
      if(this.changeObject) {
        return this.changeObject.rels.length === 0
      }
      return true
    }
  },
  methods: {
    confirm() {
      this.$emit('confirm', this.newObject)
      this.cancel()
    },
    cancel() {
      this.$emit('cancel')
    }
  },
  created() {
    if(this.changeObject) {
      this.newObject = _.cloneDeep(this.changeObject)
    } else if(this.filteredObjects.length) {
      this.newObject = new SearchTreeItem({
        id: this.filteredObjects[0].id,
        rel: this.listRelations[0].id,
        relValue: this.listRelationItems[0].id
      })
    }
  },
}
</script>

<style scoped>
.context-settings >>> .v-list-item {
  padding: 0 0;
}
.context-settings >>> .v-list-group__header {
  text-align: center;
  min-height: 2em;
  border: 1px solid #009688;
  border-radius: 5px;
}
</style>