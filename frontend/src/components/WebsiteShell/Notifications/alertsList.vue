<template>
  <v-col class="alert-list">
    <v-slide-x-reverse-transition group>
      <alert v-for="alert in alertsList" :key="alert.id" :alert="alert" @removeAlert="removeAlertFromList"></alert>
    </v-slide-x-reverse-transition>
  </v-col>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import alert from './alert'

export default {
  name: 'alertsList',
  components: {
    alert
  },
  methods: {
    ...mapActions(['removeAlertFromList'])
  },
  computed: {
    ...mapGetters(['alertsList'])
  }
}
</script>

<style scoped>
  ::-webkit-scrollbar {
    width: 0;
  }
  .alert-list {
    position: absolute;
    z-index: 99999999999999;
    bottom: 0;
    max-width: 25em;
    max-height: 50%;
    overflow-y: auto;
    right: 0;
  }
</style>
