<template>
  <v-col>
    <div class="work-place">
      <v-card flat>
        <v-card-subtitle v-if="!editableRelation" class="text-center text-no-wrap">
          Выбирете объекты для связи
        </v-card-subtitle>
        <v-card-subtitle v-else class="pa-0">
          <p v-for="(relation, key) in [editableRelation.o1, editableRelation.o2]" class="mb-0">
            <v-icon>
              {{relation.object.object.icon}}
            </v-icon>
            {{relation.object.title}}
          </p>
        </v-card-subtitle>
      </v-card>
      <v-form ref="form" v-model="valid">
        <object-record-area
          v-if="editableRelation"
          :params="editableRelation.params"
          @createNewParam="createNewParam"
          @deleteNewParam="deleteNewParam"
        ></object-record-area>
      </v-form>
    </div>
    <v-divider></v-divider>
    <control-menu :buttons="controlButtons" @create="createRelation" class="control-menu"></control-menu>
  </v-col>
</template>

<script>
import ObjectRecordArea from "./createPageComponents/objectRecordArea";
import {mapActions, mapGetters} from "vuex";
import ControlMenu from "./createPageComponents/controlMenu";

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
    ...mapActions(['addNewParamEditableRelation', 'deleteNewParamEditableRelation', 'saveEditableRelation']),
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
.selector-object {
  height: 5em;
}
.control-menu {
  height: 3em;
  align-items: flex-end;
}
</style>