<template>
  <v-card flat>
    <v-card-subtitle class="text-uppercase py-2 text-center text-break block-card-subtitle">
      {{header}}
    </v-card-subtitle>
    <v-divider></v-divider>
    <v-card-text class="px-4 py-2">
      <v-autocomplete
        :items="listRelations" item-text="title" v-model="selectedObject" return-object
        hide-details color="teal" hide-no-data item-color="teal" class="pt-0" :menu-props="{maxWidth: '23em', minWidth: '23em'}"
      ></v-autocomplete>
      <v-autocomplete
        v-if="listRelationItems" v-model="selectedRelationListItem" return-object
        :items="listRelationItems" item-text="value" :menu-props="{maxWidth: '23em', minWidth: '23em'}"
        hide-details color="teal" hide-no-data item-color="teal" class="pt-0"
      >
        <template v-slot:item="{ item }">
          <div class="my-3">{{item.value}}</div>
        </template>
      </v-autocomplete>
      <v-list>
        <v-list-group value="true" color="teal" style="margin: 0 -14px">
          <template v-slot:activator>
            <v-list-item-title>Период времени связи</v-list-item-title>
          </template>
          <v-list-item  class="pb-1">
            <v-col class="pa-0">
            <date-time-input title="начала" v-model="selectedDateTimeStart" class="pt-4"></date-time-input>
            <date-time-input title="конца" v-model="selectedDateTimeEnd" class="pt-4"></date-time-input>
            </v-col>
          </v-list-item>
        </v-list-group>
      </v-list>

    </v-card-text>
    <v-card-actions>
      <v-btn outlined color="teal" width="40%" @click="$emit('stepBack')">Назад</v-btn>
      <v-spacer></v-spacer>
      <v-btn outlined color="teal" width="40%" @click="$emit('stepNext')">Готово</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import dateTimeInput from "../../../WebsiteShell/NavigationDrawer/ConstructorBlocks/BlocksForEnteringValues/dateTimeInput"

export default {
  name: "selectRelation",
  components: { dateTimeInput, },
  props: {
    header: { type: String, default: null },
    listRelations: { type: Array, default: function () { return [] } },
    listRelationItems: { type: Array, default: function () { return null } },
    selectedRelation: { type: Object, default: null },
    selectedRelationItem: { type: Object, default:  function () { return {} } , },
    dateTimeStart: { type: Object, default: function () { return { date: '', time: '' } } },
    dateTimeEnd: { type: Object, default: function () { return { date: '', time: '' } } }
  },
  computed: {
    selectedObject: {
      get: function () { return this.selectedRelation },
      set: function (value) { this.$emit('selectedRelation', value) },
    },
    selectedRelationListItem: {
      get: function () { return this.selectedRelationItem },
      set: function (value) { this.$emit('selectedRelationItem', value) },
    },
    selectedDateTimeEnd: {
      get: function () { return this.dateTimeEnd },
      set: function (value) { this.$emit('dateTimeEnd', value) },
    },
    selectedDateTimeStart: {
      get: function () { return this.dateTimeStart },
      set: function (value) { this.$emit('dateTimeStart', value) },
    }
  },
  created() {
    this.selectedRelationListItem = this.selectedRelationItem
    this.selectedObject = this.selectedRelation
    this.selectedDateTimeEnd = this.dateTimeEnd
  },
}
</script>

<style scoped>
.block-card-subtitle {
  background-color: #009688;
  color: white !important;
}
</style>