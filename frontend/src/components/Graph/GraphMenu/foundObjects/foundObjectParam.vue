<template>
  <v-select
    v-model='param.date' :items="[{ value: param.value, date: param.date }].concat(param.old)"
    :menu-props="menuProps(param)" :append-icon="menuIcon(param)" item-text="value" item-value="date"
    attach hide-details class="py-2" color="teal" type="text" item-color="teal" autocomplete="off"
    :label="label" placeholder="Выберете необходимое значение"
  >
    <template v-slot:item="{ item }">
      <v-list-item @click="" :key="item.date" :style="menuItemColor(param, item)">
        <v-row no-gutters>
          <v-col>{{ item.value }}</v-col>
          <v-col class="d-flex text-right align-center" cols="auto">{{ item.date }}</v-col>
        </v-row>
      </v-list-item>
    </template>
  </v-select>
</template>

<script>
export default {
  name: "foundObjectParam",
  props: {
    param: Object,
    label: String,
  },
  data: () => ({
    oldestValue: null,
  }),
  computed: {
    value: {
      get: function () { return this.param.value },
      set: function (value) { console.log(value) },
    }
  },
  methods: {
    menuItemColor (param, item) {
      return param.date !== item.date || { backgroundColor: '#E0F2F1' }
    },
    menuProps (param) {
      let menu = { offsetY: true, maxWidth: '100%', minWidth: '100%', closeOnClick: true, }
      if (!param.old.length) menu.value = false
      return menu
    },
    menuIcon (params) {
      return params.old.length ? 'mdi-format-list-bulleted' : ''
    },
  },
  created() {
    this.oldestValue = this.param.value
  }
}
</script>

<style scoped>

</style>