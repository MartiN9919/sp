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
          <v-icon>{{ dropdownIcon }}</v-icon>
        </v-list-item-action>
      </v-list-item>
    </v-list>
    <v-expand-transition>
      <div v-show="show">
        <slot/>
      </div>
    </v-expand-transition>
  </v-card>
</template>

<script>
export default {
  name: "SettingBlock",
  props: {
    icon: String,
    title: String,
    subTitle: String,
  },
  data: () => ({
    show: false,
    activeColor: {
      backgroundColor: '#757575'
    },
  }),
  computed: {
    headerStyle: function () {
      return this.show ? this.activeColor : {}
    },
    headerRipple: function () {
      return { style: this.activeColor }
    },
    dropdownIcon: function () {
      return this.show ? 'mdi-chevron-up' : 'mdi-chevron-down'
    }
  }
}
</script>

<style scoped>

</style>