<template>
  <v-dialog v-model="dialog" persistent @click:outside="close" width="40%">
    <template v-slot:activator="{ on, attrs }">
      <v-card-actions>
        <v-btn v-on="on" v-bind="attrs" outlined color="teal" width="100%">
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
          <boolean-input v-model="object.actual" label="Поиск только по актуальным значениям"/>
          <date-input v-model="object.relDateTimeStart" :dropdown="false" clearable label="начала"/>
          <date-input v-model="object.relDateTimeEnd" :dropdown="false" clearable label="конца"/>
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
          <record-area :params="object.fields" item-value="value" search/>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import RecordArea from "@/components/Graph/GraphMenu/Create/Record/RecordArea"
import BooleanInput from "@/components/WebsiteShell/InputForms/booleanInput"
import DateInput from "@/components/WebsiteShell/InputForms/dateInput"

export default {
  name: "AdditionalSettings",
  components: {RecordArea, DateInput, BooleanInput},
  props: {
    object: Object,
    relationSetting: Boolean
  },
  data: () => ({
    dialog: false,
    valid: true
  }),
  methods: {
    clean() {
      this.object.cleanAdditionalSettings()
    },
    close() {
      if (this.valid) {
        this.dialog = false
      }
    }
  }
}
</script>

<style scoped>

</style>