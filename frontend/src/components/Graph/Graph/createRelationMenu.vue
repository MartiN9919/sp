<template>
<v-card flat>
    <v-card-text>
      <selector-input v-model="selectedRelationId" :list="listRelations" item-text="title"></selector-input>
      <selector-input v-model="selectedRelationItemId" :list="listRelationItems" item-text="value" ></selector-input>
      <v-divider></v-divider>
      <v-form ref="form" lazy-validation style="width: 100%">
        <date-time-input title="установления связи" :clearable="true"></date-time-input>
      </v-form>
      <v-divider></v-divider>
    </v-card-text>
    <v-card-actions>
      <v-btn @click="" outlined color="teal" width="40%">Отмена</v-btn>
      <v-spacer></v-spacer>
      <v-btn @click="" outlined color="teal" width="40%">Готово</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import SelectorInput from "../../WebsiteShell/InputForms/selectorInput";
import DateTimeInput from "../../WebsiteShell/InputForms/dateTimeInput";
import {mapActions, mapGetters} from "vuex";
export default {
  name: "createRelation",
  components: {DateTimeInput, SelectorInput},
  props: {
    params: Object,
  },
  data :() => ({
    relation: null,
    selectedRelationItemId: null,

  }),
  methods: {
    ...mapActions(['getBaseRelations', ])
  },
  computed : {
    ...mapGetters(['baseRelations']),
    selectedRelationId: {
      get: function () { return this.relation },
      set: function (id) {
        this.relation = id
        this.selectedRelationItemId = this.listRelationItems[0].id
      },
    },
    listRelations () {
      console.log(this.params)
      let relations = []
      relations = this.baseRelations({ f_id: this.params.object1_id, s_id: this.params.object2_id })
      console.log(relations)
      let defaultRelations = [{ id: 0, title: 'Без связи' }]
      return Array.isArray(relations) ? defaultRelations.concat(relations) : defaultRelations
    },
    listRelationItems: function () {
      let relationList = this.listRelations.find(relation => relation.id === this.selectedRelationId)?.list
      let defaultRelationList = [{ id: 0, value: 'Не выбрано' }]
      return Array.isArray(relationList) ? defaultRelationList.concat(relationList) : defaultRelationList
    },
  },
  mounted() {
    this.getBaseRelations({ params: { object_1_id: this.params.object1_id, object_2_id: this.params.object2_id, }, })
    this.relation = this.listRelations[0].id
    this.selectedRelationItemId = this.listRelationItems[0].id
  }
}
</script>

<style scoped>

</style>