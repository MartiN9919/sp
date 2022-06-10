<template>
  <v-card flat>
    <v-card-text v-if="copyItem">
      <selector-input v-if="!item.recId" v-model="copyItem.objectId" :items="baseObjects" :label="selectorTitle" item-text="titleSingle"/>
      <boolean-input v-model="copyItem.actual" :label="booleanTitle" class="pt-4"/>
    </v-card-text>
    <additional-settings v-if="copyItem" :object="copyItem"/>
    <control-menu :buttons="buttons" @confirm="confirm" @cancel="cancel"/>
  </v-card>
</template>

<script>
import SelectorInput from "@/components/WebsiteShell/InputForms/selectorInput"
import BooleanInput from "@/components/WebsiteShell/InputForms/booleanInput"
import ControlMenu from "@/components/Graph/GraphMenu/Create/Modules/ControlMenu"
import {SearchTreeRootItem} from "@/store/modules/graph/searchTree"
import {mapGetters} from "vuex"
import _ from "lodash"
import AdditionalSettings from "@/components/Graph/GraphMenu/Search/SearchTree/ControllForms/AdditionalSettings";

export default {
  name: "FormChange",
  components: {AdditionalSettings, ControlMenu, SelectorInput, BooleanInput},
  props: {
    item: SearchTreeRootItem,
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
