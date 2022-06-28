<template>
  <div class="text-input-form">
    <body-input-form
      v-model="value"
      v-bind="$attrs"
      :class="bodyInputClasses"
      :placeholder="placeholder"
      :icon="icon"
      :rules="rules"
      @deletable="$emit('deletable')"
      :clearable="false"
    >
      <template v-slot:message>
        <slot name="message"></slot>
      </template>
    </body-input-form>
  </div>
</template>

<script>
import BodyInputForm from "@/components/WebsiteShell/CustomComponents/bodyInputForm"

export default {
  name: "textInput",
  components: {BodyInputForm},
  model: { prop: 'inputString', event: 'changeInputString', },
  props: {
    inputString: String,
  },
  data: () => ({
    properties: {
      eng: {
        icon: 'mdi-alpha-e',
        placeholder: 'Введите необходимое значение на английском',
        rule: /^[A-Z a-z0-9]+$/,
      },
      ru: {
        icon: 'mdi-alpha-r',
        placeholder: 'Введите необходимое значение на русском',
        rule: /^[А-Яа-я0-9]+$/,
      },
      default: {
        icon: 'mdi-format-color-text',
        placeholder: 'Введите необходимое значение',
        rule: /^/,
      },
    }
  }),
  computed: {
    textType: function () { return this.properties[this.$attrs['type-load']] || this.properties.default },
    placeholder: function () { return this.textType.placeholder },
    icon: function () { return this.textType.icon },
    rules : function () {
      if (this.value) {
        let rule = [() => this.textType.rule.test(this.value) || 'Проверьте введенный текст']
        return this.$attrs.hasOwnProperty('rules') ? rule.concat(this.$attrs.rules) : rule
      }
      else return this.$attrs.rules
    },
    bodyInputClasses: function () { return this.$attrs.hasOwnProperty('label') ? '' : 'pt-0' },
    value: {
      get: function () { return this.inputString },
      set: function (value) { this.$emit('changeInputString', value) }
    }
  },
}
</script>

<style scoped>
.text-input-form {
  width: 100%;
}
</style>