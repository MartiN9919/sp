<template>
  <v-text-field
    v-model="model"
    :prepend-inner-icon="item.object.icon"
    flat
    dense
    outlined
    hide-details
    color="teal"
    autocomplete="off"
    :readonly="relation && base"
    @keyup.enter="$emit('find')"
  >
    <template v-slot:append-outer="">
      <v-btn v-if="base" @click="$emit('find')" icon>
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
        if(this.relation) {
          if(this.base) {
            return this.item.title
          }
        } else {
          return this.item.request
        }
      },
      set(value) {
        this.item.request = value
      }
    }
  }
}
</script>

<style scoped>
>>> .v-input__append-outer {
  margin-top: 2px !important;
}
</style>