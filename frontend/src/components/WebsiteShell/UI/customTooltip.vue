<template>
  <v-tooltip bottom transition="false" color="#00796B" z-index="10001" max-width="30%" content-class='custom-tooltip'>
    <template v-slot:activator="{ on }">
      <slot name="activator" :on="on"></slot>
    </template>
    <slot name="body">
      <v-img width="250" max-width="auto" v-if="typeTooltip==='picture'" :src="fileLink"></v-img>
      <v-img width="250" v-else-if="typeTooltip" :src="typeTooltip"></v-img>
      <div class="ma-2" v-else>{{bodyText || alternativeString}}</div>
    </slot>
  </v-tooltip>
</template>

<script>
import {getFileLink} from '@/plugins/axios_settings'

export default {
  name: "customTooltip",
  props: {
    settings: Object,
    bodyText: {
      type: String,
      default: ''
    },
    alternativeString: {
      type: String,
      default: 'Описание отсутствует'
    },
  },
  data: () => ({
    fileTypes: {
      'pdf': '~@/assets/img/fileTypes/PDF.png',
      'default': 'http://127.0.0.1:8000/static/src/vue/dist/img/fileTypes/EXE.png'
    },
    imageTypes: ['jpg', 'jpeg', 'png'],
  }),
  computed: {
    fileLink: function () { return getFileLink(this.settings.objectId, this.settings.recId, this.bodyText) },
    typeTooltip: function () {
      if(this.imageTypes.includes(this.bodyText.split('.').pop().toLowerCase()))
        return 'picture'
      if(Object.keys(this.fileTypes).includes(this.bodyText.split('.').pop()))
        return this.typeTooltip[this.bodyText.split('.').pop()]
      return this.fileTypes.default
    },
  }
}
</script>

<style scoped>
.v-tooltip__content.menuable__content__active {
  opacity: 1!important;
  box-shadow: 0 11px 15px -7px rgba(0, 0, 0, 0.2),
              0 24px 38px 3px rgba(0, 0, 0, 0.14),
              0 9px 46px 8px rgba(0, 0, 0, 0.12);
  padding: 0;
}
</style>