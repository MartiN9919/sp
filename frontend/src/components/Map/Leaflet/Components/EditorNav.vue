<template>
  <v-card height="100%">
    <v-tabs
      ref="tabs"
      v-model="tab"
      :color="$CONST.APP.COLOR_OBJ"
      background-color="transparent"
      grow
    >
      <v-tabs-slider :color="$CONST.APP.COLOR_OBJ"/>
      <v-tab href="#tab-obj">
        <v-icon left>mdi-vector-polygon</v-icon>
        Объекты
      </v-tab>
      <v-tab href="#tab-osm">
        <v-icon left>mdi-web</v-icon>
        Поиск
      </v-tab>



      <v-tab-item value="tab-obj">
        <EditorNavObj
          v-bind="$attrs"
          v-on="$listeners"
        />
      </v-tab-item>

      <v-tab-item value="tab-osm">
        <editorNavOsm
          v-bind="$attrs"
          v-on="$listeners"
        />
      </v-tab-item>

    </v-tabs>

  </v-card>
</template>

<script>

import router       from '@/router'
import editorNavOsm from '@/components/Map/Leaflet/Components/EditorNavOsm';
import EditorNavObj from '@/components/Map/Leaflet/Components/EditorNavObj';

export default {
  name: 'EditorNav',
  components: { EditorNavObj, editorNavOsm, },
  inheritAttrs: false,
  props: {
    localStorageKey: { type: String, default() { return '' } },
    triggerResize: Boolean,           // триггер изменения размера компонента
  },

  data: () => ({
    tab: null,
  }),

  watch: {
    tab: function(val) {
      localStorage[this.key_tab] = val
    },

    triggerResize: function(val) {
      this.$refs.tabs.callSlider(); // устранение бага со слайдером
    },
  },

  computed: {
    key_tab() { return router.currentRoute.name + '_editor_nav_tab_sel_' + this.localStoragePrefix },
  },

  mounted() {
    this.tab = localStorage[this.key_tab]
  },

}


</script>