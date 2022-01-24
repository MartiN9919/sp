<template>
  <v-dialog v-model="dossier" width="40%" style="z-index: 100000" overlay-opacity="0" content-class="overflow-hidden">
    <dossier :params="params" :rec-id="recId" :object-id="objectId"/>
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

</style>