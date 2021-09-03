<template>
  <v-expansion-panels v-model="openedPanels" multiple accordion hover focusable tile>
    <v-expansion-panel v-for="(item, key) in params" :key="key">
      <record-title
        :title="item.baseParam.title"
        :opened="openedPanels.includes(key)"
        @createNewParam="createNewParam(item.baseParam.id)"
      ></record-title>
      <v-expansion-panel-content class="expansion-panel-content-custom">
        <v-card tile flat>
          <v-row v-for="param in item.new_values" no-gutters class="flex-nowrap">
            <record-input
              :param="param"
              :type="item.baseParam.type"
              :list="item.baseParam.list"
              @deletable="deleteNewParam(item.baseParam.id, param)"
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
    params: Array,
    type: {
      type: Boolean,
      default: false
    }
  },
  data: () => ({
    openedPanels: []
  }),
  methods: {
    createNewParam(id) {
      this.$emit('createNewParam', id)
    },
    deleteNewParam(id, param) {
      this.$emit('deleteNewParam', { id: id, param: param })
    }
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
  min-height: 35px;
}
.expansion-panel-content-custom >>> .v-expansion-panel-content__wrap {
  padding: 0 8;
}
</style>