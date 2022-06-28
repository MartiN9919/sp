<template>
  <v-dialog v-model="dossier" scrollable width="40%" class="dialog">
    <v-card v-if="dossier" tile>
      <v-card-text class="pa-0 black--text">
        <dossier :params="params" :rec-id="recId" :object-id="objectId" :title="selectedItem.title"/>
      </v-card-text>
      <control-menu :buttons="controlButtons" @change="editObject" @addToGraph="showObject"/>
    </v-card>
  </v-dialog>
</template>

<script>
import Dossier from '@/components/WebsiteShell/CustomComponents/Dossier/dossier'
import ControlMenu from '@/components/Graph/GraphMenu/Create/Modules/ControlMenu'
import {mapActions, mapGetters} from "vuex";
import router from "@/router";

export default {
  name: "Description",
  components: {Dossier, ControlMenu},
  props: {
    viewDat: { type: Array, default: () => undefined, },  // [obj_id, rec_id]
  },
  data: () => ({
    dossier: false,
    selectedItem: null,
    controlButtons: [
      {
        title: 'Добавить на граф',
        action: 'addToGraph',
        disabled: true
      },
      {
        title: 'Изменить',
        action: 'change',
        disabled: true
      },
    ]
  }),
  computed: {
    ...mapGetters(['SCRIPT_GET_ITEM_SEL']),
    objectId: function () {
      return this.selectedItem.base.id
    },
    recId: function () {
      return this.selectedItem.recId
    },
    payload: function () {
      return {object_id: this.objectId, rec_id: this.recId, title: this.selectedItem.title}
    },
    params: function () {
      return this.selectedItem.params
    }
  },
  methods: {
    ...mapActions(['getObject', 'setEditableObject', 'addObjectToGraph']),
    toGraph() {
      return new Promise(function(resolve, reject) {
        if (router.history.current.name === 'Graph') {
          resolve()
        } else {
          router.push({name: 'Graph'}).then(() => resolve()).catch(() => reject())
        }
      })
    },
    editObject() {
      this.toGraph().then(() => {
        this.setEditableObject(this.payload)
        this.dossier = false
      })
    },
    showObject() {
      this.toGraph().then(() => {
        this.addObjectToGraph({
          object: this.payload,
          action: {
            name: 'addGeometryToGraph',
            payload: this.payload.title
          }
        })
        this.dossier = false
      })
    },
  },
  watch: {
    viewDat: {
      handler(val) {
        if (val != undefined)
          this.getObject({object_id: val[0], rec_id: val[1]})
              .then(r => {
                this.selectedItem = r
                this.dossier = true
              })
        else {
          this.selectedItem = null
          this.dossier = false
        }
      },
      deep: true,
    },
  },
}
</script>

<style scoped>
.dialog {
  z-index: 100001;
}
>>> .v-dialog {
  max-height: 60% !important;
}
</style>