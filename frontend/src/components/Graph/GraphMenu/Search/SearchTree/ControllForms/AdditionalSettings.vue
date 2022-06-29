<template>
  <v-dialog v-model="dialog" persistent scrollable width="40%">
    <template v-slot:activator="{ on, attrs }">
      <v-card-actions>
        <v-btn v-on="on" v-bind="attrs" :disabled="disabled" outlined color="teal" width="100%">
          Дополнительные настройки
          <v-btn v-if="object.isAdditionalSettings" @click.stop="clean" icon color="error">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-btn>
      </v-card-actions>
    </template>
    <v-card>
      <template v-if="relationSetting">
        <v-card-title>
          Настройки связи
        </v-card-title>
        <v-card-subtitle>
          Расширенные настройки связи поля с вышестоящим
        </v-card-subtitle>
        <v-card-text>
          <boolean-input v-model="copyObject.actual" label="Поиск только по актуальным значениям"/>
          <date-input v-model="copyObject.relDateTimeStart" :dropdown="false" clearable label="начала"/>
          <date-input v-model="copyObject.relDateTimeEnd" :dropdown="false" clearable label="конца"/>
        </v-card-text>
        <v-divider/>
      </template>
      <v-card-title>
        Настройка полей
      </v-card-title>
      <v-card-subtitle>
        Указать явные поля, по которым осуществлять поиск
      </v-card-subtitle>
      <v-card-text>
        <v-form ref="form" v-model="valid" onSubmit="return false;" autofocus>
          <record-area v-if="copyObject" :params="copyObject.fields" item-value="value" search/>
        </v-form>
      </v-card-text>
      <control-menu :buttons="buttons" @confirm="confirm" @cancel="cancel"/>
    </v-card>
  </v-dialog>
</template>

<script>
import RecordArea from "@/components/Graph/GraphMenu/Create/Record/RecordArea"
import BooleanInput from "@/components/WebsiteShell/InputForms/booleanInput"
import DateInput from "@/components/WebsiteShell/InputForms/dateInput"
import ControlMenu from "@/components/Graph/GraphMenu/Create/Modules/ControlMenu"
import _ from 'lodash'

export default {
  name: "AdditionalSettings",
  components: {ControlMenu, RecordArea, DateInput, BooleanInput},
  props: {
    object: Object,
    relationSetting: Boolean,
    disabled: Boolean
  },
  data: () => ({
    dialogState: false,
    valid: true,
    copyObject: null,
  }),
  computed: {
    dialog: {
      get: function () {
        return this.dialogState
      },
      set: function (value) {
        if(value) {
          this.copyObject = _.cloneDeep(this.object)
        }
        this.dialogState = value
      }
    },
    buttons: function () {
      return [
        {action: 'cancel', title: 'Отмена', disabled: true},
        {action: 'confirm', title: 'Готово', disabled: this.valid},
      ]
    },
  },
  methods: {
    clean() {
      this.object.cleanAdditionalSettings()
    },
    cancel() {
      this.dialog = false
    },
    confirm() {
      Object.assign(this.object, this.copyObject)
      this.dialog = false
    }
  }
}
</script>

<style scoped>

</style>