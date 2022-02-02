<template>
  <div class="unknown-form">
    <body-input-form
      v-model="value"
      v-bind="$attrs"
      :class="bodyInputClasses"
      @deletable="$emit('deletable')"
      icon="mdi-alert-circle-outline"
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
  name: "unknownInput",
  components: {BodyInputForm},
  model: { prop: 'inputString', event: 'changeInputString'},
  props: {
    inputString: Number,
  },
  computed: {
    bodyInputClasses: function () { return this.$attrs.hasOwnProperty('label') ? '' : 'pt-0' },
    value: {
      get: function () {
        if(this.inputString !== null)
          return this.$attrs.unknownText || 'Создана'
        else this.value = 0
      },
      set: function (value) { this.$emit('changeInputString', value) }
    }
  },
}
</script>

<style scoped>
.unknown-form {
  width: 100%;
}
</style>