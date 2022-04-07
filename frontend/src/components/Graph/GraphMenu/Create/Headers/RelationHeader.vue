<template>
  <div class="header text-center text-no-wrap">
    <div v-for="(object, key) in objects" :key="key" v-if="object">
      <v-icon>
        {{object.base.icon}}
      </v-icon>
      {{object.title}}
    </div>
  </div>
</template>

<script>
export default {
  name: "RelationHeader",
  props: {
    objects: Array
  }
}
</script>

<style scoped>

</style>