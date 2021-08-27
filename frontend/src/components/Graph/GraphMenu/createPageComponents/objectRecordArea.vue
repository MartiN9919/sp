<template>
  <v-expansion-panels v-model="openedPanels" multiple accordion hover focusable tile>
    <v-expansion-panel v-for="(item, key) in classifiers" :key="key">
      <record-title
        :title="item.classifier.title"
        :opened="openedPanels.includes(key)"
        @createNewParam="createNewParam(item.classifier.id)"
      ></record-title>
      <v-expansion-panel-content eager class="expansion-panel-content-custom">
        <v-card  tile flat>
          <v-row v-for="param in item.new_values" no-gutters class="flex-nowrap">
            <record-input
              :param="param"
              :type="item.classifier.type"
              :list="item.classifier.list"
              @deletable="deleteNewParam(item.classifier.id, param)"
            ></record-input>
          </v-row>
          <table>
            <tbody class="py-2">
            <tr v-for="item in item.values">
              <td><span>{{item.value ? item.value : 'Создана'}}</span></td>
              <td class="text-end text-no-wrap pl-3"><span>{{item.date}}</span></td>
            </tr>
            </tbody>
          </table>
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
import TableOldValues from "./objectRecordComponents/tableOldValues"
import {mapGetters} from "vuex"

export default {
  name: "objectRecordArea",
  components: {TableOldValues, RecordInput, RecordTitle, MenuDateTime, DropDownMenu},
  props: {
    classifiers: Array,
    type: {
      type: Boolean,
      default: false
    }
  },
  data: () => ({
    openedPanels: []
  }),
  methods: {
    createNewParam(classifierId) {
      this.$emit('createNewParam', classifierId)
    },
    deleteNewParam(classifierId, param) {
      this.$emit('deleteNewParam', { classifierId: classifierId, param: param })
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
table {
  width: 100%;
  color: #757575;
  border-spacing: initial;
}
td {
  height: 0.9em
}
span {
  font-size: 0.8em
}
.v-expansion-panel >>> .v-expansion-panel-header {
  min-height: 32px;
}
.expansion-panel-content-custom >>> .v-expansion-panel-content__wrap {
  padding: 0 8;
}
</style>