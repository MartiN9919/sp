<template>
  <div class="boolean-input-form">
    <drop-down-menu nudge-left="64" min-width="auto" close-on-click close-on-content-click>
      <template v-slot:activator="{ on }">
        <div v-on="on">
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
              <v-icon v-else size="24">mdi-order-bool-descending-variant</v-icon>
            </template>
            <template v-slot:message>
              <slot name="message"></slot>
            </template>
          </body-input-form>
        </div>
      </template>
      <template v-slot:body="{ status, closeMenu }">
        <menu-boolean v-if="status" v-model="value" :close-menu="closeMenu" :booleanMenu="booleanMenu"></menu-boolean>
      </template>
    </drop-down-menu>
  </div>
</template>

<script>
import BodyInputForm from "./BodyToForm/bodyInputForm"
import DropDownMenu from "./BodyToForm/dropDownMenu"
import MenuBoolean from "./InputFormsUI/menuBoolean"

export default {
  name: "booleanInput",
  components: {BodyInputForm, DropDownMenu, MenuBoolean},
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
</style>