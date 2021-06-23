<template>
  <v-speed-dial absolute right bottom direction="top" open-on-hover transition="slide-y-reverse-transition">
    <template v-slot:activator>
      <v-btn icon color="teal" large><v-icon>mdi-pencil</v-icon></v-btn>
    </template>
    <v-tooltip v-for="item in items" :key="item.id" z-index="100001" right :color="item.color">
      <template v-slot:activator="{ on }">
        <v-btn fab small :color="item.color" dark v-on="on" @click="$emit('selectTool', item.id)">
          <v-icon>{{item.icon}}</v-icon>
        </v-btn>
      </template>
      <span>{{item.title}}</span>
    </v-tooltip>
  </v-speed-dial>
</template>

<script>
export default {
  name: "speedDialOfTools",
  props: { items: Array },
}
</script>

<style scoped>

</style>