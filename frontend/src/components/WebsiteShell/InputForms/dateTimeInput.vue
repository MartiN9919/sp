<template>
  <div class="datetime-input-form">
    <drop-down-menu min-width="auto" offset-y close-on-click :close-on-content-click="false">
      <template v-slot:activator="{ on }">
        <div v-on="on">
          <body-input-form
            v-model="value"
            v-bind="$attrs"
            :rules="rulesDateTime"
            :class="bodyInputClasses"
            :placeholder="$attrs.placeholder || 'Выберете необходимую дату и время'"
            @deletable="$emit('deletable')"
            readonly
          >
            <template v-slot:append="{ hover }">
              <v-icon size="24">mdi-calendar-clock</v-icon>
            </template>
            <template v-slot:message>
              <slot name="message"></slot>
            </template>
          </body-input-form>
        </div>
      </template>
      <template v-slot:body="{ closeMenu, status }">
        <select-date-time v-if="status" v-model="value" :close-menu="closeMenu"></select-date-time>
      </template>
    </drop-down-menu>
  </div>
</template>

<script>
import BodyInputForm from "../UI/bodyInputForm"
import DropDownMenu from "../UI/dropDownMenu"
import SelectDateTime from "../UI/selectDateTime"

export default {
  name: "dateTimeInput",
  components: {BodyInputForm, DropDownMenu, SelectDateTime},
  model: { prop: 'inputString', event: 'changeInputString'},
  props: {
    inputString: String,
  },
  computed: {
    bodyInputClasses: function () { return this.$attrs.hasOwnProperty('label') ? '' : 'pt-0' },
    rulesDateTime : function () {
      if (this.value) {
        let dateTimeRule = [v => (v || '').split(' ').length > 1 || 'Введите все значения']
        return this.$attrs.hasOwnProperty('rules') ? dateTimeRule.concat(this.$attrs.rules) : dateTimeRule
      }
      else return this.$attrs.rules
    },
    value: {
      get: function () { return this.inputString },
      set: function (val) { this.$emit('changeInputString', val) }
    },
  },

}
</script>

<style scoped>
.datetime-input-form >>> input {
  cursor: pointer;
}
.datetime-input-form >>> .v-input__slot {
  cursor: pointer;
}
.datetime-input-form {
  width: 100%;
}
</style>