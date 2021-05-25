<template>
  <v-app>
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
