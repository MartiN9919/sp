<template>
  <v-hover v-slot="{ hover }">
    <v-expansion-panel-header class="py-0 px-2" :color="opened ? '#bfbfbf' : '#f2f2f2'">
      <template v-slot:actions="">
        <v-icon
          style="transform: none"
          v-if="hover && opened"
          @click.stop="$emit('createNewParam')"
          :color="opened ? 'white' : 'black'"
        >mdi-plus</v-icon>
      </template>
      <template v-slot:default="">
        <span :style="opened ? { color: 'white' } : { color: 'black' }">
          {{ title }}
        </span>
      </template>
    </v-expansion-panel-header>
  </v-hover>
</template>

<script>
export default {
  name: "recordTitle",
  props: {
    title: String,
    opened: Boolean,
  }
}
</script>

<style scoped>

</style>