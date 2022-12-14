<template>
  <v-app-bar v-if="userInformation" app dense flat dark :color="$CONST.APP.COLOR_OBJ">
    <v-app-bar-nav-icon @click="drawer = !drawer"/>
    <v-tabs fixed-tabs hide-slider>
      <v-tab v-for="tab in appbarTabs" :key="tab.route" :to="tab.route" tabindex="-1">
        {{tab.title}}<v-icon right>{{ tab.icon }}</v-icon>
      </v-tab>
    </v-tabs>
    <v-spacer/>
    <v-menu offset-y z-index="100003" :close-on-content-click="false">
      <template v-slot:activator="{ on, attrs }">
        <v-btn large plain v-bind="attrs" v-on="on" tabindex="-1">
          {{ userInformation.first_name }} {{ userInformation.last_name }}
          <v-icon right size="24">mdi-account</v-icon>
        </v-btn>
      </template>
      <v-card max-width="min-content">
        <v-list>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>
                {{userInformation.first_name}}
                {{userInformation.last_name}}
                ({{userInformation.username}})
              </v-list-item-title>
              <v-list-item-subtitle v-if="!!staffStatus">Статус персонала: {{staffStatus}}</v-list-item-subtitle>
              <v-list-item-subtitle>Группа доступа: {{accessGroup}}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>

        <v-divider></v-divider>

        <v-list>
          <v-subheader>Общие настройки системы</v-subheader>

          <v-list-item @click="notificationStatus = !notificationStatus" v-ripple="{ class: 'teal--text' }">
            <v-list-item-icon>
              <v-icon>mdi-bell-outline</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Уведомления</v-list-item-title>
              <v-list-item-subtitle>Получение уведомлений</v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-action>
              <v-switch v-model="notificationStatus" disabled color="teal"></v-switch>
            </v-list-item-action>
          </v-list-item>

          <v-list-item @click="tooltipStatus = !tooltipStatus" v-ripple="{ class: 'teal--text' }">
            <v-list-item-icon>
              <v-icon>mdi-help</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Подсказки</v-list-item-title>
              <v-list-item-subtitle>Отображение подсказок</v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-action>
              <v-switch v-model="tooltipStatus" disabled color="teal"></v-switch>
            </v-list-item-action>
          </v-list-item>

          <v-subheader>Действия над системой</v-subheader>
          <notification-list v-slot:default="{on}">
            <v-list-item link v-on="on" v-ripple="{ class: 'teal--text' }">
              <v-list-item-icon><v-icon left>mdi-history</v-icon></v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>История уведомлений</v-list-item-title>
                <v-list-item-subtitle>Список всех ваших уведомлений</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </notification-list>
          <manual-list v-slot:default="{on}">
            <v-list-item link v-on="on" v-ripple="{ class: 'teal--text' }">
              <v-list-item-icon><v-icon left>mdi-file-document-outline</v-icon></v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>Руководство пользователя</v-list-item-title>
                <v-list-item-subtitle>Рекомендации, руководства, методики</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </manual-list>
          <v-list-item v-if="isAdmin || isStaff" href="/admin/" link v-ripple="{ class: 'teal--text' }">
            <v-list-item-icon><v-icon left>mdi-account-cog-outline</v-icon></v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Сайт администратора</v-list-item-title>
              <v-list-item-subtitle>Открыть страницу администрирования</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item @click="logOutUser" link v-ripple="{ class: 'teal--text' }">
            <v-list-item-icon><v-icon left>mdi-logout</v-icon></v-list-item-icon>
            <v-list-item-title>Выйти из системы</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-card>
    </v-menu>
  </v-app-bar>
</template>

<script>
import NotificationList from "@/components/WebsiteShell/UIMainComponents/NotificationList"
import { mapActions, mapGetters } from 'vuex'
import router from "@/router"
import ManualList from "@/components/WebsiteShell/UIMainComponents/ManualList";

export default {
  name: 'appBar',
  components: {ManualList, NotificationList},
  data: () => ({
    status: {
      admin: 'Администратор',
      staff: 'Модератор'
    },
  }),
  computed: {
    ...mapGetters([
      'appbarTabs',
      'baseList',
      'navigationDrawerStatus',
      'userInformation',
      'globalTooltipStatus',
      'globalNotificationStatus',
    ]),
    tooltipStatus: {
      get: function () { return this.globalTooltipStatus },
      set: function (value) { this.setGlobalTooltipStatus(value) }
    },
    notificationStatus: {
      get: function () { return this.globalNotificationStatus },
      set: function (value) { this.setGlobalNotificationStatus(value) }
    },
    drawer: {
      get: function () { return this.navigationDrawerStatus(router.currentRoute.name) },
      set: function (val) { this.setNavigationDrawerStatus(val) }
    },
    accessGroup: function () {
      const group = this.userInformation.group_id
      return this.baseList(group.list_id).values.find(v => v.id === group.id).value
    },
    isAdmin: function () { return this.userInformation.admin },
    isStaff: function () { return this.userInformation.staff },
    staffStatus: function () {
      let result = []
      if(this.isAdmin) result.push(this.status.admin)
      if(this.isStaff) result.push(this.status.staff)
      return result.join(', ')
    },
  },
  methods: mapActions([
    'logOutUser',
    'setNavigationDrawerStatus',
    'setGlobalTooltipStatus',
    'setGlobalNotificationStatus'
  ]),
}
</script>

<style scoped>
</style>
