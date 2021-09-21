<template>
  <v-col>
    <div class="work-place">
      <div class="selector-object">
        <p>{{`${editableRelation.o1.object.object.titleSingle}: ${editableRelation.o1.object.title}`}}</p>
        <p>{{`${editableRelation.o2.object.object.titleSingle}: ${editableRelation.o2.object.title}`}}</p>
      </div>
      <v-form ref="form" v-model="valid">
        <object-record-area
          :params="editableRelation.params"
          @createNewParam="createNewParam"
          @deleteNewParam="deleteNewParam"
        ></object-record-area>
      </v-form>
    </div>
    <v-divider></v-divider>
    <control-menu
      v-if="editableRelation"
      :buttons="controlButtons"
      @create="create"
      class="control-menu"
    ></control-menu>
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
    create() {
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