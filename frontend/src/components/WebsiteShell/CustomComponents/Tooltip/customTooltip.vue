<template>
  <v-tooltip
    v-bind="$attrs"
    :color="$CONST.APP.COLOR_OBJ"
    :disabled="status"
    transition="false"
    z-index="10000001"
    max-width="30%"
    open-delay="1000"
  >
    <template v-slot:activator="{ on }">
      <slot name="activator" :on="on"></slot>
    </template>

    <slot name="body">
      <div v-if="isDescription" class="subtitle-1">
        {{description || 'Описание отсутствует'}}
      </div>
      <v-divider v-if="isDescription && value" dark/>
      <component :is="component.tag"  v-bind="component.attrs"/>
    </slot>
  </v-tooltip>
</template>

<script>
import textViewer from "@/components/WebsiteShell/CustomComponents/Tooltip/TextViewer";
import geometryViewer from "@/components/WebsiteShell/CustomComponents/Tooltip/GeometryViewer";
import photoViewer from "@/components/WebsiteShell/CustomComponents/Tooltip/PhotoViewer";
import {mapGetters} from "vuex"

export default {
  name: "customTooltip",
  components: {textViewer, geometryViewer, photoViewer},
  props: {
    settings: Object,
    description: {
      type: String,
      default: ''
    },
    isDescription: {
      type: Boolean,
      default: false,
    },
    value: {
      default: null
    },
    type: {
      type: Object,
      default: null
    }
  },
  computed: {
    ...mapGetters(['globalTooltipStatus', 'baseLists']),
    status: function () { return !this.globalTooltipStatus },
    geometry: function () {
      return {tag: 'geometryViewer', attrs: {value: this.value}}
    },
    search: function () {
      return {tag: 'textViewer', attrs: {value: this.value ? this.value.title : ''}}
    },
    phone: function () {
      return {tag: 'textViewer', attrs: {value: this.value ? '+' + this.value : ''}}
    },
    checkbox: function () {
      return {tag: 'textViewer', attrs: {value: this.value ? 'Да' : 'Нет'}}
    },
    text: function () {
      return {tag: 'textViewer', attrs: {value: this.value}}
    },
    unknown: function () {
      return {tag: 'textViewer', attrs: {value: 'Создана'}}
    },
    photo: function () {
      if(this.value) {
        if(typeof this.value === 'object') {
          return {tag: 'textViewer', attrs: {value: this.value.file.name}}
        } else {
          return {tag: 'photoViewer', attrs: {value: this.value, ...this.settings}}
        }
      } else {
        return {tag: 'textViewer', attrs: {value: ''}}
      }
    },
    file: function () {
      if(this.value && typeof this.value === 'object') {
        return {tag: 'textViewer', attrs: {value: this.value.file.name}}
      } else {
        return {tag: 'textViewer', attrs: {value: this.value}}
      }
    },
    list: function () {
      if(!Number.isInteger(this.value)) {
        return {tag: 'textViewer', attrs: {value: this.value}}
      }
      let value
      for (const [listId, list] of Object.entries(this.baseLists)) {
        value = list.values.find(item => item.id === this.value)
        if (value) {
          return {tag: 'textViewer', attrs: {value: value.value}}
        }
      }
      return {tag: 'textViewer', attrs: {value: ''}}
    },
    component: function () {
      if(this.type) {
        switch (this.type.title) {
          case 'geometry':
            return this.geometry
          case 'search':
            return this.search
          case 'phone_number':
            return this.phone
          case 'checkbox':
            return this.checkbox
          case 'list':
            return this.list
          case 'unknown':
            return this.unknown
          case 'file':
            if (this.type.value === 'photo') {
              return this.photo
            } else if (this.type.value === 'any') {
              return this.file
            } else {
              return this.text
            }
          default:
            return this.text
        }
      } else {
        return this.text
      }
    }
  }
}
</script>

<style scoped>
.v-tooltip__content.menuable__content__active {
  opacity: 1 !important;
}
</style>