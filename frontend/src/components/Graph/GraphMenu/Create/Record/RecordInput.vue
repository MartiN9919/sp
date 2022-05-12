<template>
  <responsive-input-form
    v-model="param.value"
    :inputType="type"
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
      >
        <template v-slot:activator="{ on }">
          <div v-on="on" class="v-messages text-no-wrap selector-date-time">
            {{param.date}}
          </div>
        </template>
        <template v-slot:body>
          <select-date-time v-model="param.date"/>
        </template>
      </drop-down-menu>
    </template>
  </responsive-input-form>
</template>

<script>
import ResponsiveInputForm from "@/components/WebsiteShell/CustomComponents/responsiveInputForm"
import DropDownMenu from "@/components/WebsiteShell/CustomComponents/dropDownMenu"
import SelectDateTime from "@/components/WebsiteShell/CustomComponents/DateTimePickers/selectDateTime"
import {mapGetters} from "vuex";

export default {
  name: "RecordInput",
  components: {DropDownMenu, SelectDateTime, ResponsiveInputForm},
  props: {
    param: Object,
    type: Object,
    conflict: Boolean
  },
  computed: {
    ...mapGetters(['editableObjects']),
    readOnly: function () {
      if(this.conflict && this.editableObjects.length > 1) {
        return !!this.editableObjects[0].params.find(p => p.values.find(v => v === this.param))
      }
      else {
        return false
      }
    },
    inputClass: function () {
      return this.readOnly ? 'readOnly' : ''
    }
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