<template>
  <div class="phone-number-form">
    <body-input-form
      v-model="value"
      :rules="rules"
      :clearable="clearable"
      :class="bodyInputClasses"
      :placeholder="placeholder"
      :hideDetails="hideDetails"
      @keypress="isNumber($event)"
      prefix="+"
    >
      <template v-slot:label>
        {{title}}
      </template>
      <template v-slot:append="props">
        <v-icon
          v-if="deletable && props.hover"
          @click.stop="$emit('deletable')"
          size="24"
          class="action-icon"
        >mdi-delete</v-icon>
        <v-icon v-else size="24">mdi-cellphone</v-icon>
      </template>
      <template v-slot:message>
        <slot name="message"></slot>
      </template>
    </body-input-form>
  </div>
</template>

<script>
import BodyInputForm from "../UI/bodyInputForm"

export default {
  name: "phoneInput",
  components: {BodyInputForm},
  model: { prop: 'inputString', event: 'changeInputString', },
  props: {
    inputString: String,
    rules: {
      type: Array,
      default: function () {
        return []
      }
    },
    deletable: {
      type: Boolean,
      default: false,
    },
    title: {
      type: String,
      default: '',
    },
    hideDetails: {
      type: Boolean,
      default: false,
    },
    clearable: {
      type: Boolean,
      default: false,
    },
    placeholder: {
      type: String,
      default: 'Введите номер телефона',
    },
  },
  computed: {
    bodyInputClasses: function () { return this.title.length ? '' : 'pt-0' },
    value: {
      get: function () { return this.inputString },
      set: function (value) { this.$emit('changeInputString', value) }
    },
  },
  methods: {
    isNumber(event) {
      if (event.key === ' ' || event.key === '.')
        return event.preventDefault()
      if(!this.value) {
        if (!Number(event.key))
          return event.preventDefault()
      } else
      if (!Number(this.value + event.key))
        return event.preventDefault()
    }
  }
}
</script>

<style scoped>
.phone-number-form {
  width: 100%;
}
</style>