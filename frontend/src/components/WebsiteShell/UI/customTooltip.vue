<template>
  <v-tooltip bottom transition="false" color="#00796B" z-index="10001" max-width="30%" content-class='custom-tooltip'>
    <template v-slot:activator="{ on }">
      <slot name="activator" :on="on"></slot>
    </template>
    <slot name="body"></slot>
  </v-tooltip>
</template>

<script>
export default {
  name: "customTooltip",
}
</script>

<style scoped>
.v-tooltip__content.menuable__content__active {
  opacity: 1!important;
  box-shadow: 0 3px 5px -1px rgba(0, 0, 0, 0.2),
              0 6px 10px 0 rgba(0, 0, 0, 0.14),
              0 1px 18px 0 rgba(0, 0, 0, 0.12);
  padding: 0;
}
</style>