<template>
  <div class="boolean-input-form" @click="value === 'ДА' ? value = false : value = true">
    <body-input-form
      v-model="value"
      :rules="rules"
      :hide-details="hideDetails"
      :class="bodyInputClasses"
      :placeholder="placeholder"
      readonly
    >
      <template v-slot:label>
        {{title}}
      </template>
      <template v-slot:append="{ hover }" class="action-icon">
        <v-icon v-if="deletable && hover" @click.stop="" size="24">mdi-delete</v-icon>
        <v-checkbox
          v-else
          :value="value === 'ДА'"
          :ripple="false"
          class="mt-0 pt-0"
          color="gray"
          on-icon="mdi-checkbox-marked-outline"
          off-icon="mdi-checkbox-blank-outline"
        ></v-checkbox>
      </template>
      <template v-slot:message>
        <slot name="message"></slot>
      </template>
    </body-input-form>
  </div>
</template>

<script>
import BodyInputForm from "../UI/bodyInputForm"
import DropDownMenu from "../UI/dropDownMenu"

export default {
  name: "booleanInput",
  components: {BodyInputForm, DropDownMenu},
  model: { prop: 'inputString', event: 'changeInputString', },
  props: {
    inputString: Boolean,
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
    placeholder: {
      type: String,
      default: 'Выберете необходимое значение',
    },
  },
  data: () => ({
    booleanMenu: [{ text: 'ДА', value: true }, { text: 'НЕТ', value: false }]
  }),
  computed: {
    bodyInputClasses: function () { return this.title.length ? '' : 'pt-0' },
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
}
</script>

<style scoped>
.boolean-input-form >>> input {
  cursor: pointer;
}
.boolean-input-form >>> .v-input__slot {
  cursor: pointer;
}
.action-icon {
  cursor: pointer;
}
.boolean-input-form {
  width: 100%;
}
.boolean-input-form >>> .v-input--selection-controls__input {
  margin-right: 0;
}
</style>