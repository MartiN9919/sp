<template>
  <custom-tooltip
      :description="base.hint"
      :value="value"
      :type="base.type"
      nudge-right="20"
      right
  >
    <template v-slot:activator="{ on }">
      <div v-on="on" class="w-100">
        <responsive-input-form
          v-model="value"
          v-bind="$attrs"
          :inputType="base.type"
          :listRules="['notEmpty']"
          :readonly="readOnly"
          deletable
          class="pt-1"
          :class="inputClass"
          @deletable="$emit('deletable')"
        >
          <template v-slot:message>
            <drop-down-menu
              max-width="300"
              min-width="300"
              nudge-left="300"
              offset-x
              offset-y
              eager
              :close-on-content-click="false"
              z-index="10004"
            >
              <template v-slot:activator="{ on }">
                <div v-on="on" class="v-messages text-no-wrap selector-date-time">
                  {{param.date}}
                </div>
              </template>
              <template v-slot:body>
                <select-period v-if="search" v-model="param.date"/>
                <select-date-time v-else v-model="param.date"/>
              </template>
            </drop-down-menu>
          </template>
        </responsive-input-form>
      </div>
    </template>
  </custom-tooltip>
</template>

<script>
import ResponsiveInputForm from "@/components/WebsiteShell/CustomComponents/responsiveInputForm"
import DropDownMenu from "@/components/WebsiteShell/CustomComponents/dropDownMenu"
import SelectDateTime from "@/components/WebsiteShell/CustomComponents/DateTimePickers/selectDateTime"
import {mapGetters} from "vuex";
import CustomTooltip from "@/components/WebsiteShell/CustomComponents/Tooltip/customTooltip";
import SelectPeriod from "@/components/WebsiteShell/CustomComponents/DateTimePickers/selectPeriod";

export default {
  name: "RecordInput",
  components: {SelectPeriod, CustomTooltip, DropDownMenu, SelectDateTime, ResponsiveInputForm},
  props: {
    param: Object,
    base: Object,
    conflict: Boolean,
    search: Boolean
  },
  computed: {
    ...mapGetters(['editableObjects', 'baseList', 'baseLists']),
    readOnly: function () {
      if(this.conflict && this.editableObjects.length > 1) {
        return !!this.editableObjects[0].params.find(p => p.values.find(v => v === this.param))
      }
      else {
        return false
      }
    },
    value: {
      get: function () {
        return this.param.value
      },
      set: function (value) {
        this.setDepend(value)
        this.param.value = value
      }
    },
    inputClass: function () {
      return this.readOnly ? 'readOnly' : ''
    }
  },
  methods: {
    setDepend(value) {
      if(this.base.type.title === 'list') {
        const findValue = this.baseList(this.base.type.value).values.find(v => v.id === value)
        if(findValue && findValue.parent_id) {
          this.$emit('depend',{
            parent: findValue.parent_id,
            list: Object.entries(this.baseLists)
                .find(([id, list]) => list.values
                    .find(v => v.id === findValue.parent_id)
                )
          })
        }
      }
    }
  },
  mounted() {
    this.setDepend(this.param.value)
  }
}
</script>

<style scoped>
.selector-date-time {
  font-size: 1.06em;
  padding-top: 1px;
  cursor: pointer;
  color: #004D40;
  margin-left: auto;
  width: fit-content;
}
.readOnly >>> input {
  color: teal
}
</style>