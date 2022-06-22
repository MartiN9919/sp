<template>
  <div class="py-1">
    <info-param :value="getValue" :title="title" :date="getDate" :base="base" :rec-id="recId"/>
    <div style="font-size: 10px; font-style: italic">
      <span v-if="document" @click="addDocumentToGraph" class="cursor-pointer teal--text">{{document.title}}</span><br>
      <span>{{getDate}}</span>
    </div>
  </div>
</template>

<script>
import InfoParam from "@/components/WebsiteShell/CustomComponents/Dossier/infoParam"
import {mapActions} from "vuex"

export default {
  name: "dossierValue",
  components: {InfoParam},
  props: {
    value: Object,
    title: {
      type: String,
      default: null
    },
    recId: Number,
    base: Object,
    document: Object
  },
  computed: {
    getValue: function () {
      return this.value.value
    },
    getDate: function () {
      return this.value.date
    },
  },
  methods: {
    ...mapActions(['addObjectToGraph']),
    addDocumentToGraph() {
      this.addObjectToGraph({
        object: this.document,
        action: {
          name: 'addDocumentToGraph',
          payload: this.document.title
        }
      })
    }
  }
}
</script>

<style scoped>

</style>