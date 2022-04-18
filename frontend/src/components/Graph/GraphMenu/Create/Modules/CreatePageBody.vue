<template>
  <div class="h-100">
    <div class="work-place">
      <slot name="header"/>
      <v-tabs v-show="tabsStatus" v-model="activeTab" :color="sliderColor" :class="tabClasses" grow show-arrows center-active>
        <v-tab v-if="tabsStatus" v-for="(item, key) in editable" :key="key">
          <v-icon :color="tabColor(key)">{{ item.base.icon }}</v-icon>
          <span :style="{color: tabColor(key)}">
            {{ key === 0 ? 'Исходный объект' : 'Схожий объект' }}
            {{ key + 1 }}
          </span>
        </v-tab>
      </v-tabs>
      <v-tabs-items v-model="activeTab">
        <slot name="body"/>
      </v-tabs-items>
    </div>
    <slot v-if="!!editable" name="control"/>
  </div>
</template>

<script>
export default {
  name: "CreatePageBody",
  model: { prop: 'tab', event: 'changeTab'},
  props: {
    editable: [Array, Object],
    tab: Number,
  },
  computed: {
    activeTab: {
      get: function () {
        return this.tab
      },
      set: function (value) {
        this.$emit('changeTab', value)
      }
    },
    tabsStatus: function () {
      return this.editable instanceof Array && this.editable && this.editable.length > 1
    },
    sliderColor: function () {
      return this.activeTab ? '#FF0000' : '#009688'
    },
    tabClasses: function () {
      if (this.editable)
        if (this.editable.length > 1)
          return 'height-with-tabs'
      return 'height-without-tabs'
    }
  },
  methods: {
    tabColor(key) {
      return key ? '#FF0000' : '#009688'
    }
  }
}
</script>

<style scoped>
.work-place {
  height: calc(100% - 44px);
  overflow-y: hidden;
  overflow-x: hidden;
}
</style>