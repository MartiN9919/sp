<template>
  <drop-down-menu
    max-width="300"
    min-width="300"
    nudge-left="300"
    eager
    offset-x
    offset-y
    z-index="10000002"
    :close-on-click="false"
    :close-on-content-click="false"
  >
    <template v-slot:activator="{ openMenu, closeMenu }">
      <body-input-form
        v-model="value"
        v-bind="$attrs"
        :on="{focus: openMenu, blur: closeMenu}"
        :class="classes"
        :rules="rules"
        :icon="formProps.icon"
        :placeholder="placeholder"
        v-facade="formProps.facade"
        @deletable="$emit('deletable')"
      >
        <template v-slot:message>
          <slot name="message"/>
        </template>
      </body-input-form>
    </template>
    <template v-slot:body>
      <component
        v-show="dropdown"
        :is="formProps.component"
        v-model="value"
        @isValid="validate"
        onmousedown="return false"
      />
    </template>
  </drop-down-menu>
</template>

<script>
import BodyInputForm from "@/components/WebsiteShell/CustomComponents/bodyInputForm"
import DropDownMenu from "@/components/WebsiteShell/CustomComponents/dropDownMenu"
const SelectDate = () => import("@/components/WebsiteShell/CustomComponents/DateTimePickers/selectDate")
const SelectDateTime = () => import("@/components/WebsiteShell/CustomComponents/DateTimePickers/selectDateTime")
const SelectPeriod = () => import("@/components/WebsiteShell/CustomComponents/DateTimePickers/selectPeriod")
import { facade } from 'vue-input-facade'

const dateProps = {
  component: 'SelectDate',
  icon: 'mdi-calendar',
  basePlaceholder: 'Выберете необходимую дату',
  errorMessage: 'Введите корректную дату',
  facade: '##.##.####',
}

const dateTimeProps = {
  component: 'SelectDateTime',
  icon: 'mdi-calendar-clock',
  basePlaceholder: 'Выберете необходимую дату и время',
  errorMessage: 'Введите все значения',
  facade: '##.##.#### ##:##',
}

const periodProps = {
  component: 'SelectPeriod',
  icon: 'mdi-calendar-range-outline',
  basePlaceholder: 'Выберете необходимый период',
  errorMessage: 'Введите все значения',
  facade: '##.##.####-##.##.####',
}

export default {
  name: "dateInput",
  directives: { facade },
  components: {BodyInputForm, DropDownMenu, SelectDate, SelectDateTime, SelectPeriod},
  model: { prop: 'inputString', event: 'changeInputString'},
  props: {
    inputString: String,
    dropdown: {
      type: Boolean,
      default: true
    }
  },
  data: () => ({
    string: '',
    isValid: true,
  }),
  computed: {
    formProps: function () {
      switch (this.$attrs['type-load']) {
        case 'date':
          return dateProps
        case 'datetime':
          return dateTimeProps
        case 'period':
          return periodProps
        default:
          return dateTimeProps
      }
    },
    classes: function () { return this.$attrs.hasOwnProperty('label') ? '' : 'pt-1' },
    placeholder: function () { return this.$attrs.placeholder || this.formProps.basePlaceholder },
    rules : function () {
      if (this.value) {
        let rule = [() => this.isValid || this.formProps.errorMessage]
        return this.$attrs.hasOwnProperty('rules') ? rule.concat(this.$attrs.rules) : rule
      }
      else return this.$attrs.rules
    },
    value: {
      get: function () {
        this.$emit('changeInputString', this.isValid ? this.string : '')
        return this.string
      },
      set: function (value) {
        this.string = value
      },
    },
  },
  methods: {
    validate(value) {
      this.isValid = value
    },
  },
  created() {
    this.value = this.inputString
  }
}
</script>

<style scoped>

</style>