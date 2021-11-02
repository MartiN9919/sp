<template>
  <div style="max-height: 100%" class="overflow-y-auto">
    <div v-if="selectedItem" class="d-flex flex-column">
      <div class="text-center text-h5 text-uppercase py-3">{{ selectedItem.title }}</div>
      <v-card v-for="param in selectedItem.params" :key="param.id + selectedItem.rec_id" tile class="my-1">
        <v-carousel v-if="getClassifierType(param)  === 'file_photo'" class="carousel" height="200">
          <div class="picture-classifier">{{ getClassifierTitle(param) }}</div>
          <v-dialog v-for="(v, key) in param.values" :key="key" width="min-content" class="dialog">
            <template v-slot:activator="{ on, attrs }">
              <v-carousel-item v-on="on" :src="file(v.value)"></v-carousel-item>
            </template>
            <v-img :src="file(v.value)"></v-img>
          </v-dialog>
        </v-carousel>
        <div v-else class="d-flex justify-space-between">
          <v-card-title class="flex-shrink-0">{{ getClassifierTitle(param) }}</v-card-title>
          <v-card-text class="py-1 text-end d-flex flex-column justify-center" style="width: max-content">
            <div v-for="(v, key) in param.values" :key="key">
              <v-dialog v-if="getClassifierType(param) === 'geometry'" width="80%" class="dialog">
                <template v-slot:activator="{ on, attrs }">
                  <p v-bind="attrs" v-on="on" class="mb-0 teal--text">Геометрия ({{ v.date }})</p>
                </template>
                <LeafletEditor :fc_parent_prop="JSON.parse(v.value)" :modeEnabled="{marker: false , line: false, polygon: false}"/>
              </v-dialog>
              <p v-else class="mb-0">{{ v.value }} ({{ v.date }})</p>
            </div>
          </v-card-text>
        </div>
      </v-card>
    </div>
    <div v-else class="text-h5 text-uppercase text-center">Выбирете объект</div>
  </div>
</template>

<script>
import {mapActions, mapGetters} from "vuex"
import {getDownloadFileLink} from '@/plugins/axios_settings'
import CustomTooltip from "@/components/WebsiteShell/UI/customTooltip"
import LeafletEditor from "../../../Map/Leaflet/LeafletEditor"

export default {
  name: "map-dossier",
  components: {CustomTooltip, LeafletEditor},
  data: () => ({
    selectedItem: null,
  }),
  computed: {
    ...mapGetters(['SCRIPT_GET_ITEM_SEL', 'baseClassifier']),
  },
  methods: {
    ...mapActions(['getObjectFromServer']),
    file(link) {
      return getDownloadFileLink(this.selectedItem.object_id, this.selectedItem.rec_id, link)
    },
    getClassifierTitle(param) {
      return this.baseClassifier(param.id).title
    },
    getClassifierType(param) {
      return this.baseClassifier(param.id).type.title
    }
  },
  watch: {
    SCRIPT_GET_ITEM_SEL: {
      handler: function (v) {
        let value = JSON.parse(v)
        if (value.length)
          this.getObjectFromServer({params: {record_id: value[0].rec_id, object_id: value[0].obj_id}})
            .then(r => { this.selectedItem = r })
        else this.selectedItem = null
      },
      immediate: true
    },
  }
}
</script>

<style scoped>
.carousel >>> .v-image__image {
  height: 200px;
}

.picture-classifier {
  position: absolute;
  left: 20px;
  z-index: 1;
  color: white;
  text-shadow: -1px 0 black, 0 1px black, 1px 0 black, 0 -1px black;
}

.dialog {
  z-index: 1000002
}
</style>