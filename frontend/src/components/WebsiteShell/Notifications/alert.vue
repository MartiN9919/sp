<template>
    <v-alert
      :color="status"
      @click="$emit('removeAlert', alert)"
      :icon="this.icon"
      border="left" dark
      style="cursor: default;"
      elevation="20"
    >
      <v-row no-gutters class="noselect">
        <div v-if="alert.status in alertText">
          <div class="text-uppercase">Ошибка выполнения запроса</div>
          <v-divider light></v-divider>
          <div>{{alertText[alert.status]}}</div>
        </div>
        <v-col v-else-if="[501, 502, 503].indexOf(alert.status) !== -1">
          <v-row v-if="(alert.date_time || alert.from)" no-gutters>
            <v-col v-if="alert.date_time" class="d-flex justify-start" >{{alert.date_time}}<br></v-col>
            <v-col v-if="alert.from"      class="d-flex justify-end "><p class="font-weight-thin mb-0" style="font-size: 12px">Отправитель {{alert.from}}</p></v-col>
          </v-row>

          <v-divider dark v-if="(alert.date_time || alert.from)"></v-divider>

          <div>{{alert.content}}</div>

        </v-col>
      </v-row>
    </v-alert>
</template>

<script>
import '@/assets/css/noselect.css'

export default {
  name: 'alert',
  data: () => ({
    alertText: {
      400: 'Запрос не был выполнен из-за некоректно предоставленных данных',
      401: 'Запрос не был выполнен из-за ошибки подтверждения персональных данных',
      403: 'Вы не обладаете правами, для выполнения данного запроса',
      404: 'По вашему запросу ничего не было найдено. Возможно ресурс был удален',
      405: 'Некорректный запрос',
      408: 'Истекло время ожидания ответа от сервера',
      452: 'Неверный формат номера телефона',
      470: 'Ошибка выполнения пользовательского сценария',
      480: 'Некорректный тип запроса',
      496: 'Ошибка базы данных(чтение)',
      497: 'Ошибка базы данных(запись)',
      498: 'Неизвестная ошибка  Сапфира',
      500: 'Произошла внутренняя ошибка сервера',
      'no connect': 'Нет соединения с сервером. Проверьте ваше соединение с сетью, либо подождите некоторое время.'
    },
    alertType: {
      501: 'green darken-1',
      502: 'blue darken-1',
      503: 'purple darken-1',
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
    if (this.alert.show_time)      setTimeout(() => { this.$emit('removeAlert', this.alert) }, this.alert.show_time*1000)
  }
}
</script>

<style scoped>

</style>
