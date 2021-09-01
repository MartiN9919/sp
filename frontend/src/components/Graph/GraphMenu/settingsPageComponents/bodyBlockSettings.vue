<template>
  <v-card tile class="mb-1">
    <v-list class="py-0">
      <v-list-item @click="show = !show" :dark="show" :style="headerStyle" v-ripple="headerRipple">
        <v-list-item-avatar>
          <v-icon>{{icon}}</v-icon>
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title>{{title}}</v-list-item-title>
          <v-list-item-subtitle>{{subTitle}}</v-list-item-subtitle>
        </v-list-item-content>
        <v-list-item-action>
          <v-icon>{{ show ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
        </v-list-item-action>
      </v-list-item>
    </v-list>
    <v-expand-transition>
      <v-list v-show="show" dense>
        <slot></slot>
      </v-list>
    </v-expand-transition>
  </v-card>
</template>

<script>
import {mapGetters} from "vuex"

export default {
  name: "bodyBlockSettings",
  props: {
    icon: String,
    title: String,
    subTitle: String,
  },
  data: () => ({
    show: false,
    activeColor: {backgroundColor: '#757575'},
  }),
  computed: {
    ...mapGetters(['baseObjects']),
    headerStyle: function () { return this.show ? this.activeColor : {} },
    headerRipple: function () { return { style: this.activeColor } },
  },
}
</script>

<style scoped>

</style>