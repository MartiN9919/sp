<template>
  <v-col>
    <div class="work-place">
      <div class="selector-object">
        <p>{{`${editableRelation.o1.titleSingle}: ${editableRelation.o1Object.title}`}}</p>
        <p>{{`${editableRelation.o2.titleSingle}: ${editableRelation.o2Object.title}`}}</p>
      </div>
      <v-form ref="form" v-model="valid">
        <object-record-area
          :classifiers="editableRelation.params"
          @createNewParam="createNewParam"
        ></object-record-area>
      </v-form>
    </div>
    <v-divider></v-divider>
    <control-menu
      v-if="editableRelation"
      :buttons="controlButtons"
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
      console.log(!!(this.valid))
      console.log(('form' in this.$refs && !!(this.$refs.form.inputs.length)))
      console.log(this.$refs.form)
      return [
        {
          title: 'Создать',
          action: 'recreate',
          disabled: !!(this.valid && 'form' in this.$refs && this.$refs.form.inputs.length)
        },
      ]
    }
  },
  methods: {
    ...mapActions(['addNewParamEditableRelation']),
    createNewParam(event) {
      this.addNewParamEditableRelation(event)
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