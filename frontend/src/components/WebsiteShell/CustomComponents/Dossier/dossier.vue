<template>
  <v-dialog v-model="dossier" width="40%" style="z-index: 100000" overlay-opacity="0" content-class="overflow-hidden">
    <v-card tile class="overflow-auto">
      <v-col>
        <v-row no-gutters v-for="param in photoParams" :key="param.id" v-if="param.values.length">
          <photo-param :param="param" :rec-id="recId" :object-id="objectId"/>
        </v-row>
        <table>
          <dossier-param v-for="param in simpleParams" :key="param.id" :param="param" :rec-id="recId" :object-id="objectId"/>
        </table>
      </v-col>
    </v-card>
  </v-dialog>
</template>

<script>
import PhotoParam from "@/components/WebsiteShell/CustomComponents/Dossier/photoParam"
import DossierParam from "@/components/WebsiteShell/CustomComponents/Dossier/dossierParam"

export default {
  name: "dossier",
  components: {DossierParam, PhotoParam},
  props: {
    params: Array,
    recId: Number,
    objectId: Number,
    dialog: {
      type: Boolean,
      default: false
    }
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
    photoParams: function () {
      return this.params.filter(p => p.baseParam.type.title === 'file_photo' && p.values.length)
    },
    simpleParams: function () {
      return this.params.filter(p => p.baseParam.type.title !== 'file_photo' && p.values.length)
    }
  }
}
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}

</style>