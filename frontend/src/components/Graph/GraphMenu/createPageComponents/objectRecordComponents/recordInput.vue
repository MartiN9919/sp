<template>
  <v-col>
    <responsive-input-form
      v-model="param.value"
      :inputType="type"
      :listRules="['notEmpty']"
      deletable
      class="pt-1"
      @deletable="$emit('deletable')"
    >
      <template v-slot:message>
        <drop-down-menu min-width="auto" left offset-y close-on-click :close-on-content-click="false">
          <template v-slot:activator="{ on }">
            <div v-on="on" class="v-messages text-no-wrap selector-date-time">
              {{param.date}}
            </div>
          </template>
          <template v-slot:body="{ closeMenu, status }">
            <select-date-time v-if="status" v-model="param.date" :close-menu="closeMenu"/>
          </template>
        </drop-down-menu>
      </template>
    </responsive-input-form>
  </v-col>
</template>

<script>
import ResponsiveInputForm from "@/components/WebsiteShell/CustomComponents/responsiveInputForm"
import DropDownMenu from "@/components/WebsiteShell/CustomComponents/dropDownMenu"
import SelectDateTime from "@/components/WebsiteShell/CustomComponents/DateTimePickers/selectDateTime"

export default {
  name: "recordInput",
  components: {DropDownMenu, SelectDateTime, ResponsiveInputForm},
  props: {
    param: Object,
    type: Object,
  },
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
</style>