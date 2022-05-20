<template>
  <v-dialog v-model="dossier" width="40%" class="description-dialog">
    <v-card tile>
      <dossier :params="params" :rec-id="recId" :object-id="objectId" :title="title"/>
    </v-card>
  </v-dialog>
</template>

<script>
import Dossier from "@/components/WebsiteShell/CustomComponents/Dossier/dossier"

export default {
  name: "description",
  components: {Dossier},
  props: {
    dialog: {
      type: Boolean,
      default: false
    },
    params: Array,
    recId: {
      type: Number,
      default: 0
    },
    objectId: {
      type: Number,
      default: 0
    },
    title: {
      type: String,
      default: null
    },
  },
  model: {
    prop: 'dialog',
    event: 'dialog'
  },
  computed: {
    dossier: {
      get: function () { return this.dialog },
      set: function (value) { this.$emit('dialog', value) }
    },
  }
}
</script>

<style scoped>
.description-dialog {
  z-index: 100000;
}
>>> .v-dialog {
  max-height: 60% !important;
}
</style>