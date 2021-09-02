<template>
  <v-card flat>
    <v-card-text>
      <selector-input
        v-model="selectedObjectId"
        :items="filteredObjects"
        :disabled="!checkChildrenChangeObject"
        item-text="title"
      ></selector-input>
      <selector-input
        v-model="selectedRelationId"
        :items="listRelations"
        :disabled="listRelations.length === 1"
        item-text="title"
      ></selector-input>
      <selector-input
        v-model="selectedRelationItemId"
        :items="listRelationItems"
        :disabled="listRelationItems.length === 1"
        item-text="value"
      ></selector-input>
      <v-list-group eager color="teal" class="context-settings pt-3" append-icon="">
        <template v-slot:activator>
          <v-list-item-title>Дополнительные настройки</v-list-item-title>
        </template>
        <v-form ref="form" lazy-validation>
          <v-list-item>
            <boolean-input
              v-model="newObject.actual"
              title="Поиск только по актуальным значениям"
            ></boolean-input>
          </v-list-item>
          <v-list-item>
            <date-time-input
              v-model="newObject.relDateTimeStart"
              :clearable="true"
              title="начала"
            ></date-time-input>
          </v-list-item>
          <v-list-item>
            <date-time-input
              v-model="newObject.relDateTimeEnd"
              :clearable="true"
              title="конца"
            ></date-time-input>
          </v-list-item>
        </v-form>
      </v-list-group>
    </v-card-text>
    <v-divider></v-divider>
    <v-card-actions class="justify-space-between">
      <v-btn
        v-for="(button, key) in actionButtons" :key="key"
        @click="buttonHandler(button.action)"
        outlined color="teal" width="40%"
      >{{ button.title }}</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import SelectorInput from "../../../WebsiteShell/InputForms/selectorInput"
import BooleanInput from "../../../WebsiteShell/InputForms/booleanInput"
import dateTimeInput from "../../../WebsiteShell/InputForms/dateTimeInput"
import { mapActions, mapGetters } from "vuex"

export default {
  name: "creatorObject",
  components: {SelectorInput, BooleanInput, dateTimeInput},
  props: {
    objectId: Number,
    changeObject: {
      type: Object,
      default: function () {
        return null
      }
    }
  },
  data: () => ({
    actionButtons: [
      { action: 'cancel', title: 'Отмена' },
      { action: 'confirm', title: 'Готово' },
    ],
    newObject: {
      id: null,
      actual: false,
      relId: null,
      relValue: null,
      relDateTimeStart: null,
      relDateTimeEnd: null
    },
  }),
  computed: {
    ...mapGetters(['baseObjects', 'baseRelations']),
    selectedObjectId: {
      get: function () {
        return this.newObject.id
      },
      set: function (id) {
        this.newObject.id = id
        this.selectedRelationId = this.listRelations[0].id
        this.getBaseRelations({params: {object_1_id: this.objectId, object_2_id: id}})
      },
    },
    selectedRelationId: {
      get: function () {
        return this.newObject.relId
      },
      set: function (id) {
        this.newObject.relId = id
        this.selectedRelationItemId = this.listRelationItems[0].id
      },
    },
    selectedRelationItemId: {
      get: function () {
        return this.newObject.relValue
      },
      set: function (id) {
        this.newObject.relValue = id
      },
    },
    filteredObjects () {
      let listObjects = []
      for (let item of this.baseObjects)
        if (item.rels.includes(this.objectId))
          listObjects.push(item)
      return listObjects
    },
    listRelations () {
      let relations = this.baseRelations({ f_id: this.objectId, s_id: this.selectedObjectId })
      let defaultRelations = [{ id: 0, title: 'Без связи' }]
      return Array.isArray(relations) ? defaultRelations.concat(relations) : defaultRelations
    },
    listRelationItems: function () {
      let relationList = this.listRelations.find(relation => relation.id === this.selectedRelationId)?.list
      let defaultRelationList = [{ id: 0, value: 'Не выбрано' }]
      return Array.isArray(relationList) ? defaultRelationList.concat(relationList) : defaultRelationList
    },
    checkChildrenChangeObject: function () {
      if(this.changeObject)
        return this.changeObject.rels.length === 0
      else return true
    }
  },
  methods: {
    ...mapActions(['getBaseRelations']),
    buttonHandler(event) {
      if (event === 'confirm')
        this.$emit('confirm', this.newObject)
      this.$emit('cancel')
    },
  },
  mounted() {
    if(this.changeObject) {
      this.selectedObjectId =  this.changeObject.object.id
      this.selectedRelationId = this.changeObject.rel?.id | 0
      this.selectedRelationItemId = this.changeObject.relValue
      this.newObject.actual = this.changeObject.actual
      this.newObject.relDateTimeStart = this.changeObject.relDateTimeStart
      this.newObject.relDateTimeEnd = this.changeObject.relDateTimeStart
    }
    else {
      this.selectedObjectId =  this.filteredObjects[0].id
      this.selectedRelationId = this.listRelations[0].id
      this.selectedRelationItemId = this.listRelationItems[0].id
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