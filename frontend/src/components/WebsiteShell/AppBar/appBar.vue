<template>
  <v-app-bar
    v-if="userInformation"
    app dense flat dark
    color="#00796B"
  >
    <v-app-bar-nav-icon
      @click="changeNavigationDrawerStatus"
    ></v-app-bar-nav-icon>

    <v-tabs fixed-tabs hide-slider>
      <v-tab
        v-for="tab in tabs"
        :key="tab.route"
        :to="tab.route">
        {{tab.title}}
        <v-icon right>{{ tab.icon }}</v-icon>
      </v-tab>
    </v-tabs>

    <v-spacer></v-spacer>

    <v-menu offset-y z-index="10001">
      <template v-slot:activator="{ on, attrs }">
        <v-btn large plain v-bind="attrs" v-on="on">
          {{ userInformation.first_name }} {{ userInformation.last_name }}
          <v-icon right size="24">mdi-account</v-icon>
        </v-btn>
      </template>

      <v-list rounded>
        <v-list-item @click="logOutUser" link>
          <v-list-item-icon><v-icon left>mdi-logout</v-icon></v-list-item-icon>
          <v-list-item-title>Выйти из системы</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-app-bar>
</template>

<script>
import NavigationDrawer from "../Mixins/NavigationDrawer"
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'appBar',
  mixins: [NavigationDrawer],
  data () {
    return {
      tabs: [
        { title: 'Карта', route: 'map', icon: 'mdi-map-search-outline' },
        { title: 'Граф', route: 'graph', icon: 'mdi-graph-outline' },
        { title: 'Отчеты', route: 'report', icon: 'mdi-file-document-multiple-outline' }
      ]
    }
  },
  computed: mapGetters(['userInformation']),
  methods: mapActions(['logOutUser'])
}
</script>

<style scoped>

</style>
