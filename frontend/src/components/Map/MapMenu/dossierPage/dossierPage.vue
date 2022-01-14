<template>
  <div class="dossier">
    <div class="content" v-if="selectedItem">
      <div class="params">
        <v-card v-for="param in selectedItem.params" :key="param.id + selectedItem.rec_id" tile class="mb-2">
          <v-hover v-if="getClassifierType(param)  === 'file_photo'" v-slot="{ hover }">
            <v-carousel hide-delimiters show-arrows-on-hover :show-arrows="param.values.length !== 1" height="200">
              <v-expand-transition>
                <div v-show="hover && param.values.length !== 1" class="delimiters">
                  <v-dialog width="min-content" class="dialog">
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
              <div class="picture-classifier">{{ getClassifierTitle(param) }}</div>
              <v-dialog v-for="(v, key) in param.values" :key="key" width="min-content" class="dialog">
                <template v-slot:activator="{ on, attrs }">
                  <v-carousel-item v-on="on" :src="getFile(v.value)"></v-carousel-item>
                </template>
                <v-img :src="getFile(v.value)"></v-img>
              </v-dialog>
            </v-carousel>
          </v-hover>
          <div v-else class="d-flex justify-space-between">
            <v-card-title style="word-break: inherit">{{ getClassifierTitle(param) }}</v-card-title>
            <v-card-text class="py-1 text-end d-flex flex-column justify-center" style="width: max-content">
              <div v-for="(v, key) in param.values" :key="key">
                <v-dialog
                  v-if="getClassifierType(param) === 'geometry' || getClassifierType(param) === 'geometry_point'"
                  class="dialog"
                  style="z-index:1000002"
                  width="60%"
                  height="80%"
                  v-model="dialog"
                  @keydown.esc="dialog = false"
                  persistent
                  transition="dialog-bottom-transition"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <div v-bind="attrs" v-on="on" class="py-1 teal--text">
                      <p class="mb-0 text-body-1" style="line-height: 1em; font-style: oblique">
                        {{ getClassifierType(param) === 'geometry' ? 'Геометрия' : 'Точка' }}
                      </p>
                      <p class="mb-0" style="line-height: 1em; font-size: 0.8em">{{ v.date }}</p>
                    </div>
                  </template>
                  <v-card>
                    <v-card-title class="text-h7">УКАЗАТЬ ЗДЕСЬ TITLE</v-card-title>
                    <v-divider></v-divider>
                    <LeafletViewer
                      v-if="dialog"
                      style="height: 70vh;"
                      :fc="JSON.parse(v.value)"
                      :controls="true"
                    />
                    <v-divider></v-divider>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn :color="$CONST.APP.COLOR_OBJ" text @click="dialog=false">Ок</v-btn>
                    </v-card-actions>
                  </v-card>
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
      <control-menu :buttons="controlButtons" @change="editObject" @addToGraph="addToGraph" class="control"></control-menu>
    </div>
    <div v-else class="text-h5 text-uppercase text-center grey--text pt-6">Объект не выбран</div>
  </div>
</template>

<script>
import ControlMenu from "@/components/Graph/GraphMenu/createPageComponents/controlMenu"
import LeafletViewer from "@/components/Map/Leaflet/LeafletViewer"
import {getDownloadFileLink} from '@/plugins/axiosSettings'
import {mapActions, mapGetters} from "vuex"
import router from "@/router"

export default {
  name: "map-dossier",
  components: {ControlMenu, LeafletViewer},
  data: () => ({
    dialog: false,
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
  computed: mapGetters(['SCRIPT_GET_ITEM_SEL', 'baseClassifier']),
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

.dialog {
  z-index: 1000002
}
.dossier {
  height: 100%;
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