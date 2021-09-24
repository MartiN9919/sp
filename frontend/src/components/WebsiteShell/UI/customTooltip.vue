<template>
  <v-tooltip v-bind="$attrs" transition="false" color="#00796B" z-index="10001" max-width="30%" content-class='custom-tooltip'>
    <template v-slot:activator="{ on }">
      <slot name="activator" :on="on"></slot>
    </template>
    <slot name="body">
      <v-img width="250" max-width="auto" v-if="pictureType" :src="fileLink"></v-img>
      <div v-else class="ma-2">{{bodyText || alternativeString}}</div>
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
    imageTypes: ['jpg', 'jpeg', 'png'],
  }),
  computed: {
    fileLink: function () { return getFileLink(this.settings.objectId, this.settings.recId, this.bodyText) },
    pictureType: function () {
      return this.imageTypes.includes(this.bodyText.split('.').pop().toLowerCase());
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