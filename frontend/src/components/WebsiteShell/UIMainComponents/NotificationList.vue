<template>
  <v-dialog v-model="dialog" scrollable width="60%" content-class="overflow-hidden align-self-start">
    <template v-slot:activator="{ on, attrs }">
      <slot :on="on"></slot>
    </template>
    <v-data-table
        v-if="dialog"
        :headers="headers"
        :items="desserts"
        :options.sync="options"
        :server-items-length="totalDesserts"
        :loading="loading"
        :footer-props="footer"
        must-sort
        fixed-header
        no-data-text=""
        height="calc(100% - 59px)"
        class="elevation-1"
    >
      <template v-slot:header.date_time="{ header }">
        <drop-down-menu max-width="20%" offset-y left close-on-click :close-on-content-click="false" z-index="100008">
          <template v-slot:activator="{ on }">
            <span v-on="on" style="cursor: pointer; white-space: nowrap;">
              {{header.text}}
            </span>
          </template>
          <template v-slot:body="{ closeMenu,  status }">
            <select-date v-if="status" v-model="extraOptions.groupDate" :close-menu="closeMenu"></select-date>
          </template>
        </drop-down-menu>
        <v-icon v-if="!!extraOptions.groupDate" @click.stop="extraOptions.groupDate = ''" size="20" color="red">
          mdi-close
        </v-icon>
      </template>
      <template v-slot:header.status="{ header }">
        <v-menu close-on-content-click>
          <template v-slot:activator="{ on }">
            <span v-on="on" style="cursor: pointer; white-space: nowrap;">
              {{header.text}}
            </span>
          </template>
          <v-list>
            <v-list-item-group v-model="extraOptions.groupStatus" color="teal">
              <v-list-item value="information">
                <v-list-item-content>
                  <v-list-item-title>Информация</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-list-item value="warning">
                <v-list-item-content>
                  <v-list-item-title>Предупреждение</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-list-item value="error">
                <v-list-item-content>
                  <v-list-item-title>Ошибка</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-menu>
        <v-icon v-if="!!extraOptions.groupStatus" @click="extraOptions.groupStatus=''" size="20" color="red">
          mdi-close
        </v-icon>
      </template>
      <template v-slot:item.status="{ item }">
        <v-chip :color="notificationType(item).color" dark>
          <v-icon left>{{notificationType(item).icon}}</v-icon>{{ notificationType(item).text }}
        </v-chip>
      </template>
      <template v-slot:item.content="{ item }">
        <div style="user-select: text; cursor: text; color: rgba(0, 0, 0, 0.87); word-wrap: anywhere" class="my-1">
          {{item.content}}
        </div>
      </template>
      <template v-slot:item.date_time="{ item }">
        <span style="white-space: nowrap">{{item.date_time}}</span>
      </template>
      <template v-slot:footer.page-text="items">
        {{ items.pageStart }} - {{ items.pageStop }} из {{ items.itemsLength }}
      </template>
    </v-data-table>
  </v-dialog>
</template>

<script>
import DropDownMenu from "@/components/WebsiteShell/CustomComponents/dropDownMenu"
import SelectDate from "@/components/WebsiteShell/CustomComponents/DateTimePickers/selectDate"
import {mapGetters, mapActions} from "vuex"

export default {
  name: "NotificationList",
  components: {SelectDate, DropDownMenu},
  data: () => ({
    headers: [
      {text: 'Тип уведомления', align: 'start', sortable: false, value: 'status',},
      {text: 'Отправитель', value: 'from', sortable: false},
      {text: 'Сообщение', value: 'content', sortable: false},
      {text: 'Время', value: 'date_time', align: 'end', sortable: true},
    ],
    footer: {
      showFirstLastPage: true,
      showCurrentPage: true,
      'items-per-page-options': [5, 10, 15],
      'items-per-page-text':'Количество на странице',
    },
    dialog: false,
    desserts: [],
    options: {
      sortBy: ['date_time'],
      sortDesc: [true]
    },
    extraOptions: {
      groupStatus: '',
      groupDate: '',
    },
    totalDesserts: 0,
    loading: true,
  }),
  computed: mapGetters(['notificationType']),
  methods: {
    ...mapActions(['getNotificationList']),
    getDataFromApi () {
      this.loading = true
      let params = {size: this.options.itemsPerPage, offset: this.options.page}
      if (!!this.options.sortDesc)
        Object.assign(params, {order: this.options.sortDesc[0] ? 'up' : 'down'})
      if (!!this.extraOptions.groupStatus)
        Object.assign(params, {type: this.extraOptions.groupStatus})
      if (!!this.extraOptions.groupDate)
        Object.assign(params, {date: this.extraOptions.groupDate})
      this.getNotificationList(params).then(response => {
        this.desserts = response.data.list
        this.totalDesserts = response.data.total
        this.loading = false
      })
    },
  },
  watch: {
    options: {
      deep: true,
      handler () {
        this.getDataFromApi()
      }
    },
    extraOptions: {
      deep: true,
      handler () {
        this.getDataFromApi()
      }
    }
  },
}
</script>

<style scoped>
>>> .v-dialog__content {
  align-items: start;
}
</style>