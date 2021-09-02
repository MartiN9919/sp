<template>
  <v-tooltip bottom transition="false" color="#00796B" z-index="10001" max-width="30%">
    <template v-slot:activator="{ on }">
      <slot name="activator" :on="on"></slot>
    </template>
    <slot name="body"></slot>
  </v-tooltip>
</template>

<script>
export default {
  name: "customTooltip"
}
</script>

<style scoped>

</style>