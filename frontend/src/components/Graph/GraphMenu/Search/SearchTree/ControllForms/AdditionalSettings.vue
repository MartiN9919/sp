<template>
  <v-dialog width="40%">
    <template v-slot:activator="{ on, attrs }">
      <v-card-actions>
        <v-btn v-on="on" v-bind="attrs" outlined color="teal" width="100%">Дополнительные настройки</v-btn>
      </v-card-actions>
    </template>
    <v-card>
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
      <v-card-title>
        Настройка полей
      </v-card-title>
      <v-card-subtitle>
        Указать явные поля, по которым осуществлять поиск
      </v-card-subtitle>
      <v-card-text>
        <record-area :params="object.fields"/>
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
  }
}
</script>

<style scoped>

</style>