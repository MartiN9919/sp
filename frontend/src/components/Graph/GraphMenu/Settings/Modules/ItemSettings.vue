<template>
  <v-list-item @click="state = !state" v-ripple="ripple">
    <v-list-item-content>
      <v-list-item-title>
        {{ title }}
      </v-list-item-title>
      <v-list-item-subtitle v-if="subTitle" class="description">
        {{ subTitle }}
      </v-list-item-subtitle>
    </v-list-item-content>
    <v-list-item-action class="my-auto ml-2">
      <v-switch disabled v-model="value" color="teal"/>
    </v-list-item-action>
  </v-list-item>
</template>

<script>
export default {
  name: "ItemSettings",
  model: {
    prop: 'value',
    event: 'changeValue'
  },
  props: {
    title: String,
    subTitle: String,
    value: Boolean
  },
  computed: {
    state: {
      get: function () {
        return this.value
      },
      set: function (value) {
        this.$emit('changeValue', value)
      }
    },
    ripple: function () {
      return { class: 'teal--text' }
    }
  }
}
</script>

<style scoped>

</style>