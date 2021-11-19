<template>
  <v-row no-gutters class="text-center control flex-nowrap">
    <v-col v-for="button in buttons" :key="button.action">
      <v-btn :disabled="disabled(button)" @click="click(button)" color="teal" text large width="100%">{{button.title}}</v-btn>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "controlMenu",
  props: { buttons: Array},
  methods: {
    disabled: function (button) { return button.hasOwnProperty('disabled') ? !button.disabled : false },
    click: function (button) { this.$emit(button.action) }
  }
}
</script>

<style scoped>
.control {
  border-bottom-width: 1px;
  border-top-width: 1px;
  border-bottom-style: solid;
  border-top-style: solid;
  border-bottom-color: rgba(0, 0, 0, 0.12);
  border-top-color: rgba(0, 0, 0, 0.12);
}
</style>