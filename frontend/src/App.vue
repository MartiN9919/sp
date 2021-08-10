<template>
  <v-app id="app" class="select_off"> <!--  oncontextmenu="return false" -->
    <appBar></appBar>  <!--  Меню навигации  -->
    <v-main id="main">
      <v-progress-linear indeterminate absolute color="red" height="2" :active="loadStatus"></v-progress-linear>
      <keep-alive>  <!--  Сохранение состояния окна при переходах  -->
        <router-view></router-view>  <!--  Основное рабочее окно, для отображения страниц  -->
      </keep-alive>
      <alertsList></alertsList>  <!--  Уведомления  -->
    </v-main>
  </v-app>
</template>

<script>
import alertsList from './components/WebsiteShell/Notifications/alertsList'
import appBar from './components/WebsiteShell/AppBar/appBar'
import { mapGetters } from "vuex"

export default {
  name: 'App',
  components: { alertsList, appBar },
  computed: {
    ...mapGetters(['loadStatus'])
  }
}
</script>

<style>
  /***** отключить выделение текста  *****/
  .select_off {
    -moz-user-select: none;
    -webkit-user-select: none;
    -ms-user-select: none;
    -khtml-user-select: none;
    user-select: none;
    cursor: default;
  }
  ::-webkit-scrollbar {
    width: 10px;
  }
  ::-webkit-scrollbar-track {
    background: #FFFFFF;
  }
  ::-webkit-scrollbar-thumb {
    background : rgba(0, 0, 0, .1);
  }
  #app, #main {
    height: 100%;
  }
</style>
