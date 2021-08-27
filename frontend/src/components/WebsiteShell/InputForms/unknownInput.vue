<template>
  <div class="unknown-form">
    <body-input-form
      v-model="value"
      :hide-details="hideDetails"
      :class="bodyInputClasses"
      readonly
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
        <v-icon v-else size="24">mdi-alert-circle-outline</v-icon>
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
  name: "unknownInput",
  components: {BodyInputForm},
  props: {
    deletable: {
      type: Boolean,
      default: false,
    },
    title: {
      type: String,
      default: '',
    },
    unknownText: {
      type: String,
      default: 'Создана'
    },
    hideDetails: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    bodyInputClasses: function () { return this.title.length ? '' : 'pt-0' },
    value: {
      get: function () { return this.unknownText },
      set: function (value) { this.$emit('changeInputString', value) }
    }
  },
}
</script>

<style scoped>
.text-input-form {
  width: 100%;
}
.action-icon {
  cursor: pointer;
}
</style>