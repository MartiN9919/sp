<template>
    <v-alert
    :color="status"
    @click="$emit('removeAlert', alert)"
    :icon="this.icon"
    border="left" dark
    style="cursor: default"
    elevation="20"
    >
      <v-row no-gutters class="noselect">
        <h3 v-if="[404].indexOf(alert.status) !== -1">
          Ошибка получения данных
        </h3>
        <div class="title"  v-else-if="[500].indexOf(alert.status) !== -1">
          Неизвестная ошибка сервера
        </div>
        <v-col v-else-if="[501, 502, 503].indexOf(alert.status) !== -1">
          <v-row no-gutters>
            <v-col class="d-flex justify-start" >{{alert.date_time}} <br> </v-col>
            <v-col class="d-flex justify-end "><p class="font-weight-thin mb-0" style="font-size: 12px">Отправитель {{alert.from}}</p></v-col>
          </v-row>

          <v-divider dark></v-divider>

          <div>Сообщение - {{alert.content}}</div>

        </v-col>
        <div v-else>
          {{alert.data.status}}
        </div>
      </v-row>
    </v-alert>
</template>

<script>
import '@/assets/css/noselect.css'

export default {
  name: 'alert',
  data: () => ({
    alertType: {
      '501': 'green darken-1',
      '502': 'blue darken-1',
      '503': 'purple darken-1'
    }
  }),
  props: {
    alert: Object
  },
  computed: {
    status: function () { return this.alert.status in this.alertType ? this.alertType[this.alert.status] : 'red darken-1' },
    icon: function () {
      if (this.status === 'red darken-1') return 'mdi-alert-rhombus-outline'
      if (this.status === 'green darken-1') {
        if (this.alert.file) return 'mdi-file-download-outline'
        else return 'mdi-check'
      }
      if (this.status === 'blue darken-1') return 'mdi-alert-circle-outline'
      if (this.status === 'purple darken-1') return 'mdi-alert-rhombus-outline'
    }
  },
  created () {
    if (this.status === 'red darken-1') setTimeout(() => { this.$emit('removeAlert', this.alert) }, 5000)
  }
}
</script>

<style scoped>

</style>
