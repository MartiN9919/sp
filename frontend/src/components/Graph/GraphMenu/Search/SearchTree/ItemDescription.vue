<template>
  <div class="message-text-style v-messages">
    <span>{{item.getInformation()}}</span>
    <span class="text-no-wrap">
      Актуальность:
      <v-icon size="15" :color="item.getInformationActual().color">
        {{item.getInformationActual().icon}}
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