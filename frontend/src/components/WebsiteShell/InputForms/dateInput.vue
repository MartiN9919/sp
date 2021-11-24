<template>
  <div class="date-input-form">
    <drop-down-menu min-width="auto" offset-y close-on-click :close-on-content-click="false">
      <template v-slot:activator="{ on }">
        <div v-on="on">
          <body-input-form
            v-model="value"
            v-bind="$attrs"
            :class="bodyInputClasses"
            icon="mdi-calendar"
            :placeholder="$attrs.placeholder || 'Выберете необходимую дату'"
            @deletable="$emit('deletable')"
            readonly
          >
            <template v-slot:message>
              <slot name="message"></slot>
            </template>
          </body-input-form>
        </div>
      </template>
      <template v-slot:body="{ closeMenu,  status }">
        <select-date v-if="status" v-model="value" :close-menu="closeMenu"></select-date>
      </template>
    </drop-down-menu>
  </div>
</template>

<script>
import BodyInputForm from "@/components/WebsiteShell/CustomComponents/bodyInputForm"
import DropDownMenu from "@/components/WebsiteShell/CustomComponents/dropDownMenu"
import SelectDate from "@/components/WebsiteShell/CustomComponents/selectDate"

export default {
  name: "dateInput",
  components: {BodyInputForm, DropDownMenu, SelectDate},
  model: { prop: 'inputString', event: 'changeInputString'},
  props: {
    inputString: String,
  },
  computed: {
    bodyInputClasses: function () { return this.$attrs.hasOwnProperty('label') ? '' : 'pt-0' },
    value: {
      get: function () { return this.inputString },
      set: function (value) { this.$emit('changeInputString', value) },
    },
  },
}
</script>

<style scoped>
.date-input-form >>> input {
  cursor: pointer;
}
.date-input-form >>> .v-input__slot {
  cursor: pointer;
}
.date-input-form {
  width: 100%;
}
</style>