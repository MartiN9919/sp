<template>
  <v-expansion-panels v-model="openedPanels" multiple accordion hover focusable tile class="expansion-panels">
    <v-expansion-panel v-for="(classifier, key) in classifiers" :key="key">
      <record-title
        :title="getClassifierObject(classifier.id).title"
        :opened="openedPanels.includes(key)"
        @createNewParam="createNewParam(classifier.id)"
      ></record-title>
      <v-expansion-panel-content

        eager class="expansion-panel-content-custom"
      >
        <v-card  tile flat>
          <v-row v-for="param in classifier.new_values" no-gutters class="flex-nowrap">
            <record-input
              :param="param"
              @deletable="deleteNewParam(classifier.id, param)"
              :type="getClassifierObject(classifier.id).type"
              :list="getClassifierObject(classifier.id).list_id"
            ></record-input>
          </v-row>
          <table-old-values :values="classifier.values"></table-old-values>
        </v-card>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script>
import RecordTitle from "./objectRecordComponents/recordTitle"
import RecordInput from "./objectRecordComponents/recordInput"
import DropDownMenu from "../../../WebsiteShell/UI/dropDownMenu"
import MenuDateTime from "../../../WebsiteShell/UI/selectDateTime"
import {mapActions, mapGetters} from "vuex"
import TableOldValues from "./objectRecordComponents/tableOldValues";

export default {
  name: "objectRecordArea",
  components: {TableOldValues, RecordInput, RecordTitle, MenuDateTime, DropDownMenu},
  props: {
    classifiers: Array,
  },
  data: () => ({
    openedPanels: []
  }),
  computed: mapGetters(['classifierObject', 'editableObject']),
  methods: {
    ...mapActions(['addNewParamEditableObject', 'deleteNewParamEditableObject']),
    getClassifierObject(classifierId) {
      return this.classifierObject({ objectId: this.editableObject.object_id, classifierId: classifierId})
    },
    createNewParam(classifierId) {
      this.addNewParamEditableObject(classifierId)
    },
    deleteNewParam(classifierId, param) {
      this.deleteNewParamEditableObject({classifierId: classifierId, param: param})
    }
  },
  mounted() {
    this.openedPanels = [...Array(this.classifiers.length).keys()]
  },
  watch: {
    classifiers: function (value) { this.openedPanels = [...Array(value.length).keys()] }
  }
}
</script>

<style scoped>
.expansion-panels {
  border-bottom: 1px solid rgba(0, 0, 0, 0.20);
}
.v-expansion-panel >>> .v-expansion-panel-header {
  min-height: 32px;
}
.expansion-panel-content-custom >>> .v-expansion-panel-content__wrap {
  padding: 0 8;
}
</style>