<template>
  <v-card flat>
    <v-card-text class="pa-0">
      <v-list class="py-0">
        <v-list-item>
          <custom-autocomplete
            :disabled="!!newObject.rels.length"
            v-model="selectedObject"
            :items="filteredListOfPrimaryObjects"
            :item-text="'title'"
          ></custom-autocomplete>
        </v-list-item>
        <v-list-item>
          <custom-autocomplete
            v-model="selectedRelation"
            :items="listRelations"
            :item-text="'title'"
          ></custom-autocomplete>
        </v-list-item>
        <v-list-item>
          <custom-autocomplete
            v-model="selectedRelationItem"
            :items="listRelationItems"
            :item-text="'value'"
          ></custom-autocomplete>
        </v-list-item>
        <v-divider class="mt-4"></v-divider>
        <v-list-group eager color="teal">
          <template v-slot:activator>
            <v-list-item-title>Дополнительные настройки</v-list-item-title>
          </template>
          <v-list-item>
            <v-form ref="form" lazy-validation style="width: 100%">
              <div class="py-3">
                <date-time-input title="начала" v-model="selectedDateTimeStart"></date-time-input>
              </div>
              <div class="py-3">
                <date-time-input title="конца" v-model="selectedDateTimeEnd"></date-time-input>
              </div>
            </v-form>
          </v-list-item>
          <v-list-item class="pt-1">
            <boolean-input v-model="isActualStatus" :title="'Поиск только по актуальным значениям'"></boolean-input>
          </v-list-item>
        </v-list-group>
        <v-divider></v-divider>
      </v-list>
    </v-card-text>
    <v-card-actions>
      <v-btn @click="$emit('cancel')" outlined color="teal" width="40%" >Назад</v-btn>
      <v-spacer></v-spacer>
      <v-btn @click="sendActionParent(createStatus)" outlined color="teal" width="40%">Готово</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import dateTimeInput from "../../../WebsiteShell/InputForms/dateTimeInput"
import CustomAutocomplete from "../../../WebsiteShell/UI/customAutocomplete";
import BooleanInput from "../../../WebsiteShell/InputForms/booleanInput";
import { mapActions, mapGetters } from "vuex";

export default {
  name: "selectObject",
  components: {BooleanInput, CustomAutocomplete, dateTimeInput, },
  props: {
    object: Object,
    newObject: Object,
  },
  data: () => ({
    createStatus: '',
  }),
  computed: {
    ...mapGetters(['primaryObject', 'listOfPrimaryObjects', 'relationsTwoObjects', 'relationObject', ]),
    selectedObject: {
      get: function () { return this.primaryObject(this.newObject.object_id) },
      set: function (value) {
        this.newObject.object_id = value.id
        this.selectedRelation = this.listRelations[0]
        this.getRelationsForObjects({ params: { object_1_id: this.object.object_id, object_2_id: value.id, }, })
      },
    },
    selectedRelation: {
      get: function () { return this.listRelations.find(rel => rel.id === this.newObject.rel.id) },
      set: function (value) {
        this.newObject.rel.id = value.id
        this.selectedRelationItem = this.listRelationItems[0]
      },
    },
    selectedRelationItem: {
      get: function () { return this.listRelationItems.find(item => item.id === this.newObject.rel.value) },
      set: function (item) { this.newObject.rel.value = item.id },
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
    filteredListOfPrimaryObjects () {
      let listObjects = []
      for (let item of this.listOfPrimaryObjects)
        if (item.rels.includes(this.object.object_id))
          listObjects.push(item)
      return listObjects
    },
    listRelations () {
      let relations = []
      relations = this.relationsTwoObjects({ firstId: this.object.object_id, secondId: this.selectedObject?.id })
      let defaultRelations = [{ id: 0, title: 'Без связи' }]
      return Array.isArray(relations) ? defaultRelations.concat(relations) : defaultRelations
    },
    listRelationItems: function () {
      let relationList = this.selectedRelation?.list
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
  },
  mounted() {
    if (!this.newObject.object_id)
      this.createStatus = 'confirm'
    else this.createStatus = 'change'
    if (!this.newObject.object_id)
      this.selectedObject = this.filteredListOfPrimaryObjects[0]
    if (!this.newObject.rel.id)
      this.selectedRelation = this.listRelations[0]
    if (!this.newObject.rel.value)
      this.selectedRelationItem = this.listRelationItems[0]
  },
}
</script>

<style scoped>

</style>