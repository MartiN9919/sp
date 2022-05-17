<template>
  <v-dialog v-model="dossier" scrollable width="40%" overlay-opacity="0">
    <v-card v-if="dossier" tile>
      <v-card-text class="pa-0">
        <dossier :params="params" :rec-id="recId" :object-id="objectId" :title="selectedItem.title"/>
      </v-card-text>
      <control-menu :buttons="controlButtons" @change="editObject" @addToGraph="toGraph"/>
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
    editObject() {
      router.push({name: 'Graph'}).then(() => this.setEditableObject(this.payload))
    },
    toGraph() {
      router.push({name: 'Graph'}).then(() => this.addObjectToGraph({
        object: this.payload,
        action: {
          name: 'addGeometryToGraph',
          payload: this.payload.title
        }
      }))
    },
  },
  watch: {
    SCRIPT_GET_ITEM_SEL: {
      handler: function (v) {
        let value = JSON.parse(v)
        if (value.length)
          this.getObject({rec_id: value[0].rec_id, object_id: value[0].obj_id})
              .then(r => {
                this.selectedItem = r
                this.dossier = true
              })
        else {
          this.selectedItem = null
          this.dossier = false
        }
      },
      immediate: true
    },
  },
}
</script>

<style scoped>

</style>