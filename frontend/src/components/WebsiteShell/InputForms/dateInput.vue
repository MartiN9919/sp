<template>
  <drop-down-menu
    max-width="300"
    nudge-left="300"
    offset-x
    offset-y
    :close-on-click="false"
    :close-on-content-click="false"
  >
    <template v-slot:activator="{ openMenu, closeMenu }">
      <body-input-form
        v-model="value"
        v-bind="$attrs"
        :on="{focus: openMenu, blur: closeMenu}"
        :class="bodyInputClasses"
        :rules="rulesDate"
        :icon="dateIcon"
        :placeholder="placeholder"
        v-mask="dateMask"
        @deletable="$emit('deletable')"
      >
        <template v-slot:message>
          <slot name="message"/>
        </template>
      </body-input-form>
    </template>
    <template v-slot:body>
      <select-date v-model="value" @isValid="dateValid" onmousedown="return false"/>
    </template>
  </drop-down-menu>
</template>

<script>
import BodyInputForm from "@/components/WebsiteShell/CustomComponents/bodyInputForm"
import DropDownMenu from "@/components/WebsiteShell/CustomComponents/dropDownMenu"
import SelectDate from "@/components/WebsiteShell/CustomComponents/DateTimePickers/selectDate"

export default {
  name: "dateInput",
  components: {BodyInputForm, DropDownMenu, SelectDate},
  model: { prop: 'inputString', event: 'changeInputString'},
  props: {
    inputString: String,
  },
  data: () => ({
    date: '',
    isDateValid: false,
    dateIcon: 'mdi-calendar',
    dateMask: [/[0-3]/, /\d/, '.', /[0-1]/, /\d/, '.', /[1-2]/, /\d/, /\d/, /\d/],
  }),
  computed: {
    bodyInputClasses: function () { return this.$attrs.hasOwnProperty('label') ? '' : 'pt-0' },
    placeholder: function () { return this.$attrs.placeholder || 'Выберете необходимую дату' },
    rulesDate : function () {
      if (this.value) {
        let dateRule = [() => this.isDateValid || 'Введите корректную дату']
        return this.$attrs.hasOwnProperty('rules') ? dateRule.concat(this.$attrs.rules) : dateRule
      }
      else return this.$attrs.rules
    },
    value: {
      get: function () {
        this.$emit('changeInputString', this.isDateValid ? this.date : '')
        return this.date
      },
      set: function (value) {
        this.date = value
      },
    },
  },
  methods: {
    dateValid(value) {
      this.isDateValid = value
    },
  }
}
</script>

<style scoped>
.date-input-form {
  width: 100%;
}
</style>