<template>
  <v-app id="app" class="select-off"> <!--  oncontextmenu="return false" -->
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/doc">Doc</router-link>
      <router-link to="/info">Info</router-link>
      <router-link to="/about">About</router-link>
    </div>
    <router-view/>
    <notifications/>  <!--  Уведомления  -->
  </v-app>
</template>

<script>
import notifications from "@/components/WebsiteShell/UIMainComponents/notifications"
export default {
  name: 'App',
  components: {notifications},
}
</script>

<style lang="scss">
  /*@import "~@/assets/css/reset.css";*/
  @import "~@/assets/css/normalize_original.css";
  @import "~@/assets/css/normalize_addition.css";
  @import "~@/main.css";
</style>
