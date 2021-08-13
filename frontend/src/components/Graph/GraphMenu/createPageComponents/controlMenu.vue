<template>
  <v-row no-gutters justify="center" class="flex-nowrap">
    <v-btn color="teal" text right width="10em" height="3.5em" @click="$emit('save')">{{textButton}}</v-btn>
  </v-row>
</template>

<script>
export default {
  name: "controlMenu",
  props: {
    textButton: String,
  }
}
</script>

<style scoped>

</style>