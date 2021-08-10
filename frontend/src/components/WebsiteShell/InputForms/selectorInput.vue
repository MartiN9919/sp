<template>
  <v-combobox
    v-model="value"
    :items="list"
    :item-text="itemText"
    :rules="rules"
    :clearable="clearable"
    :hide-details="hideDetails"
    :class="bodyInputClasses"
    :placeholder="placeholder"
    :menu-props="{offsetY: true, allowOverflow: false}"
    class="customCombobox"
    autocomplete="off"
    messages=" "
    color="teal"
    item-color="teal"
  >
    <template v-slot:label>
      {{title}}
    </template>
    <template v-slot:append>
      <v-hover v-slot="{ hover }" class="action-icon">
        <v-icon v-if="deletable && hover" @click.stop="" size="24">mdi-delete</v-icon>
        <v-icon v-else size="24">mdi-format-list-bulleted</v-icon>
      </v-hover>
    </template>
    <template v-slot:message>
      <slot name="message"></slot>
    </template>
    <template v-slot:item="{ item }">
      <div class="py-1">{{item[itemText]}}</div>
    </template>
  </v-combobox>
</template>

<script>
  export default {
    name: "selectorInput",
    props: {
      inputString: Number,
      list: Array,
      rules: {
        type: Array,
        default: function () {
          return []
        }
      },
      itemText: String,
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
        default: 'Введите необходимое значение',
      },
    },
    model: { prop: 'inputString', event: 'changeInputString', },
    computed: {
      bodyInputClasses: function () { return this.title.length ? 'pt-5' : '' },
      menuProps: function () {
        if (this?.$el?.clientWidth)
          return {offsetY: true, maxWidth: this?.$el?.clientWidth, minWidth: this?.$el?.clientWidth}
      },
      value: {
        get: function () { return this.list.find(item => item.id === this.inputString) },
        set: function (value) { this.$emit('changeInputString', value.id) }
      }
    },
  }
</script>

<style scoped>
.v-text-field {
  margin-top: 0;
  padding-top: 0;
}
.customCombobox >>> input {
  padding: 0;
}
.customCombobox >>> .v-input__slot {
  align-items: flex-end;
  margin-bottom: 0;
}
.customCombobox >>> .v-input__append-inner {
  margin-top: 0 !important;
}
.customCombobox >>> .v-messages {
  min-height: 0;
}
.customCombobox >>> .v-text-field__details {
  min-height: 0;
}
.customCombobox >>> input {
  cursor: pointer;
}
.customCombobox >>> .v-select__slot {
  cursor: pointer;
}
.action-icon {
  cursor: pointer;
}
.customCombobox {
  width: 100%;
}
</style>
