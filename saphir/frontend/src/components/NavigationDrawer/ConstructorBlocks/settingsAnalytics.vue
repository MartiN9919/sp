<template>
  <v-row no-gutters class="align-center noselect">
    <v-col cols='auto pr-2 pb-2'>
      <div>{{variable.title}}:</div>
    </v-col>
    <v-col>
      <v-text-field color="teal" :type="variable.type" v-model="variable.value"></v-text-field>
    </v-col>
  </v-row>
</template>

<script>
import '@/assets/css/noselect.css'

export default {
  name: 'settingsAnalytics',
  props: {
    variable: Object
  }
}
</script>

<style scoped>

</style>
