<template>
  <v-card flat>
    <v-card-text>
      <selector-input
        v-model="objectId"
        :items="baseObjects"
        :label="selectorTitle"
        item-text="titleSingle"
      />
      <boolean-input
        v-model="objectActual"
        :label="booleanTitle"
        class="pt-4"
      />
    </v-card-text>
    <v-divider/>
    <v-card-actions class="justify-space-between">
      <v-btn
        v-for="(button, key) in actionButtons"
        :key="key"
        @click="buttonHandler(button.action)"
        outlined color="teal" width="40%"
      >
        {{ button.title }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import SelectorInput from "@/components/WebsiteShell/InputForms/selectorInput"
import BooleanInput from "@/components/WebsiteShell/InputForms/booleanInput"
import {mapGetters} from "vuex"
import _ from "lodash"

export default {
  name: "FormChange",
  components: {SelectorInput, BooleanInput},
  props: {
    objectSettings: Object,
  },
  data: () => ({
    newSettingsObject: null,
    booleanTitle: 'Поиск только по актуальным значениям',
    selectorTitle: 'Выбор типа объекта',
    actionButtons: [
      { action: 'cancel', title: 'Отмена' },
      { action: 'confirm', title: 'Готово' },
    ],
  }),
  computed: {
    ...mapGetters(['baseObjects']),
    objectId: {
      get: function () {
        return this.newSettingsObject ? this.newSettingsObject.object_id : null
      },
      set: function (newObjectId) {
        this.newSettingsObject.object_id = newObjectId
      },
    },
    objectActual: {
      get: function () {
        return this.newSettingsObject ? this.newSettingsObject.actual : null
      },
      set: function (newObjectActual) {
        if(this.newSettingsObject) {
          this.newSettingsObject.actual = newObjectActual
        }
      },
    }
  },
  methods: {
    buttonHandler(event) {
      if (event === 'confirm') {
        this.$emit('confirm', this.newSettingsObject)
      }
      this.$emit('cancel')
    },
  },
  mounted() {
    this.newSettingsObject = _.clone(this.objectSettings)
  },
}
</script>
