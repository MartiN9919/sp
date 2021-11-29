<template>
  <v-card flat v-if="!editableRelation">
    <v-card-subtitle class="text-center text-no-wrap">
      Выбирете объекты для связи
    </v-card-subtitle>
  </v-card>
  <div v-else class="h-100">
    <div class="work-place">
      <div class="header text-center text-no-wrap py-1">
        <div v-for="(relation, key) in [editableRelation.relation.o1, editableRelation.relation.o2]" :key="key">
          <v-icon>{{relation.object.object.icon}}</v-icon>{{relation.object.title}}
        </div>
        <div v-if="editableRelation.document">
          <v-icon>{{editableRelation.document.object.object.icon}}</v-icon>{{editableRelation.document.object.title}}
        </div>
      </div>
      <v-form v-if="editableRelation" ref="form" v-model="valid" class="overflow-y-auto">
        <object-record-area
          v-if="editableRelation.relation"
          :params="editableRelation.relation.params"
          @createNewParam="createNewParam"
          @deleteNewParam="deleteNewParam"
          @addDocumentToGraph="addObjectToGraph"
        ></object-record-area>
      </v-form>
    </div>
    <control-menu :buttons="controlButtons" @create="createRelation" class="control-menu"></control-menu>
  </div>
</template>

<script>
import ObjectRecordArea from "@/components/Graph/GraphMenu/createPageComponents/objectRecordArea"
import ControlMenu from "@/components/Graph/GraphMenu/createPageComponents/controlMenu"
import {mapActions, mapGetters} from "vuex"

export default {
  name: "createRelationPage",
  components: {ControlMenu, ObjectRecordArea},
  data: () => ({
    valid: true,
  }),
  computed: {
    ...mapGetters(['editableRelation']),
    controlButtons: function () {
      return [
        {
          title: 'Создать',
          action: 'create',
          disabled: !!(this.valid && 'form' in this.$refs && this.$refs.form.inputs.length)
        },
      ]
    }
  },
  methods: {
    ...mapActions(['addNewParamEditableRelation', 'deleteNewParamEditableRelation', 'saveEditableRelation', 'addObjectToGraph']),
    createNewParam(event) {
      this.addNewParamEditableRelation(event)
    },
    deleteNewParam(event) {
      this.deleteNewParamEditableRelation({param: event.param, id: event.id})
    },
    createRelation() {
      this.saveEditableRelation()
    }
  }
}
</script>

<style scoped>
.header {
  border-bottom-width: 1px;
  border-bottom-style: solid;
  border-bottom-color: rgba(0, 0, 0, 0.12);
}
.work-place {
  height: calc(100% - 3em);
  display: flex;
  flex-direction: column;
}
.control-menu {
  height: 3em;
  align-items: flex-end;
}
</style>