<template>
  <div>
    <record-body
        v-for="param in params"
        :key="param.baseParam.id"
        v-model="openedPanels"
        @click="param.add({period: search})"
    >
      <template v-slot:title="">
        {{param.baseParam.title}}
      </template>
      <template v-slot:body="">
        <v-row
            v-for="(value, key) in param.new_values" :key="key"
            @keyup.alt.enter="param.remove(value)"
            no-gutters
            class="flex-nowrap px-2"
        >
          <record-input
              v-bind="$attrs"
              :param="getParam(param, value)"
              :base="param.baseParam"
              :conflict="conflict"
              @deletable="param.remove(value)"
              @depend="createDependParam"
              :search="search"
          ></record-input>
        </v-row>
        <old-records
            :base="param.baseParam"
            :values="param.values"
            :title="title"
            :rec-id="recId"
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
    params: Array,
    title: {
      type: String,
      default: null
    },
    conflict: {
      type: Boolean,
      default: false
    },
    recId: Number,
    search: Boolean
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
    createDependParam(payload) {
      const findParam = this.params.find(p =>
          p.baseParam.type.title === 'list' && p.baseParam.type.value === parseInt(payload.list[0])
      )
      if(findParam && !findParam.new_values.length) {
        findParam.add({value: payload.parent})
      }
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