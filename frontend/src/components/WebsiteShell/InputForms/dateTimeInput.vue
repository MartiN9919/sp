<template>
  <div class="datetime-input-form">
    <drop-down-menu :nudge-left="290" min-width="auto" close-on-click :close-on-content-click="false">
      <template v-slot:activator="{ on }">
        <div v-on="on">
          <body-input-form
            v-model="value"
            :rules="rulesDateTime"
            :clearable="clearable"
            :hide-details="hideDetails"
            :class="bodyInputClasses"
            :placeholder="placeholder"
            readonly
          >
            <template v-slot:label>
              {{customLabel}}
            </template>
            <template v-slot:append="{ hover }" class="action-icon">
              <v-icon
                v-if="deletable && hover"
                @click.stop="$emit('deletable')"
                size="24"
              >mdi-delete</v-icon>
              <v-icon v-else size="24">mdi-calendar-clock</v-icon>
            </template>
            <template v-slot:message>
              <slot name="message"></slot>
            </template>
          </body-input-form>
        </div>
      </template>
      <template v-slot:body="{ closeMenu, status }">
        <select-date-time v-if="status" v-model="value" :close-menu="closeMenu"></select-date-time>
      </template>
    </drop-down-menu>
  </div>
</template>

<script>
import BodyInputForm from "../UI/bodyInputForm"
import DropDownMenu from "../UI/dropDownMenu"
import SelectDateTime from "../UI/selectDateTime"

export default {
  name: "dateTimeInput",
  components: {BodyInputForm, DropDownMenu, SelectDateTime},
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
      default: 'Выберете необходимую дату и время',
    },
    clearable: {
      type: Boolean,
      default: false,
    }
  },

  computed: {
    bodyInputClasses: function () { return this.title.length ? '' : 'pt-0' },
    rulesDateTime : function () {
      if (this.value)
        return [v => (v || '').split(' ').length > 1 || 'Введите все значения'].concat(this.rules)
      else return this.rules
    },
    value: {
      get: function () { return this.inputString },
      set: function (val) { this.$emit('changeInputString', val) }
    },
    customLabel: function () { return this.title.length ? 'Дата и время - ' + this.title : '' }
  },

}
</script>

<style scoped>
.datetime-input-form >>> input {
  cursor: pointer;
}
.datetime-input-form >>> .v-input__slot {
  cursor: pointer;
}
.action-icon {
  cursor: pointer;
}
.datetime-input-form {
  width: 100%;
}
</style>