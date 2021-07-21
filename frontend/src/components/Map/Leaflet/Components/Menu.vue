<template>
  <v-menu
    class="select_off"
    style="z-index: 50000;"
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
      <template v-if="!root" v-slot:activator="{ on }">
        <v-list-item class='d-flex justify-space-between' v-on="on">
            {{ name }}
            <div class="flex-grow-1"></div>
            <v-icon>mdi-chevron-right</v-icon>
        </v-list-item>
      </template>
      <v-list

      >
        <template v-for="(item, index) in menuItems">

          <!-- ЭЛЕМЕНТ МЕНЮ: СЕПАРАТОР-->
          <v-divider v-if='item.divider' :key='index'/>

         <!-- ЭЛЕМЕНТ МЕНЮ: ПОДМЕНЮ -->
          <Menu v-else-if='item.menu'
            :key='index'
            :name='item.title'
            :menu-items='item.menu'
            :is-open-on-hover=false
            :is-offset-x=true
            :is-offset-y=false
            :is-sub-menu=true
            @click='on_click_submenu'
            @click-item='on_click_item_retraslate'
          />

          <!-- ЭЛЕМЕНТ МЕНЮ: ITEM -->
          <v-list-item v-else
            :key='index'
            @click='on_click_item(item)'
          >
            <!--
              @click.prevent="item.click(item.click_param)"

              @click='on_click(item)'
              @click.prevent="form[item.click](item.click_param)"
            -->
            <!-- ITEM: ИКОНКА -->
            <v-list-item-icon>
              <v-icon large v-text="item.icon"/>
            </v-list-item-icon>

            <!-- ТЕКСТ -->
            <v-list-item-content>
              <v-list-item-title v-text="item.title"/>
              <v-list-item-subtitle v-text="item.subtitle"/>
            </v-list-item-content>

            <!-- ACTION -->
            <v-list-item-action
              v-if="item.action"
            >
              <v-switch
                v-model="item.model"
                color="green"
                @click.stop=""
              />
            </v-list-item-action>

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

  data: () => ({
    root:      false,
    open:      false,
    positionX: undefined,
    positionY: undefined,
  }),

  computed: {
    // https://coderoad.ru/63553151/Vue-как-использовать-Getter-настройка-в-v-модели-с-v-for
    form: vm => vm,
  },

  methods: {
    activate_root(x, y) {
      this.open      = false;
      this.root      = true;
      this.positionX = x;
      this.positionY = y;
      this.$nextTick(() => { this.open = true })
    },

    on_click_submenu(item) {
      console.log('menu.on_click_submenu', item)
      this.$emit("click-submenu", item);
      this.open = false;
    },

    on_click_item(item) {
      console.log('menu.on_click_item', item)
      this.$emit("click-item", item);
      //item.click(item.click_param)
    },

    // проброс события в рекурсии
    on_click_item_retraslate(item, ee) {
      console.log('!!!', item, ee)
      this.$emit("click-item", item);
    }
  },



}
</script>