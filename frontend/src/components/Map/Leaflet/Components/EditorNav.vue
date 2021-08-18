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
import MixResize    from '@/components/Map/Leaflet/Mixins/Resize';

export default {
  name: 'EditorNav',

  components: { EditorNavObj, editorNavOsm, },
  mixins: [ MixResize, ],

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
      //console.log(111)
      this.$refs.tabs.callSlider(); // устранение бага со слайдером
    },
  },

  computed: {
    key_tab() { return router.currentRoute.name + '_editor_nav_tab_sel_' + this.localStoragePrefix },
  },

  mounted() {
    this.tab = localStorage[this.key_tab]
  },

  methods: {
    // fire from MixResize
    onResize () {
      //this.$emit('resize', this.$refs.tabs.offsetHeight)
      this.$refs.tabs.callSlider();
    },
  },


}


</script>

<style scoped lang="scss">
  /* fix bug: кнопка влево не нужна*/
  div::v-deep .v-slide-group__prev { display: none !important; }

  /* fix bug: tab не нужно сдвигать */
  div::v-deep .v-slide-group__content { transform: translateX(0) !important; }
</style>

