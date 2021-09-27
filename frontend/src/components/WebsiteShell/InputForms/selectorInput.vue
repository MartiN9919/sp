<template>
  <v-combobox
    v-model="value"
    :items="items"
    :item-text="itemText"
    :rules="rules"
    :clearable="clearable"
    :hide-details="hideDetails"
    :class="bodyInputClasses"
    :placeholder="placeholder"
    :disabled="disabled"
    :menu-props="{ offsetY: true, zIndex: 1000001 }"
    class="customCombobox"
    autocomplete="off"
    messages=" "
    color="teal"
    item-color="teal"
    dense
  >
    <template v-slot:label>
      {{title}}
    </template>
    <template v-slot:append>
      <v-hover v-slot="{ hover }" class="action-icon">
        <v-icon
          v-if="deletable && hover"
          @click.stop="$emit('deletable')"
          size="24"
        >mdi-delete</v-icon>
        <v-icon v-else size="24">mdi-format-list-bulleted</v-icon>
      </v-hover>
    </template>
    <template v-slot:message>
      <slot name="message"></slot>
    </template>
    <template v-slot:item="{ item }">
      <v-list-item-icon v-if="item.hasOwnProperty('icon')">
        <v-icon>{{item.icon}}</v-icon>
      </v-list-item-icon>
      <v-list-item-title class="selector-item">{{item[itemText]}}</v-list-item-title>
    </template>
  </v-combobox>
</template>

<script>

export default {
  name: "selectorInput",
  model: { prop: 'inputString', event: 'changeInputString', },
  props: {
    clearable: {
      type: Boolean,
      default: false,
    },
    deletable: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    hideDetails: {
      type: Boolean,
      default: false,
    },
    inputString: Number,
    itemText: {
      type: String,
      default: 'value',
    },
    items: {
      type: Array,
      default: function () {
        return []
      }
    },
    placeholder: {
      type: String,
      default: '',
    },
    rules: {
      type: Array,
      default: function () {
        return []
      }
    },
    title: {
      type: String,
      default: '',
    },
  },
  computed: {
    bodyInputClasses: function () { return this.title.length ? 'pt-5' : '' },
    value: {
      get: function () { return this.items.find(item => item.id === this.inputString) },
      set: function (value) { this.$emit('changeInputString', value.id) }
    }
  },
}
</script>

<style scoped>
.v-text-field {
  margin-top: 0;
  padding-top: 12px;
}
.customCombobox >>> input {
  padding: 0;
  cursor: pointer;
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
.customCombobox >>> .v-select__slot {
  cursor: pointer;
}
.action-icon {
  cursor: pointer;
}
.customCombobox {
  width: 100%;
}
.selector-item {
  white-space: normal;
  /*white-space: nowrap;*/
  /*overflow: hidden;*/
  /*text-overflow: ellipsis;*/
  width: 0;
}
</style>
