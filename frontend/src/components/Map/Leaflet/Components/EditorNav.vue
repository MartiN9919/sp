<template>
  <div>
    <v-btn @click="dd">2</v-btn>
    <editorNavOsm
      v-bind="$attrs"
      v-on="$listeners"
    />
    <EditorNavObj
      v-bind="$attrs"
      v-on="$listeners"
    />
  </div>
</template>

<script>
/*



      @options2="$emit('update:options2', options2)"
      :selReset="selReset"
      @selectedGeometry="selected_geometry"

*/
import editorNavOsm from '@/components/Map/Leaflet/Components/EditorNavOsm';
import EditorNavObj from '@/components/Map/Leaflet/Components/EditorNavObj';

export default {
  name: 'EditorNav',
  components: { EditorNavObj, editorNavOsm, },
  inheritAttrs: false,
  // props: {
  //   options2: Object,
  // },

  // watch: {
  //   $attrs: function(val) {
  //     console.log('transit', val)
  //     //this.$emit('update:options2', val)
  //   },
  // },

  methods: {
    dd() {
      console.log('transit', this.options2)
      this.$emit('update:options2', {ff: 5})
      //this.$emit('selectedGeometry', '111111');
    },
  },


}


</script>