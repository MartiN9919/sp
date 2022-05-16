<template>
  <v-col class="pa-0 overflow-auto">
    <v-row no-gutters v-for="param in photoParams" :key="`${param.baseParam.id}_${recId}`" v-if="param.values.length">
      <photo-param :param="param" :rec-id="recId" :object-id="objectId"/>
    </v-row>
    <table>
      <dossier-param
        v-for="param in simpleParams"
        :key="`${param.baseParam.id}_${recId}`"
        :param="param"
        :rec-id="recId"
        :object-id="objectId"
        :title="title"
      />
    </table>
  </v-col>
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
    title: {
      type: String,
      default: null
    }
  },
  computed: {
    photoParams: function () {
      return this.params.filter(p => p.baseParam.type.title === 'file' && p.baseParam.type.value === 'photo' && p.values.length)
    },
    simpleParams: function () {
      return this.params.filter(p => p.baseParam.type.title !== 'file' && p.baseParam.type.value !== 'photo' && p.values.length)
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