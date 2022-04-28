<template>
  <v-row no-gutters class="text-center control flex-nowrap">
    <v-col v-for="btn in buttons" :key="btn.action">
      <v-btn
        :disabled="!btn.disabled"
        @click="$emit(btn.action)"
        width="100%"
        color="teal"
        large
        text
      >
        {{btn.title}}
      </v-btn>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "ControlMenu",
  props: {
    buttons: Array
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