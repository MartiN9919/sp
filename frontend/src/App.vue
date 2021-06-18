<template>
  <v-app class="select_off"> <!--  oncontextmenu="return false" -->
    <appBar></appBar>  <!--  Меню навигации  -->
    <v-main>
      <v-progress-linear
        indeterminate
        absolute
        color="red"
        height="2"
        style="width: 100%"
        :active="$store.getters.progressLinearStatus"
      ></v-progress-linear>
      <keep-alive>  <!--  Сохранение состояния окна при переходах  -->
        <router-view></router-view>  <!--  Основное рабочее окно, для отображения страниц  -->
      </keep-alive>
      <alertsList></alertsList>  <!--  Уведомления  -->
    </v-main>
  </v-app>
</template>

<script>
import alertsList from './components/Notifications/alertsList'
import appBar from './components/AppBar/appBar'

export default {
  name: 'App',
  components: { alertsList, appBar }
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
</style>
