<template>
  <v-card flat>
    <v-card-text>
<!--      :disabled="!!newObject.rels.length"-->
      <selector-input v-model="selectedObjectId" :list="filteredObjects" item-text="title"></selector-input>
      <selector-input v-model="selectedRelationId" :list="listRelations" item-text="title" max-height="400%"></selector-input>
<!--      :disabled="listRelationItems.length === 1"-->
      <selector-input v-model="selectedRelationItemId" :list="listRelationItems" item-text="value" max-height="400%"></selector-input>
      <v-divider></v-divider>
      <v-list-group eager color="teal" class="context-settings">
        <template v-slot:activator>
          <v-list-item-title>Дополнительные настройки</v-list-item-title>
        </template>

        <v-form ref="form" lazy-validation style="width: 100%">
          <v-list-item>
            <date-time-input title="начала" v-model="selectedDateTimeStart" :clearable="true"></date-time-input>
          </v-list-item>
          <v-list-item>
            <date-time-input title="конца" v-model="selectedDateTimeEnd" :clearable="true"></date-time-input>
          </v-list-item>
        </v-form>

        <v-list-item>
          <boolean-input v-model="isActualStatus" title="Поиск только по актуальным значениям"></boolean-input>
        </v-list-item>
      </v-list-group>
      <v-divider></v-divider>
    </v-card-text>
    <v-card-actions>
      <v-btn @click="cancel" outlined color="teal" width="40%">Отмена</v-btn>
      <v-spacer></v-spacer>
      <v-btn @click="sendActionParent(createStatus)" outlined color="teal" width="40%">Готово</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import dateTimeInput from "../../../../../WebsiteShell/InputForms/dateTimeInput"
import CustomAutocomplete from "../../../../../WebsiteShell/UI/customAutocomplete"
import BooleanInput from "../../../../../WebsiteShell/InputForms/booleanInput"
import { mapActions, mapGetters } from "vuex"
import SelectorInput from "../../../../../WebsiteShell/InputForms/selectorInput";

export default {
  name: "selectObject",
  components: {SelectorInput, BooleanInput, CustomAutocomplete, dateTimeInput, },
  props: {
    object: Object,
    newObject: Object,
  },
  data: () => ({
    createStatus: '',
  }),
  computed: {
    ...mapGetters(['primaryObject', 'listOfPrimaryObjects', 'relationsTwoObjects', 'relationObject', ]),
    selectedObjectId: {
      get: function () { return this.newObject.object_id },
      set: function (id) {
        this.newObject.object_id = id
        this.selectedRelationId = this.listRelations[0].id
        this.getRelationsForObjects({ params: { object_1_id: this.object.object_id, object_2_id: id, }, })
      },
    },
    selectedRelationId: {
      get: function () { return this.newObject.rel.id },
      set: function (id) {
        this.newObject.rel.id = id
        this.selectedRelationItemID = this.listRelationItems[0].id
      },
    },
    selectedRelationItemId: {
      get: function () { return this.newObject.rel.value },
      set: function (id) { this.newObject.rel.value = id },
    },
    isActualStatus: {
      get: function () { return this.newObject.actual },
      set: function (value) { this.newObject.actual = value },
    },
    selectedDateTimeEnd: {
      get: function () { return this.newObject.rel.date_time_end },
      set: function (value) { this.newObject.rel.date_time_end = value },
    },
    selectedDateTimeStart: {
      get: function () { return this.newObject.rel.date_time_start },
      set: function (value) { this.newObject.rel.date_time_start = value },
    },
    filteredObjects () {
      let listObjects = []
      for (let item of this.listOfPrimaryObjects)
        if (item.rels.includes(this.object.object_id))
          listObjects.push(item)
      return listObjects
    },
    listRelations () {
      let relations = []
      relations = this.relationsTwoObjects({ firstId: this.object.object_id, secondId: this.selectedObjectId })
      let defaultRelations = [{ id: 0, title: 'Без связи' }]
      return Array.isArray(relations) ? defaultRelations.concat(relations) : defaultRelations
    },
    listRelationItems: function () {
      let relationList = this.listRelations.find(relation => relation.id === this.selectedRelationId)?.list
      let defaultRelationList = [{ id: 0, value: 'Не выбрано' }]
      return Array.isArray(relationList) ? defaultRelationList.concat(relationList) : defaultRelationList
    },
  },
  methods: {
    ...mapActions(['getRelationsForObjects', ]),
    sendActionParent(action) {
      if (this.$refs.form.validate())
        this.$emit(action)
    },
    cancel() {
      this.$emit('cancel')
    },
  },
  mounted() {
    if (!this.newObject.object_id)
      this.createStatus = 'create'
    if (!this.newObject.object_id)
      this.selectedObjectId = this.filteredObjects[0]?.id
    if (!this.newObject.rel.id)
      this.selectedRelationId = this.listRelations[0].id
    if (!this.newObject.rel.value)
      this.selectedRelationItemId = this.listRelationItems[0].id
  },
}
</script>

<style scoped>
.context-settings >>> .v-list-item {
  padding: 0 0;
}
</style>