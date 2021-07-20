<template>
  <v-menu
    ref="menu"
    :close-on-content-click="false"
    :offset-x='isOffsetX'
    :offset-y='isOffsetY'
    :position-x="positionX"
    :position-y="positionY"
    :open-on-hover='isOpenOnHover'
    :transition='transition'
    :value="openMenu"
    :absolute="root"
  >
      <template v-slot:activator="{ on }">
        <v-btn v-if='icon' :color='color' v-on="on">
            <v-icon>{{ icon }}</v-icon>
        </v-btn>
        <v-list-item v-else-if='isSubMenu' class='d-flex justify-space-between' v-on="on">
            {{ name }}<div class="flex-grow-1"></div><v-icon>mdi-chevron-right</v-icon>
        </v-list-item>
        <v-btn v-else :color='color' v-on="on"  @click="openMenu=true"  text >{{ name }}</v-btn>
      </template>
      <v-list>
        <template v-for="(item, index) in menuItems">
          <v-divider v-if='item.isDivider' :key='index' />
          <Menu v-else-if='item.menu'
            :key='index'
            :name='item.name'
            :menu-items='item.menu'
            @Menu-click='emitClickEvent'
            :is-open-on-hover=false
            :is-offset-x=true
            :is-offset-y=false
            :is-sub-menu=true />
          <v-list-item v-else :key='index' @click='emitClickEvent(item)'>
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
    icon:          String,
    menuItems:     Array,
    color:         { type: String,  default: "secondary" },
    isOffsetX:     { type: Boolean, default: false },
    isOffsetY:     { type: Boolean, default: true  },
    isOpenOnHover: { type: Boolean, default: false },
    isSubMenu:     { type: Boolean, default: false },
    transition:    { type: String,  default: "scale-transition" }
  },
  methods: {
    emitClickEvent (item) {
      this.$emit("Menu-click", item);
      this.openMenu = false;
    },
    activateRoot(x, y) {
      console.log(222);
      this.root      = true;
      this.openMenu  = false;
      this.positionX = x;
      this.positionY = y;
      this.$nextTick(() => { this.openMenu = true })
    }
  },
  data: () => ({
    root:      false,
    openMenu:  false,
    positionX: undefined,
    positionY: undefined,
  }),
}
</script>