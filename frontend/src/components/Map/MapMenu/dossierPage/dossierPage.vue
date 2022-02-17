<template>
  <div class="dossier">
    <div class="content" v-if="selectedItem">
      <div class="params">
        <dossier :params="selectedItem.params" :rec-id="recId" :object-id="objectId" :title="selectedItem.title"/>
      </div>
      <control-menu :buttons="controlButtons" @change="editObject" @addToGraph="toGraph" class="control"></control-menu>
    </div>
    <div v-else class="text-h5 text-uppercase text-center grey--text pt-6">Объект не выбран</div>
  </div>
</template>

<script>
import Dossier from "@/components/WebsiteShell/CustomComponents/Dossier/dossier"
import ControlMenu from "@/components/Graph/GraphMenu/createPageComponents/controlMenu"
import {mapActions, mapGetters} from "vuex"
import router from "@/router"

export default {
  name: "map-dossier",
  components: {Dossier, ControlMenu},
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
    ...mapGetters(['SCRIPT_GET_ITEM_SEL']),
    objectId: function () {
      return this.selectedItem.base.id
    },
    recId: function () {
      return this.selectedItem.recId
    },
    payload: function () {
      return {object_id: this.objectId, rec_id: this.recId}
    }
  },
  methods: {
    ...mapActions(['getObject', 'setEditableObject', 'addObjectToGraph']),
    editObject() {
      router.push({name: 'Graph'}).then(() => this.setEditableObject(this.payload))
    },
    toGraph() {
      router.push({name: 'Graph'}).then(() => this.addObjectToGraph(this.payload))
    },
  },
  watch: {
    SCRIPT_GET_ITEM_SEL: {
      handler: function (v) {
        let value = JSON.parse(v)
        if (value.length)
          this.getObject({rec_id: value[0].rec_id, object_id: value[0].obj_id})
            .then(r => this.selectedItem = r)
        else this.selectedItem = null
      },
      immediate: true
    },
  }
}
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}
.dossier {
  height: 100%;
  overflow: hidden;
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