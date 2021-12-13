<template>
  <v-card height="100%">
    <v-tabs
      ref="tabs"
      v-model="tab.value"
      :color="$CONST.APP.COLOR_OBJ"
      background-color="transparent"
      grow style="height: 100%"
    >
      <v-tabs-slider :color="$CONST.APP.COLOR_OBJ"/>
      <v-tab href="#tab-obj">
        <v-icon left>mdi-vector-polygon</v-icon>
        Объекты
      </v-tab>
      <v-tab href="#tab-osm">
        <v-icon left>mdi-web</v-icon>
        Мир
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

import router       from '@/router';
import UserSetting  from "@/store/addition"
import editorNavOsm from '@/components/Map/Leaflet/Components/Editor/EditorNavOsm';
import EditorNavObj from '@/components/Map/Leaflet/Components/Editor/EditorNavObj';
import MixResize    from '@/components/Map/Leaflet/Mixins/Resize';

export default {
  name: 'EditorNav',

  components: { EditorNavObj, editorNavOsm, },
  mixins: [ MixResize, ],

  inheritAttrs: false,

  data: () => ({
    tab: new UserSetting('EditorNav.tab', null),
  }),

  methods: {
    on_resize () {                   // fire from MixResize
      this.$refs.tabs.callSlider();  // устранение бага со слайдером
    },
  },


}


</script>

<style scoped lang="scss">
  /* fix bug: build height */
  div::v-deep .v-tabs { height: 100%; }
  div::v-deep .v-sheet { height: 100%; }

  /* fix bug: кнопка влево не нужна */
  div::v-deep .v-slide-group__prev { display: none !important; }
  div::v-deep .v-tabs-items { height: calc(100% - 48px); }
  div::v-deep .v-window-item  { height: 100%; }
  div::v-deep .v-window__container  { height: 100%; }

  /* fix bug: tab не нужно сдвигать */
  div::v-deep .v-slide-group__content { transform: translateX(0) !important; }
</style>

