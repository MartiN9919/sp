<template>
  <div class="dossier">
    <div class="content" v-if="selectedItem">
      <div class="params">
        <v-card v-for="param in selectedItem.params" :key="param.id + selectedItem.rec_id" tile class="mb-2">
          <v-carousel v-if="getClassifierType(param)  === 'file_photo'" :show-arrows="param.values.length !== 1" class="carousel" height="200">
            <div class="picture-classifier">{{ getClassifierTitle(param) }}</div>
            <v-dialog v-for="(v, key) in param.values" :key="key" width="min-content" class="dialog">
              <template v-slot:activator="{ on, attrs }">
                <v-carousel-item v-on="on" :src="getFile(v.value)"></v-carousel-item>
              </template>
              <v-img :src="getFile(v.value)"></v-img>
            </v-dialog>
          </v-carousel>
          <div v-else class="d-flex justify-space-between">
            <v-card-title style="word-break: inherit">{{ getClassifierTitle(param) }}</v-card-title>
            <v-card-text class="py-1 text-end d-flex flex-column justify-center" style="width: max-content">
              <div v-for="(v, key) in param.values" :key="key">
                <v-dialog v-if="getClassifierType(param) === 'geometry'" width="80%" class="dialog">
                  <template v-slot:activator="{ on, attrs }">
                    <div v-bind="attrs" v-on="on" class="py-1 teal--text">
                      <p class="mb-0 text-body-1" style="line-height: 1em; font-style: oblique">Геометрия</p>
                      <p class="mb-0" style="line-height: 1em; font-size: 0.8em">{{ v.date }}</p>
                    </div>
                  </template>
                  <LeafletEditor :fc_parent_prop="JSON.parse(v.value)" :modeEnabled="{marker: false , line: false, polygon: false}"/>
                </v-dialog>
                <div v-else class="py-1">
                  <p class="mb-0 text-body-1" style="line-height: 1em; font-style: oblique">{{v.value}}</p>
                  <p class="mb-0" style="line-height: 1em; font-size: 0.8em">{{ v.date }}</p>
                </div>
              </div>
            </v-card-text>
          </div>
        </v-card>
      </div>
      <v-divider></v-divider>
      <control-menu :buttons="controlButtons" @change="editObject" @addToGraph="addToGraph" class="control"></control-menu>
    </div>
    <div v-else class="text-h5 text-uppercase text-center grey--text pt-6">Выбирете объект</div>
  </div>
</template>

<script>
import {mapActions, mapGetters} from "vuex"
import {getDownloadFileLink} from '@/plugins/axios_settings'
import LeafletEditor from "../../../Map/Leaflet/LeafletEditor"
import ControlMenu from "@/components/Graph/GraphMenu/createPageComponents/controlMenu"
import router from "@/router"

export default {
  name: "map-dossier",
  components: {ControlMenu, LeafletEditor},
  data: () => ({
    selectedItem: null,
    controlButtons: [
        {
          title: 'Добавить на граф',
          action: 'addToGraph',
        },
        {
          title: 'Изменить',
          action: 'change',
        },
      ]
  }),
  computed: {
    ...mapGetters(['SCRIPT_GET_ITEM_SEL', 'baseClassifier']),
  },
  methods: {
    ...mapActions(['getObjectFromServer', 'setEditableObject', 'addObjectToGraph']),
    getFile(link) {
      return getDownloadFileLink(this.selectedItem.object_id, this.selectedItem.rec_id, link)
    },
    getClassifierTitle(param) {
      return this.baseClassifier(param.id).title
    },
    getClassifierType(param) {
      return this.baseClassifier(param.id).type.title
    },
    editObject() {
      router.push({name: 'Graph'})
      .then(() => {
        this.setEditableObject({
          objectId: this.selectedItem.object_id,
          recId: this.selectedItem.rec_id
        })
      })
    },
    addToGraph() {
      router.push({name: 'Graph'})
        .then(() => {
          this.addObjectToGraph({
            objectId: this.selectedItem.object_id,
            recId: this.selectedItem.rec_id
          })
        })
    },
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
.dossier {
  max-height: 100%;
  overflow-y: hidden;
}
.content {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.params {
  height: calc(100% - 3em);
  overflow-y: auto;
}
.control {
  height: 3em;
}
</style>