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
        <v-list-item
          class='d-flex justify-space-between'
          v-on="on"
        >
          {{ title }}
          <div class="flex-grow-1"></div>
          <v-icon>mdi-chevron-right</v-icon>
        </v-list-item>
      </template>

      <v-list
        oncontextmenu="return false"
      >
        <template v-for="(item, index) in items">

          <!-- ЭЛЕМЕНТ МЕНЮ: СЕПАРАТОР-->
          <v-divider v-if='item.divider' :key='index'/>

         <!-- ЭЛЕМЕНТ МЕНЮ: ПОДМЕНЮ -->
         <!-- ПРОБРОС СВОЙСТВ И СОБЫТИЙ В РЕКУРСИИ -->
          <contextMenuNested v-else-if='item.menu'
            :key='index'
            :title='item.title'

            :items='item.menu'
            :color='color'

            :is-open-on-hover=false
            :is-offset-x=true
            :is-offset-y=false
            :is-sub-menu=true

            @click-item='on_click_item_retraslate'
            @close-menu='on_close_menu'
          />

          <!-- ЭЛЕМЕНТ МЕНЮ: ITEM -->
          <v-list-item v-else
            :key='index'
            @click='on_click_item(item)'
          >

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
                :color="item.color || color"
                @click.stop=""
              />
            </v-list-item-action>

          </v-list-item>

        </template>
      </v-list>
  </v-menu>
</template>

<script>

/*
ИСХОДНИК
  https://codepen.io/Moloth/pen/ZEBOzQP

ПРИМЕР ВЫЗОВА
  <contextMenuNested
    :menuItems='menu_items'
    :color="'red'"
    @click-item='on_click_item'
  />


*/

export default {
  name: 'contextMenuNested',
  props: {
    title:         String,                                           // заголовок субменю
    items:         Array,
    isOffsetX:     { type: Boolean, default: false },
    isOffsetY:     { type: Boolean, default: true  },
    isOpenOnHover: { type: Boolean, default: false },                // открытие при наведении курсора, с субменю работает не корректно
    transition:    { type: String,  default: "slide-x-transition" }, // анимация появления меню
    color:         { type: String,  default: "green" },              // цвет по умолчанию (переключатели и т.п.)
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
    show_root(x, y) {
      this.open      = false;
      this.root      = true;
      this.positionX = x;
      this.positionY = y;
      this.$nextTick(() => { this.open = true })
    },

    on_close_menu() {
      this.open = false;
      this.$emit("close-menu");           // проброс события в рекурсии
    },

    on_click_item(item) {
      this.$emit("click-item", item);
      this.on_close_menu();
    },

    on_click_item_retraslate(item, ee) {
      this.$emit("click-item", item);      // проброс события в рекурсии
    },

  },



}
</script>