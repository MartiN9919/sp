<template>
<!--  <div class="v-messages d-flex pt-2" style="width: auto" :class="showAll ? 'text-wrap' : 'text-no-wrap'">-->
<!--    <span :class="!showAll && 'overflow-hidden'">-->
<!--      {{item.information}}-->
<!--      {{item.fieldInformation}}-->
<!--      <span class="text-no-wrap">-->
<!--        Актуальность:-->
<!--        <v-icon size="15" :color="item.informationActual.color">-->
<!--          {{item.informationActual.icon}}-->
<!--        </v-icon>-->
<!--      </span>-->
<!--      <span v-if="showAll" @click="showAll = false" class="pl-2" style="color: teal; cursor: pointer">-->
<!--        скрыть-->
<!--      </span>-->
<!--    </span>-->
<!--    <span v-if="!showAll"  @click="showAll = true" class="pl-2" style="color: teal; cursor: pointer">-->
<!--      показать все-->
<!--    </span>-->
<!--  </div>-->

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