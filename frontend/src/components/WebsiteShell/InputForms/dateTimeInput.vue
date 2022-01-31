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
        :rules="rulesDateTime"
        :icon="dateTimeIcon"
        :class="bodyInputClasses"
        :placeholder="placeholder"
        v-mask="dateTimeMask"
        @deletable="$emit('deletable')"
      >
        <template v-slot:message>
          <slot name="message"/>
        </template>
      </body-input-form>
    </template>
    <template v-slot:body>
      <select-date-time v-model="value" @isValid="dateTimeValid" onmousedown="return false"/>
    </template>
  </drop-down-menu>
</template>

<script>
import BodyInputForm from "@/components/WebsiteShell/CustomComponents/bodyInputForm"
import DropDownMenu from "@/components/WebsiteShell/CustomComponents/dropDownMenu"
import SelectDateTime from "@/components/WebsiteShell/CustomComponents/DateTimePickers/selectDateTime"

export default {
  name: "dateTimeInput",
  components: {BodyInputForm, DropDownMenu, SelectDateTime},
  model: { prop: 'inputString', event: 'changeInputString'},
  props: {
    inputString: String,
  },
  data: () => ({
    dateTime: '',
    isDateTimeValid: false,
    dateTimeIcon: 'mdi-calendar-clock',
    dateTimeMask: [/[0-3]/, /\d/, '.', /[0-1]/, /\d/, '.', /[1-2]/, /\d/, /\d/, /\d/, ' ', /[0-2]/, /[0-9]/, ':' , /[0-5]/, /[0-9]/],
  }),
  computed: {
    placeholder: function () { return this.$attrs.placeholder || 'Выберете необходимую дату и время' },
    bodyInputClasses: function () { return this.$attrs.hasOwnProperty('label') ? '' : 'pt-0' },
    rulesDateTime : function () {
      if (this.value) {
        let dateTimeRule = [() => this.isDateTimeValid || 'Введите все значения']
        return this.$attrs.hasOwnProperty('rules') ? dateTimeRule.concat(this.$attrs.rules) : dateTimeRule
      }
      else return this.$attrs.rules
    },
    value: {
      get: function () {
        this.$emit('changeInputString', this.isDateTimeValid ? this.dateTime : '')
        return this.dateTime
      },
      set: function (value) {
        this.dateTime = value
      }
    },
  },
  methods: {
    dateTimeValid(value) {
      this.isDateTimeValid = value
    }
  }
}
</script>

<style scoped>
.datetime-input-form {
  width: 100%;
}
</style>