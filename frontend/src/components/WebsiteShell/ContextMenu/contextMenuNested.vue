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
    :transition="transition"
    :value="open"
    :absolute="root"
  >
    <!-- СЛОТ-АКТИВАТОР ПОДМЕНЮ -->
    <template v-if="!root" v-slot:activator="{ on }">
      <v-list-item
        class="d-flex justify-space-between"
        v-on="on"
        :disabled="!( items && (items.length > 0) )"
      >
        <v-list-item-icon v-if="icon">
          <v-icon v-text="icon"/>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title v-text="title"/>
          <v-list-item-subtitle v-text="subtitle"/>
        </v-list-item-content>

        <v-list-item-action>
          <v-icon>mdi-chevron-right</v-icon>
        </v-list-item-action>
      </v-list-item>
    </template>

    <v-list
      oncontextmenu="return false"
      rounded
      hide-details
    >

      <template v-for="(item, index) in items">

        <!-- ЭЛЕМЕНТ МЕНЮ: СЕПАРАТОР-->
        <v-divider v-if="item.divider" :key="index"/>

        <!-- ЭЛЕМЕНТ МЕНЮ: ПОДМЕНЮ -->
        <!-- ПРОБРОС СВОЙСТВ И СОБЫТИЙ В РЕКУРСИИ -->
        <contextMenuNested v-else-if="item.menu"
          :key="index"
          :icon="item.icon"
          :title="item.title"
          :subtitle="item.subtitle"
          :radio="item.radio"
          :model="item.model"

          :form="form"
          :items="item.menu"
          :color="color"

          :is-open-on-hover=false
          :is-offset-x=true
          :is-offset-y=false
          :is-sub-menu=true

          @close-menu="on_close_menu"
        />

        <!-- ЭЛЕМЕНТ МЕНЮ: RADIO-GROUP -->
        <v-radio-group v-else-if="item.radio"
          v-model="form[item.model]"
          style="margin-top:0;padding-top:0;"
        >
        <v-list-item-group>
              <v-radio
                v-for="(radio_item, radio_index) in item.radio"
                :value="radio_index"
                :key="radio_index"
                :color="radio_item.color || color"
                @click.stop=""
              >

            <v-list-item-icon v-if="radio_item.icon">
              <v-icon v-text="radio_item.icon"/>
            </v-list-item-icon>

            <v-list-item-content>
              <v-list-item-title v-text="radio_item.title"/>
              <v-list-item-subtitle v-text="radio_item.subtitle"/>
            </v-list-item-content>


              </v-radio>
        </v-list-item-group>
        </v-radio-group>


        <!-- ЭЛЕМЕНТ МЕНЮ: ITEM (ОБЫЧНЫЙ, SWITCH) -->
        <v-list-item v-else
          :key="index"
          @click="on_click_item(item, index)"
        >

            <!-- ITEM: ИКОНКА -->
            <v-list-item-icon v-if="item.icon">
              <v-icon v-text="item.icon"/>
            </v-list-item-icon>

            <!-- ITEM: ТЕКСТ -->
            <v-list-item-content>
              <v-list-item-title v-text="item.title"/>
              <v-list-item-subtitle v-text="item.subtitle"/>
            </v-list-item-content>

            <!-- ITEM: ACTION -->
            <v-list-item-action
              v-if="item.model || radio"
            >

              <!-- ITEM ACTION: SWITCH -->
              <v-switch
                v-if="item.model"
                v-model="form[item.model]"
                :color="item.color || color"
                @click.stop=""
              />

            </v-list-item-action>

          </v-list-item>

        </template>

      </v-list>
  </v-menu>

          <!-- ЭЛЕМЕНТ МЕНЮ: ITEM (RADIO) -->
<!--
          <v-radio-group v-else-if="item.radio"
            v-if="group_item.radio"
            v-for="(item, ind) in form[group_item.items]"
            v-model="form[group_item.model]"
            :key="group_item.key+'_'+ind"
            class="map-menu-radio-group select_off"
            hide-details
          >
            <v-list-item
              class="map-menu-tile-radio"
              @click.prevent="form[group_item.click](ind)"
              :disabled="item.disabled"
            >
              <v-list-item-icon>
                <v-icon large v-text="item.icon"/>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title v-text="item.title"/>
                <v-list-item-subtitle v-text="item.subtitle"/>
              </v-list-item-content>
              <v-list-item-action>
                <v-radio
                  color="green"
                  :value="ind"
                  :key="ind"
                  @click.stop=""
                />
              </v-list-item-action>
            </v-list-item>
          </v-radio-group>
-->

</template>

<script>

/*
ИСХОДНИК
  https://codepen.io/Moloth/pen/ZEBOzQP


ПРИМЕР ВЫЗОВА
  <contextMenuNested
    :form="form"
    :menuItems='menu_items'
    :color="'red'"
  />

  menu_show(x, y) { this.$refs.menu.show_root(x, y); },


ВАЖНО:
  item могуть быть:
    с обработкой model
    с обработкой action (закрытие при выборе)
  item.menu == [] - item disabled
*/

export default {
  name: 'contextMenuNested',
  props: {
    form:          Object,                                           // указатель на объект, вызвавший root menu (органайзер)
    icon:          String,                                           // субменю: иконка, если ' ' - отсутствует, но место остается
    title:         String,                                           // субменю: заголовок
    subtitle:      String,                                           // субменю: подзаголовок
    radio:         Boolean,                                          // субменю: radio-группа
    model:         String,                                           // субменю: radio-model
    items:         Array,
    isOffsetX:     { type: Boolean, default: false },
    isOffsetY:     { type: Boolean, default: true  },
    isOpenOnHover: { type: Boolean, default: false },                // открытие при наведении курсора, только для root
    transition:    { type: String,  default: "slide-x-transition" }, // анимация появления меню
    color:         { type: String,  default: "green" },              // цвет по умолчанию (переключатели и т.п.)
  },

  data: () => ({
    root:      false,
    open:      false,
    positionX: undefined,
    positionY: undefined,
  }),

  methods: {
    // Показать первый уровень меню, вызывается из родителя
    show_root(x, y) {
      this.open      = false;
      this.root      = true;
      this.positionX = x;
      this.positionY = y;
      this.$nextTick(() => { this.open = true })
    },

    // закрыть меню рекурсивно
    on_close_menu() {
      this.open = false;
      this.$emit("close-menu");
    },

    on_click_item(item, index) {
      // ITEM: SWITCH
      if (item.model) {
        this.form[item.model] = !this.form[item.model];
      }

      // ITEM: RADIO
      else if ((this.radio) && (this.model)) {
        this.form[this.model] = index;
      }

      // ITEM: ACTION
      else if (item.action) {
        this.on_close_menu();
        this.form[item.action](item);
      }
    },

  },


}
</script>