<template>
  <v-card flat>
    <v-card-text v-if="copyItem">
      <selector-input v-model="copyItem.baseId" :items="baseObjects" :label="selectorTitle" multiple item-text="titleSingle"/>
      <boolean-input v-model="copyItem.actual" :label="booleanTitle" class="pt-4"/>
    </v-card-text>
    <additional-settings v-if="copyItem" :object="copyItem" :disabled="copyItem.baseId.length > 1"/>
    <control-menu :buttons="buttons" @confirm="confirm" @cancel="cancel"/>
  </v-card>
</template>

<script>
import SelectorInput from "@/components/WebsiteShell/InputForms/selectorInput"
import BooleanInput from "@/components/WebsiteShell/InputForms/booleanInput"
import ControlMenu from "@/components/Graph/GraphMenu/Create/Modules/ControlMenu"
import AdditionalSettings from "@/components/Graph/GraphMenu/Search/SearchTree/ControllForms/AdditionalSettings"
import {SearchTreeMain} from "@/store/modules/graph/searchTree"
import {mapGetters} from "vuex"
import _ from "lodash"

export default {
  name: "FormChange",
  components: {AdditionalSettings, ControlMenu, SelectorInput, BooleanInput},
  props: {
    item: SearchTreeMain,
  },
  data: () => ({
    copyItem: null,
    booleanTitle: 'Поиск только по актуальным значениям',
    selectorTitle: 'Выбор типа объекта',
    buttons: [
      {action: 'cancel', title: 'Отмена', disabled: true},
      {action: 'confirm', title: 'Готово', disabled: true},
    ],
  }),
  computed: mapGetters(['baseObjects']),
  methods: {
    confirm() {
      this.$emit('confirm', this.copyItem)
      this.cancel()
    },
    cancel() {
      this.$emit('cancel')
    }
  },
  mounted() {
    this.copyItem = _.cloneDeep(this.item)
  },
}
</script>
