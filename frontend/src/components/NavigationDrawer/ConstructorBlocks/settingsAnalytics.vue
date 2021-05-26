<template>
  <v-row no-gutters class="align-center noselect">
    <v-col cols='auto pr-2 pb-2'>
      <div>{{variable.title}}:</div>
    </v-col>
    <v-col>
      <map-dialog
          v-if="variable.type === 'geometry'"
          :value="variable.value !== null ? variable.value : [2, 3]"
          @changeValueGeometry="variable.value = $event"
      ></map-dialog>
      <v-text-field v-else color="teal" :type="variable.type" v-model="variable.value"></v-text-field>
    </v-col>
  </v-row>
</template>

<script>
import '@/assets/css/noselect.css'
import './mapDialog'
import mapDialog from "./mapDialog";

export default {
  name: 'settingsAnalytics',
  components: {mapDialog, },
  props: {
    variable: Object
  },
}
</script>

<style scoped>

</style>
