<template>
  <a tabindex="-1" v-if="isFile" :href="downloadLink" target="_blank" class="teal--text">{{ value }}</a>
  <geometry-param v-else-if="isGeometry" :value="value" :title="title">
    {{ geometryTextValue }}
  </geometry-param>
  <span v-else class="word-wrap">
      {{ text }}
      <v-dialog width="40%" scrollable>
        <template v-slot:activator="{ on, attrs }">
          <span v-on="on" v-bind="attrs" v-if="showText" class="cursor-pointer teal--text">еще</span>
        </template>
        <v-card>
          <v-card-title>{{base.title}} <v-spacer/> <span class="subtitle-2">{{date}}</span></v-card-title>
          <v-card-subtitle>{{base.hint}}</v-card-subtitle>
          <v-card-actions>
            <v-text-field v-model="search" solo hide-details color="teal" label="Поиск по тексту" :suffix="suffix">
              <template v-if="search.length" v-slot:append>
                <v-icon @click="plusPosition" class="cursor-pointer icon">mdi-chevron-down</v-icon>
                <v-icon @click="minusPosition" class="cursor-pointer icon">mdi-chevron-up</v-icon>
                <v-icon @click="clear" class="cursor-pointer icon">mdi-close</v-icon>
              </template>
            </v-text-field>
          </v-card-actions>
          <v-card-text id="full-text" class="text-justify overflow-x-hidden">
            <v-lazy v-for="(text, key) in fullText" :key="key" :options="{threshold: .25}" transition="fade-transition">
              <div v-html="text"></div>
            </v-lazy>
          </v-card-text>
        </v-card>
      </v-dialog>
    </span>
</template>

<script>
import GeometryParam from "@/components/WebsiteShell/CustomComponents/Dossier/geometryParam"
import {getDownloadFileLink} from "@/plugins/axiosSettings";

export default {
  name: "infoParam",
  components: {GeometryParam},
  props: {
    value: String,
    title: String,
    date: String,
    recId: Number,
    base: Object
  },
  data: () => ({
    searchString: '',
    position: null
  }),
  computed: {
    search: {
      get: function () {
        return this.searchString
      },
      set: function (value) {
        this.searchString = value
        this.position = null
      }
    },
    positions: function () {
      return [...this.value.matchAll(new RegExp(this.search, 'gi'))].map(a => a.index)
    },
    fullText: function () {
      if(this.search.length > 0) {
        return this.value.replaceAll(
            new RegExp(this.search,"gi"),
            (match, key) => {
              const id = `search-${key}`
              const style = `background-color: ${key === this.positions[this.position]
                  ? 'rgba(255,42,74,0.75)'
                  : 'rgba(255,245,42,0.75)'
              }`
              return `<span id="${id}" style="${style}">${match}</span>`;
            }
        ).split('\n').filter(s => s.length)
      } else {
        return this.value.split('\n').filter(s => s.length)
      }
    },
    suffix: function () {
      if(this.position !== null) {
        return `${this.position + 1}/${this.positions.length}`
      } else if(this.search.length) {
        return `0/${this.positions.length}`
      } else {
        return ''
      }
    },
    showText: function () {
      return this.value.length > 255
    },
    text: function () {
      if(this.value) {
        if(this.showText) {
          return this.value.slice(0, 255) + '...'
        } else
          return this.value
      } else {
        return 'Создана'
      }
    },
    geometryTextValue: function () {
      return this.base.type.value === 'polygon' ? 'Геометрия' : 'Точка'
    },
    isFile: function () {
      return this.base.type.title === 'file'
    },
    isGeometry: function () {
      return this.base.type.title === 'geometry'
    },
    downloadLink: function () {
      return getDownloadFileLink(this.base.objectId, this.recId, this.value)
    },
  },
  methods: {
    scroll() {
      this.$vuetify.goTo(
          '#search-' + this.positions[this.position],
          { duration: 300, offset: 100, easing: 'easeInOutCubic', container: '#full-text' })
    },
    clear() {
      this.search = ''
    },
    plusPosition() {
      if(this.position === null) {
        this.position = 0
      } else {
        if(this.position === this.positions.length - 1) {
          this.position = 0
        } else {
          this.position += 1
        }
      }
      this.scroll()
    },
    minusPosition() {
      if(this.position) {
        this.position -= 1
      } else {
        this.position = this.positions.length - 1
      }
      this.scroll()
    }
  }
}
</script>

<style scoped>
.icon:hover {
  color: teal;
}
.word-wrap {
  word-wrap: anywhere;
}
</style>