<template>
  <v-menu
    :close-on-content-click="false"
    :offset-x="isOffsetX"
    :offset-y="isOffsetY"
    :position-x="positionX"
    :position-y="positionY"
    :open-on-hover='isOpenOnHover'
    :transition='transition'
    :value="open"
    :absolute="root"
  >
      <template v-slot:activator="{ on }">
        <v-list-item class='d-flex justify-space-between' v-on="on">
            {{ name }}
            <div class="flex-grow-1"></div>
            <v-icon>mdi-chevron-right</v-icon>
        </v-list-item>
      </template>
      <v-list>
        <template v-for="(item, index) in menuItems">
          <v-divider v-if='item.divider' :key='index' />
          <Menu v-else-if='item.menu'
            :key='index'
            :name='item.name'
            :menu-items='item.menu'
            :is-open-on-hover=false
            :is-offset-x=true
            :is-offset-y=false
            :is-sub-menu=true
            @Menu-click='on_click_item'
          />
          <v-list-item v-else :key='index' @click='on_click_item(item)'>
              <v-list-item-title>{{ item.name }}</v-list-item-title>
          </v-list-item>
        </template>
      </v-list>
  </v-menu>
</template>

<script>
// https://codepen.io/Moloth/pen/ZEBOzQP
export default {
  name: 'Menu',
  props: {
    name:          String,
    menuItems:     Array,
    color:         { type: String,  default: "secondary" },
    isOffsetX:     { type: Boolean, default: false },
    isOffsetY:     { type: Boolean, default: true  },
    isOpenOnHover: { type: Boolean, default: false },                // открытие при наведении курсора, с субменю работает не корректно
    transition:    { type: String,  default: "slide-x-transition" }, // появление меню
  },
  methods: {
    on_click_item (item) {
      this.$emit("Menu-click", item);
      this.open = false;
    },
    activate_root(x, y) {
      this.open      = false;
      this.root      = true;
      this.positionX = x;
      this.positionY = y;
      this.$nextTick(() => { this.open = true })
    }
  },
  data: () => ({
    root:      false,
    open:      false,
    positionX: undefined,
    positionY: undefined,
  }),
}
</script>