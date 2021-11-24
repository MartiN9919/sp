<template>
  <div class="boolean-input-form">
    <body-input-form
      v-model="value"
      v-bind="$attrs"
      :class="bodyInputClasses"
      :icon="value === 'ДА' ? 'mdi-checkbox-marked-outline' : 'mdi-checkbox-blank-outline'"
      :placeholder="$attrs.placeholder || 'Выберете необходимое значение'"
      @click.native="changeValue"
      @deletable="$emit('deletable')"
      readonly
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
  name: "booleanInput",
  components: {BodyInputForm},
  model: { prop: 'inputString', event: 'changeInputString'},
  props: {
    inputString: Boolean,
  },
  data: () => ({
    booleanMenu: [{ text: 'ДА', value: true }, { text: 'НЕТ', value: false }]
  }),
  computed: {
    bodyInputClasses: function () { return this.$attrs.hasOwnProperty('label') ? '' : 'pt-0' },
    value: {
      get: function () {
        if (this.inputString === null)
          this.value = false
        else
          return this.booleanMenu.find(item => item.value === this.inputString).text
      },
      set: function (value) { this.$emit('changeInputString', value) }
    },
  },
  methods: {
    changeValue() {
      this.value === 'ДА' ? this.value = false : this.value = true
    }
  }
}
</script>

<style scoped>
.boolean-input-form >>> input {
  cursor: pointer;
}
.boolean-input-form >>> .v-input__slot {
  cursor: pointer;
}
.boolean-input-form {
  width: 100%;
}
.boolean-input-form >>> .v-input--selection-controls__input {
  margin-right: 0;
}
</style>