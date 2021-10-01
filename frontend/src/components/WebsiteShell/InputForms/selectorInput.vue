<template>
  <v-combobox
    v-model="value"
    v-bind="$attrs"
    :items="items"
    :item-text="itemText"
    :class="bodyInputClasses"
    :menu-props="{ offsetY: true, zIndex: 1000001 }"
    class="customCombobox"
    autocomplete="off"
    messages=" "
    color="teal"
    item-color="teal"
    dense
  >
    <template v-slot:append>
      <v-hover v-slot="{ hover }" class="action-icon">
        <v-icon
          v-if="$attrs.hasOwnProperty('deletable') && hover"
          @click.stop="$emit('deletable')"
          size="24"
          class="action-icon"
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
      <v-list-item-title class="selector-item">{{item[itemText || 'value']}}</v-list-item-title>
    </template>
  </v-combobox>
</template>

<script>

import {mapGetters} from "vuex";

export default {
  name: "selectorInput",
  model: { prop: 'inputString', event: 'changeInputString'},
  props: {
    inputString: Number,
  },
  computed: {
    ...mapGetters(['baseList']),
    bodyInputClasses: function () { return this.$attrs.hasOwnProperty('label') ? 'pt-2' : '' },
    items: function() {
      return this.$attrs['type-load'] ? this.baseList(this.$attrs['type-load']).values : this.$attrs.items
    },
    itemText: function () { return this.$attrs['item-text'] || 'value'},
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
