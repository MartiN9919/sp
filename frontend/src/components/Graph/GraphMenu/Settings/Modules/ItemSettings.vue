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
      <slot/>
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
  data: () => ({
    ripple: { class: 'teal--text' }
  }),
  computed: {
    state: {
      get: function () {
        return this.value
      },
      set: function (value) {
        this.$emit('changeValue', value)
      }
    }
  }
}
</script>

<style scoped>

</style>