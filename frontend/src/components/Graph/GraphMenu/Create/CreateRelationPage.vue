<template>
  <create-page-body :editable="editableRelation">
    <template v-slot:header>
      <relation-header :objects="editableObjects"/>
      <v-card flat v-if="!editableObjects.length">
        <v-card-subtitle class="text-center text-no-wrap">
          Выберите на графе объекты для создания связи
        </v-card-subtitle>
      </v-card>
    </template>
    <template v-slot:body>
      <v-form ref="form" v-model="valid" class="overflow-y-auto" onSubmit="return false;">
        <record-area
          :params="editableRelation.relation.params"
          @addDocumentToGraph="addDocumentToGraph"
        />
      </v-form>
    </template>
    <template v-slot:control>
      <control-menu :buttons="controlButtons" @create="createRelation" class="control-menu"/>
    </template>
  </create-page-body>
</template>

<script>
import CreatePageBody from "@/components/Graph/GraphMenu/Create/Modules/CreatePageBody"
import RecordArea from "@/components/Graph/GraphMenu/Create/Record/RecordArea"
import ControlMenu from "@/components/Graph/GraphMenu/Create/Modules/ControlMenu"
import {mapActions, mapGetters} from "vuex"
import RelationHeader from "@/components/Graph/GraphMenu/Create/Headers/RelationHeader";

export default {
  name: "CreateRelationPage",
  components: {RelationHeader, CreatePageBody, ControlMenu, RecordArea},
  data: () => ({
    valid: true,
  }),
  computed: {
    ...mapGetters(['editableRelation']),
    editableObjects: function () {
      if(this.editableRelation) {
        return [
          this.editableRelation.relation.o1,
          this.editableRelation.relation.o2,
          this.editableRelation.document
        ]
      }
      else {
        return []
      }
    },
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
    ...mapActions([
      'saveEditableRelation',
      'addObjectToGraph',
      'clearSelectedNodes',
    ]),
    createRelation() {
      this.saveEditableRelation().then(() => { this.clearSelectedNodes() })
    },
    addDocumentToGraph(object) {
      this.addObjectToGraph({
        object,
        action: {
          name: 'addDocumentToGraph',
          payload: object.title
        }
      })
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