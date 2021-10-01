<template>
  <component
    :is="selectComponent"
    v-model="value"
    :type-value="typeTitle"
    :type-load="typeValue"
    :rules="activeRules"
    v-bind="$attrs"
    @deletable="$emit('deletable')"
  >
    <template v-slot:message>
      <slot name="message"></slot>
    </template>
  </component>
</template>

<script>
import geometryInput from "@/components/WebsiteShell/InputForms/geometryInput"
import booleanInput from "@/components/WebsiteShell/InputForms/booleanInput"
import dateInput from "@/components/WebsiteShell/InputForms/dateInput"
import dateTimeInput from "@/components/WebsiteShell/InputForms/dateTimeInput"
import numberInput from "@/components/WebsiteShell/InputForms/numberInput"
import textInput from "@/components/WebsiteShell/InputForms/textInput"
import selectorInput from "@/components/WebsiteShell/InputForms/selectorInput"
import phoneInput from "@/components/WebsiteShell/InputForms/phoneInput"
import fileInput from "@/components/WebsiteShell/InputForms/fileInput"
import searchInput from "@/components/WebsiteShell/InputForms/searchInput"
import unknownInput from "@/components/WebsiteShell/InputForms/unknownInput"

export default {
  name: 'responsiveInputForm',
  inheritAttrs: false,
  components: {
    searchInput,
    phoneInput,
    geometryInput,
    booleanInput,
    dateInput,
    dateTimeInput,
    numberInput,
    textInput,
    selectorInput,
    fileInput,
    unknownInput
  },
  props: {
    inputString: [
      String,
      Object,
      Boolean,
      Array,
      Number,
      Function
    ],
    inputType: [
      Object
    ],
    listRules: {
      type: Array,
      default: function () {
        return []
      }
    }
  },
  model: {
    prop: 'inputString',
    event: 'changeInputString'
  },
  data: () => ({
    generalRules: {
      notEmpty: v => !!v || 'Поле должно быть заполнено'
    },
    components: {
      list: 'selectorInput',
      search: 'searchInput',
      text: 'textInput',
      geometry: 'geometryInput',
      checkbox: 'booleanInput',
      date: 'dateInput',
      datetime: 'dateTimeInput',
      number: 'numberInput',
      phone_number: 'phoneInput',
      file_photo: 'fileInput',
      file_any: 'fileInput',
      default: 'unknownInput'
    }
  }),
  computed: {
    activeRules: function () {
      return Array.from(this.listRules, rule => this.generalRules[rule])
    },
    selectComponent: function () {
      return this.inputType ? this.components[this.inputType.title] : this.components.default
    },
    typeTitle: function () {
      return this.inputType ? this.inputType.title : ''
    },
    typeValue: function () {
      return this.inputType ? this.inputType.value : ''
    },
    value: {
      get: function () { return this.inputString },
      set: function (value) { this.$emit('changeInputString', value) }
    }
  }
}
</script>

<style scoped>

</style>
