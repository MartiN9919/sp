<template>
  <v-text-field
    v-model="model"
    flat
    dense
    outlined
    hide-details
    color="teal"
    autocomplete="off"
    :readonly="readOnly"
    :prepend-inner-icon="icon"
    @keyup.enter="$emit('find')"
  >
    <template v-slot:append-outer="">
      <v-btn v-if="base" @click="$emit('find')" icon tabindex="-1">
        <v-icon size="30">mdi-magnify</v-icon>
      </v-btn>
    </template>
    <template v-slot:append="">
      <slot/>
    </template>
  </v-text-field>
</template>

<script>
export default {
  name: "Item",
  props: {
    item: Object,
    base: Boolean,
    relation: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    model: {
      get: function () {
        return this.item.fieldInformation || this.item.request
      },
      set(value) {
        this.item.request = value
      }
    },
    icon: function () {
      if(!Array.isArray(this.item.base)) {
        return this.item.base.icon
      }
      if(this.item.baseId.length === 1) {
        return this.item.base[0].icon
      } else if (this.item.baseId.length > 9) {
        return 'mdi-numeric-9-plus-box-multiple'
      } else {
        return `mdi-numeric-${this.item.baseId.length}-box-multiple`
      }

    },
    readOnly: function () {
      return (this.relation && this.base) || this.item.isFields
    }
  }
}
</script>

<style scoped>
>>> .v-input__append-outer {
  margin-top: 2px !important;
}
</style>