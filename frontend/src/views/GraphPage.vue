<template>
  <split-panel>
    <template v-slot:firstPane>
      <graph-menu></graph-menu>
    </template>
    <template v-slot:secondPane>
      <work-place></work-place>
    </template>
  </split-panel>
</template>

<script>
import SplitPanel from "../components/WebsiteShell/UI/splitPanel"
import workPlace from '../components/Graph/Graph/workPlace'
import graphMenu from '../components/Graph/GraphMenu/graphMenu'
import { mapActions } from "vuex";

export default {
  name: 'GraphPage',
  components: {SplitPanel, workPlace, graphMenu,},
  methods: {
    ...mapActions(['setDefaultValueActiveTool', 'getListOfPrimaryObjects', ]),
  },
  mounted() {
    this.getListOfPrimaryObjects()
    this.setDefaultValueActiveTool()
  },
}
</script>

<style >

</style>
