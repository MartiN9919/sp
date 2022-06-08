<template>
  <div class="message-text-style v-messages">
    <span>{{item.information}}</span>
    <span class="text-no-wrap">
      Актуальность:
      <v-icon size="15" :color="item.informationActual.color">
        {{item.informationActual.icon}}
      </v-icon>
    </span>
  </div>
</template>

<script>
export default {
  name: "Description",
  props: {
    item: Object
  }
}
</script>

<style scoped>
.message-text-style {
  white-space: normal
}
</style>