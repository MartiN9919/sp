<template>
  <v-expansion-panels v-model="openedPanels" multiple accordion hover focusable tile>
    <v-expansion-panel v-for="(param, key) in params" :key="key">
      <record-title
        :title="param.baseParam.title"
        :opened="openedPanels.includes(key)"
        @create="createNewParam(param.baseParam.id)"
        @keyup.ctrl.enter.native="createNewParam(param.baseParam.id)"
      />
      <v-expansion-panel-content class="expansion-panel-content-custom">
        <v-card tile flat>
          <v-row
              v-for="(value, key) in param.new_values" :key="key"
              @keyup.alt.enter="deleteNewParam(param.baseParam.id, value)"
              no-gutters
              class="flex-nowrap"
          >
            <record-input
              :param="getParam(param, value)"
              :type="param.baseParam.type"
              @deletable="deleteNewParam(param.baseParam.id, value)"
            ></record-input>
          </v-row>
          <old-records
              :base="param.baseParam"
              :values="param.values"
              :title="title"
              :settings="settings"
              @addDocToGraph="addDocToGraph"
          ></old-records>
        </v-card>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script>
import RecordTitle from "@/components/Graph/GraphMenu/Create/Record/RecordTitle";
import RecordInput from "@/components/Graph/GraphMenu/Create/Record/RecordInput";
import DropDownMenu from "@/components/WebsiteShell/CustomComponents/dropDownMenu";
import MenuDateTime from "@/components/WebsiteShell/CustomComponents/DateTimePickers/selectDateTime";
import OldRecords from "@/components/Graph/GraphMenu/Create/Record/OldRecords";
import _ from 'lodash';

export default {
  name: "RecordArea",
  components: {OldRecords, RecordInput, RecordTitle, MenuDateTime, DropDownMenu},
  props: {
    settings: Object,
    params: Array,
    title: {
      type: String,
      default: null
    }
  },
  data: () => ({
    openedPanels: []
  }),
  methods: {
    getParam(param, value) {
      if(param.baseParam.title === 'geometry' && param.values.length > 0){
        let copyGeometry = _.cloneDeep(param.values[0])
        value.value = JSON.parse(copyGeometry.value)
      }
      return value
    },
    addDocToGraph(doc) {
      this.$emit('addDocumentToGraph', doc)
    },
    createNewParam(id) {
      this.$emit('createNewParam', id)
    },
    deleteNewParam(id, param) {
      this.$emit('deleteNewParam', { id: id, param: param })
    },
  },
  mounted() {
    this.openedPanels = [...Array(this.params.length).keys()]
  },
  watch: {
    params: function (value) { this.openedPanels = [...Array(value.length).keys()] }
  }
}
</script>

<style scoped>
.v-expansion-panel >>> .v-expansion-panel-header {
  min-height: 35px;
}
.expansion-panel-content-custom >>> .v-expansion-panel-content__wrap {
  padding: 0 8px;
}
</style>