<template>
  <v-app id="app"> <!--  oncontextmenu="return false" -->
    <router-view name="appbar"/>  <!--  Меню навигации  -->
    <v-main id="main">
      <v-progress-linear indeterminate absolute color="red" height="2" :active="loadStatus"/>
      <keep-alive :include="keepAlivePages">  <!--  Сохранение состояния окна при переходах  -->
        <router-view/>  <!--  Основное рабочее окно, для отображения страниц  -->
      </keep-alive>
      <notifications/>  <!--  Уведомления  -->
    </v-main>
  </v-app>
</template>

<script>
import notifications from "@/components/WebsiteShell/UIMainComponents/notifications"
import {mapGetters} from "vuex"

export default {
  name: 'App',
  components: {notifications},
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
  /*@import "~@/assets/css/reset.css";*/
  @import "~@/assets/css/normalize_original.css";
  @import "~@/assets/css/normalize_addition.css";
  @import "~@/main.css";
</style>
