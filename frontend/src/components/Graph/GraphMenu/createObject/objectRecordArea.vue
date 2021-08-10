<template>
  <v-expansion-panels v-model="openedPanels" multiple accordion hover focusable tile style="border-bottom: 1px solid rgba(0, 0, 0, 0.20)">
    <v-expansion-panel v-for="(classifier, key) in classifiers" :key="key">
      <record-title
        :title="getClassifierObject(classifier.id).title"
        :opened="openedPanels.includes(key)"
        @createNewParam="createNewParam(classifier.id)"
      ></record-title>
      <v-expansion-panel-content eager class="expansion-panel-content-custom">
        <v-card tile flat>
          <v-row v-for="param in classifier.new_values" no-gutters class="flex-nowrap">
            <record-input :param="param" @deletable="deleteNewParam(classifier.id, param)" :type="getClassifierObject(classifier.id).type" :list="getClassifierObject(classifier.id).list_id"></record-input>
          </v-row>
          <table style="width: 100%; color: #757575; border-spacing: initial" class="py-2">
            <tbody>
              <tr v-for="i in 3">
                <td style="height: 0.9em">
                  <span style="font-size: 0.8em">Старое значение {{i}} Старое значение {{i}} Старое значение {{i}} Старое значение {{i}}</span>
                </td>
                <td class="text-end text-no-wrap pl-3" style="height: 0.9em;">
                  <span style="font-size: 0.8em">Старая дата {{i}}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </v-card>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script>
import TextInput from "../../../WebsiteShell/InputForms/textInput"
import GeometryInput from "../../../WebsiteShell/InputForms/geometryInput"
import DropDownMenu from "../../../WebsiteShell/InputForms/BodyToForm/dropDownMenu"
import MenuDateTime from "../../../WebsiteShell/InputForms/InputFormsUI/menuDateTime"
import SettingsAnalytics from "../../../Map/MapMenu/scriptsPage/settingsAnalytics"
import {mapActions, mapGetters} from "vuex"
import RecordTitle from "./objectRecordComponents/recordTitle";
import RecordInput from "./objectRecordComponents/recordInput";

export default {
  name: "objectRecordArea",
  components: {RecordInput, RecordTitle, SettingsAnalytics, MenuDateTime, DropDownMenu, GeometryInput, TextInput},
  props: {
    classifiers: Array,
  },
  computed: {
    ...mapGetters(['classifierObject', 'editableObject']),
    openedPanels: {
      get: function () {
        return [...Array(this.classifiers.length).keys()]
      },
      set: function (value) {
        this.openedPanels.splice(this.openedPanels.findIndex(item => item === value), 1)
      }
    }
  },
  methods: {
    ...mapActions(['addNewParamEditableObject', 'deleteNewParamEditableObject', ]),
    getClassifierObject(classifierId) {
      return this.classifierObject({ objectId: this.editableObject.object_id, classifierId: classifierId})
    },
    createNewParam(classifierId) {
      this.addNewParamEditableObject(classifierId)
    },
    deleteNewParam(classifierId, param) {
      this.deleteNewParamEditableObject({classifierId: classifierId, param: param})
    }
  }
}
</script>

<style scoped>
.v-expansion-panel--active >>> .v-expansion-panel-header {
  min-height: 48px;
}
.expansion-panel-content-custom >>> .v-expansion-panel-content__wrap {
  padding: 0 8;
}
</style>