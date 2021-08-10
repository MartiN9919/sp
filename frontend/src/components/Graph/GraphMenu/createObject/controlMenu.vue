<template>
  <v-row no-gutters justify="space-between" class="flex-nowrap">
    <v-btn color="teal" text left width="10em" height="3.5em">Создать</v-btn>
    <v-btn color="teal" text right width="10em" height="3.5em" @click="$emit('save')">Сохранить</v-btn>
  </v-row>
</template>

<script>
export default {
  name: "controlMenu",
}
</script>

<style scoped>

</style>