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
              :param="getParam(param, value)"
              :type="param.baseParam.type"
              @deletable="deleteNewParam(param.baseParam.id, value)"
            ></record-input>
          </v-row>
          <table>
            <tbody class="py-2" v-if="checkTypeParam(param) === 'file_photo'">
              <custom-tooltip
                v-for="(item, key) in param.values" :key="key"
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
            </tbody>
            <tbody class="py-2" v-else>
              <tr v-for="item in param.values">
                <td v-if="checkTypeParam(param) === 'file_any'">
                  <a :href="getDownloadLink(item.value)">{{item.value}}</a>
                </td>
                <td v-else-if="checkTypeParam(param) === 'geometry'">
                  <v-dialog
                    style="z-index:1000002"
                    width="60%"
                    height="80%"
                    v-model="dialog"
                    @keydown.esc="dialog = false"
                    persistent
                    transition="dialog-bottom-transition"
                  >
                    <template v-slot:activator="{ on, attrs }">
                      <span v-bind="attrs" v-on="on">
                        Геометрия
                      </span>
                    </template>

                    <v-card>
                      <v-card-title class="text-h7">УКАЗАТЬ ЗДЕСЬ TITLE</v-card-title>
                      <v-divider></v-divider>
                      <LeafletViewer
                        v-if="dialog"
                        style="height: 70vh;"
                        :fc="JSON.parse(item.value)"
                        :controls="true"
                      />
                      <v-divider></v-divider>
                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn :color="$CONST.APP.COLOR_OBJ" text @click="dialog=false">Ок</v-btn>
                      </v-card-actions>
                    </v-card>

                  </v-dialog>
                </td>
                <td v-else><span>{{item.value ? item.value : 'Создана'}}</span></td>
                <td class="text-center" @click="addDocumentToGraph(item.doc)" style="cursor: pointer"><span>{{item.doc ? item.doc.title : ''}}</span></td>
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
import RecordTitle from "@/components/Graph/GraphMenu/createPageComponents/objectRecordComponents/recordTitle"
import RecordInput from "@/components/Graph/GraphMenu/createPageComponents/objectRecordComponents/recordInput"
import DropDownMenu from "@/components/WebsiteShell/CustomComponents/dropDownMenu"
import MenuDateTime from "@/components/WebsiteShell/CustomComponents/selectDateTime"
import CustomTooltip from "@/components/WebsiteShell/CustomComponents/customTooltip"
import LeafletViewer from "@/components/Map/Leaflet/LeafletViewer"
import {getDownloadFileLink} from '@/plugins/axiosSettings'
import _ from 'lodash'

export default {
  name: "objectRecordArea",
  components: {CustomTooltip, RecordInput, RecordTitle, MenuDateTime, DropDownMenu, LeafletViewer},
  props: {
    settings: Object,
    params: Array,
  },
  data: () => ({
    dialog: false,
    openedPanels: []
  }),
  methods: {
    getParam(param, value) {
      if(this.checkTypeParam(param) === 'geometry' && param.values.length > 0){
        let copyGeometry = _.cloneDeep(param.values[0])
        value.value = JSON.parse(copyGeometry.value)
      }
      return value
    },
    addDocumentToGraph(doc) {
      this.$emit('addDocumentToGraph', {objectId: doc.object_id, recId: doc.rec_id})
    },
    checkTypeParam(param) {
      if(param.baseParam.hasOwnProperty('type'))
        return param.baseParam.type.title
    },
    createNewParam(id) {
      this.$emit('createNewParam', id)
    },
    deleteNewParam(id, param) {
      this.$emit('deleteNewParam', { id: id, param: param })
    },
    getDownloadLink(fileName) {
      return getDownloadFileLink(this.settings.objectId, this.settings.recId, fileName)
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
tr {
  line-height: normal;
  border-spacing: initial;
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