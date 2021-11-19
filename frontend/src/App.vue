<template>
  <v-app id="app" class="select_off"> <!--  oncontextmenu="return false" -->
    <router-view name="appbar"/>  <!--  Меню навигации  -->
    <v-main id="main">
      <v-progress-linear indeterminate absolute color="red" height="2" :active="loadStatus"/>
      <keep-alive :include="keepAlivePages">  <!--  Сохранение состояния окна при переходах  -->
        <router-view/>  <!--  Основное рабочее окно, для отображения страниц  -->
      </keep-alive>
      <router-view name="notification"/>  <!--  Уведомления  -->
    </v-main>
  </v-app>
</template>

<script>
import {mapGetters} from "vuex"

export default {
  name: 'App',
  computed: {
    ...mapGetters(['loadStatus']),
    keepAlivePages: function () {
      return Array.from(this.$router.options.routes.filter(
        r => r.meta && (this.$route.meta.auth ? r.meta.auth : !r.meta.auth)), r => r.name)
    },
  },
}
</script>

<style>
  @import "~@/main.css";
</style>
