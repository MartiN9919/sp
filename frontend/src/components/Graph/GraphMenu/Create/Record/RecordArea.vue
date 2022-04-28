<template>
  <div>
    <record-body
        v-for="param in params"
        :key="param.baseParam.id"
        v-model="openedPanels"
        @click="createNewParam"
    >
      <template v-slot:title="">
        {{param.baseParam.title}}
      </template>
      <template v-slot:body="">
        <v-row
            v-for="(value, key) in param.new_values" :key="key"
            @keyup.alt.enter="deleteNewParam(param.baseParam.id, value)"
            no-gutters
            class="flex-nowrap px-2"
        >
          <record-input
              :param="getParam(param, value)"
              :type="param.baseParam.type"
              @deletable="deleteNewParam(param.baseParam.id, value)"
          ></record-input>
        </v-row>
        <old-records
            :base="param.baseParam"
            :values="param.values"
            :title="title"
            :settings="settings"
            @addDocToGraph="addDocToGraph"
            class="px-2"
        ></old-records>
      </template>
    </record-body>
  </div>
</template>

<script>
import RecordBody from "@/components/Graph/GraphMenu/Create/Record/RecordBody";
import RecordInput from "@/components/Graph/GraphMenu/Create/Record/RecordInput";
import OldRecords from "@/components/Graph/GraphMenu/Create/Record/OldRecords";
import _ from 'lodash';

export default {
  name: "RecordArea",
  components: {RecordBody, OldRecords, RecordInput},
  props: {
    settings: Object,
    params: Array,
    title: {
      type: String,
      default: null
    }
  },
  data: () => ({
    openedPanels: []
  }),
  methods: {
    getParam(param, value) {
      if(param.baseParam.title === 'geometry' && param.values.length > 0){
        let copyGeometry = _.cloneDeep(param.values[0])
        value.value = JSON.parse(copyGeometry.value)
      }
      return value
    },
    addDocToGraph(doc) {
      this.$emit('addDocumentToGraph', doc)
    },
    createNewParam(id) {
      this.$emit('createNewParam', id)
    },
    deleteNewParam(id, param) {
      this.$emit('deleteNewParam', { id: id, param: param })
    },
  },
  mounted() {
    this.openedPanels = this.params.map(p => p.baseParam.id)
  },
  watch: {
    params: function (value) {
      this.openedPanels = value.map(p => p.baseParam.id)
    }
  }
}
</script>

<style scoped>

</style>