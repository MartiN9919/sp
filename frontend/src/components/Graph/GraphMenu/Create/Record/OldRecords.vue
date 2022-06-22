<template>
  <table>
    <tbody class="py-2">
      <custom-tooltip
          v-for="(item, key) in values"
          :key="key"
          :value="item.value"
          :type="typeRecord"
          :settings="{recId: recId, objectId: base.objectId}"
          nudge-right="20"
          right
      >
        <template v-slot:activator="{ on }">
          <tr v-on="on">
            <info :base="base" :value="item.value" :date="item.date" :title="title" :rec-id="recId" :type="typeRecord"/>
            <document :doc="item.doc" @addToGraph="addDocToGraph"/>
            <date :date="item.date"/>
          </tr>
        </template>
      </custom-tooltip>
    </tbody>
  </table>
</template>

<script>
import GeometryParam from "@/components/WebsiteShell/CustomComponents/Dossier/geometryParam";
import CustomTooltip from "@/components/WebsiteShell/CustomComponents/Tooltip/customTooltip";
import Info from "@/components/Graph/GraphMenu/Create/Record/Cells/Info";
import Document from "@/components/Graph/GraphMenu/Create/Record/Cells/Document";
import Date from "@/components/Graph/GraphMenu/Create/Record/Cells/Date";


export default {
  name: "OldRecords",
  props: {
    values: Array,
    base: Object,
    title: String,
    recId: Number,
  },
  components: {Date, Document, Info, CustomTooltip, GeometryParam},
  computed: {
    typeRecord: function () {
      if(this.base.hasOwnProperty('type'))
        return this.base.type
    }
  },
  methods: {
    addDocToGraph(doc) {
      this.$emit('addDocToGraph', doc)
    }
  }
}
</script>

<style scoped>
table {
  width: 100%;
  border-spacing: initial;
  cursor: default;
}
table >>> span, table >>> a {
  font-size: 13px;
  text-decoration: none;
}
</style>