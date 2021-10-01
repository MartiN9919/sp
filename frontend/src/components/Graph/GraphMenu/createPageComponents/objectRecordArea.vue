<template>
  <v-expansion-panels v-model="openedPanels" multiple accordion hover focusable tile>
    <v-expansion-panel v-for="(param, key) in params" :key="key">
      <record-title
        :title="param.baseParam.title"
        :opened="openedPanels.includes(key)"
        @createNewParam="createNewParam(param.baseParam.id)"
      ></record-title>
      <v-expansion-panel-content class="expansion-panel-content-custom">
        <v-card tile flat>
          <v-row v-for="(value, key) in param.new_values" :key="key" no-gutters class="flex-nowrap">
            <record-input
              :param="value"
              :type="param.baseParam.type"
              @deletable="deleteNewParam(param.baseParam.id, value)"
            ></record-input>
          </v-row>
          <table>
            <tbody class="py-2">
              <custom-tooltip
                v-for="(item, key) in param.values" :key="key"
                v-if="checkTypeParam(param) === 'file_photo'"
                :body-text="item.value"
                :settings="settings"
                bottom
              >
                <template v-slot:activator="{ on }">
                  <tr v-on="on">
                    <td>
                      <a :href="getDownloadLink(item.value)">{{item.value}}</a>
                    </td>
                    <td class="text-end text-no-wrap pl-3"><span>{{item.date}}</span></td>
                  </tr>
                </template>
              </custom-tooltip>
            <tr v-for="item in param.values" v-else>
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
import CustomTooltip from "../../../WebsiteShell/UI/customTooltip"
import {getDownloadFileLink} from '@/plugins/axios_settings'

export default {
  name: "objectRecordArea",
  components: {CustomTooltip, RecordInput, RecordTitle, MenuDateTime, DropDownMenu},
  props: {
    settings: Object,
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
    checkTypeParam(param) {
      if(param.baseParam.hasOwnProperty('type'))
        return param.baseParam.type
    },
    createNewParam(id) {
      this.$emit('createNewParam', id)
    },
    deleteNewParam(id, param) {
      this.$emit('deleteNewParam', { id: id, param: param })
    },
    getDownloadLink(fileName) {
      return getDownloadFileLink(this.settings.objectId, this.settings.recId, fileName)
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
  border-spacing: initial;
  cursor: default;
}
span, a {
  color: #555555;
  font-size: 0.8em;
  text-decoration: none;
}
tr:hover a, tr:hover span {
  color: #009688;
}
.v-expansion-panel >>> .v-expansion-panel-header {
  min-height: 35px;
}
.expansion-panel-content-custom >>> .v-expansion-panel-content__wrap {
  padding: 0 8px;
}
</style>