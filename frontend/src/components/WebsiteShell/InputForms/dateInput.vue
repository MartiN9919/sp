<template>
  <div class="date-input-form">
    <drop-down-menu nudge-left="290" min-width="auto" close-on-click :close-on-content-click="false">
      <template v-slot:activator="{ on }">
        <div v-on="on">
          <body-input-form
            v-model="value"
            :rules="rules"
            :clearable="clearable"
            :hide-details="hideDetails"
            :class="bodyInputClasses"
            :placeholder="placeholder"
            readonly
          >
            <template v-slot:label>
              {{title}}
            </template>
            <template v-slot:append="{ hover }" class="action-icon">
              <v-icon
                v-if="deletable && hover"
                @click.stop="$emit('deletable')"
                size="24"
              >mdi-delete</v-icon>
              <v-icon v-else size="24" >mdi-calendar</v-icon>
            </template>
            <template v-slot:message>
              <slot name="message"></slot>
            </template>
          </body-input-form>
        </div>
      </template>
      <template v-slot:body="{ closeMenu,  status }">
        <select-date v-if="status" v-model="value" :close-menu="closeMenu"></select-date>
      </template>
    </drop-down-menu>
  </div>
</template>

<script>
import BodyInputForm from "../UI/bodyInputForm"
import DropDownMenu from "../UI/dropDownMenu"
import SelectDate from "../UI/selectDate"

export default {
  name: "dateInput",
  components: {BodyInputForm, DropDownMenu, SelectDate},
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
    placeholder: {
      type: String,
      default: 'Выберете необходимую дату',
    },
    clearable: {
      type: Boolean,
      default: false,
    }
  },
  computed: {
    bodyInputClasses: function () { return this.title.length ? '' : 'pt-0' },
    value: {
      get: function () { return this.inputString },
      set: function (value) { this.$emit('changeInputString', value) },
    },
  },
}
</script>

<style scoped>
.date-input-form >>> input {
  cursor: pointer;
}
.date-input-form >>> .v-input__slot {
  cursor: pointer;
}
.action-icon {
  cursor: pointer;
}
.date-input-form {
  width: 100%;
}
</style>