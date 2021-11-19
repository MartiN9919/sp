<template>
  <v-col>
    <div class="work-place">
      <v-card flat>
        <v-card-subtitle v-if="!editableRelation" class="text-center text-no-wrap">
          Выбирете объекты для связи
        </v-card-subtitle>
        <v-card-subtitle v-else class="pa-0">
          <p v-for="(relation, key) in [editableRelation.relation.o1, editableRelation.relation.o2]" class="mb-0">
            <v-icon>
              {{relation.object.object.icon}}
            </v-icon>
            {{relation.object.title}}
          </p>
          <p class="mb-0" v-if="editableRelation.document">
            <v-icon>
              {{editableRelation.document.object.object.icon}}
            </v-icon>
            {{editableRelation.document.object.title}}
          </p>
        </v-card-subtitle>
      </v-card>
      <v-form v-if="editableRelation" ref="form" v-model="valid">
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
  </v-col>
</template>

<script>
import ObjectRecordArea from "./createPageComponents/objectRecordArea"
import ControlMenu from "./createPageComponents/controlMenu"
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
.work-place {
  height: calc(100% - 3em);
}
.control-menu {
  height: 3em;
  align-items: flex-end;
}
</style>