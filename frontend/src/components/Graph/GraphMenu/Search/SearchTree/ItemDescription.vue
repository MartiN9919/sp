<template>
  <div class="v-messages message-text-style">
    <div class="message-text-style">
      <span class="text-no-wrap">
        Актуальность:
        <v-icon size="15" :color="item.actualInformation.color">
          {{item.actualInformation.icon}}
        </v-icon>
      </span>
      <span>{{item.information}}</span>
      <span>{{item.fieldInformation}}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: "Description",
  props: {
    item: Object
  },
  data: () => ({
    showAll: false
  }),
}
</script>

<style scoped>
.message-text-style {
  white-space: normal
}
.truncate-text {
  width: auto;
}
</style>