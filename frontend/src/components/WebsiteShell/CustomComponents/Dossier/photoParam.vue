<template>
  <v-hover v-slot="{ hover }">
    <v-carousel hide-delimiters show-arrows-on-hover :show-arrows="param.values.length !== 1" height="200" class="cursor-pointer">
      <v-expand-transition>
        <div v-show="hover && param.values.length !== 1" class="delimiters">
          <v-dialog width="min-content">
            <template v-slot:activator="{ on, attrs }">
              <v-btn text v-on="on" width="100%">
                Посмотреть все
                <v-icon right>mdi-image-multiple</v-icon>
              </v-btn>
            </template>
            <v-img v-for="(v, key) in param.values" :key="key" :src="getFile(v.value)"></v-img>
          </v-dialog>
        </div>
      </v-expand-transition>
      <div class="picture-classifier">{{ param.baseParam.title }}</div>
      <v-dialog v-for="(v, key) in param.values" :key="key" width="min-content" class="dialog">
        <template v-slot:activator="{ on, attrs }">
          <v-carousel-item v-on="on" :src="getFile(v.value)"></v-carousel-item>
        </template>
        <v-img :src="getFile(v.value)"></v-img>
      </v-dialog>
    </v-carousel>
  </v-hover>
</template>

<script>
import {getDownloadFileLink} from "@/plugins/axiosSettings"

export default {
  name: "photoParam",
  props: {
    param: Object,
    recId: Number,
    objectId: Number,
  },
  methods: {
    getFile(link) {
      return getDownloadFileLink(this.objectId, this.recId, link)
    },
  }
}
</script>

<style scoped>
.picture-classifier {
  position: absolute;
  left: 20px;
  z-index: 1;
  color: white;
  text-shadow: -1px 0 black, 0 1px black, 1px 0 black, 0 -1px black;
}

.delimiters {
  position: absolute;
  bottom: 0;
  z-index: 1;
  height: min-content;
  width: 100%;
  background-color: rgba(0, 0, 0, 0.2);
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>