<template>
  <v-card @click="$emit('removeAlert', alert)" :color="status" max-height="400" dark hover class="ma-2" style="background-clip: content-box" :style="{borderLeft: `10px solid ${status}B3 !important`}">
    <v-row no-gutters class="px-4 pt-2">
      <v-col cols="1" class="my-auto mr-4">
        <v-icon>{{this.icon}}</v-icon>
      </v-col>
      <v-col>
        <div style="font: bold 1em sans-serif; color: white">Отправитель: {{alert.from || 'Система'}}</div>
        <div style="color: rgba(255, 255, 255, 0.7); font-size: 0.9em">{{alert.date_time || `Статус ошибки: ${alert.status}`}}</div>
      </v-col>
    </v-row>
    <v-divider dark></v-divider>
    <v-card-text style="word-break: break-all; max-height: 298px;" class="overflow-y-auto pt-0">
      {{alert.content || alertText[alert.status]}}
    </v-card-text>
  </v-card>

<!--    <v-alert-->
<!--      :color="status"-->
<!--      @click="$emit('removeAlert', alert)"-->
<!--      :icon="this.icon"-->
<!--      border="left" dark-->
<!--      elevation="20" class="ma-0"-->
<!--    >-->
<!--&lt;!&ndash;      <div class="overflow-y-auto" style="max-height: 350px">{{alert}}</div>&ndash;&gt;-->
<!--      <v-divider dark></v-divider>-->
<!--      <div class="text-end">{{alert.date_time}}</div>-->
<!--      <v-row no-gutters class="noselect">-->
<!--        <div v-if="alert.status in alertText">-->
<!--          <div class="text-uppercase">Ошибка выполнения запроса</div>-->
<!--          <v-divider light></v-divider>-->
<!--          <div>{{alertText[alert.status]}}</div>-->
<!--        </div>-->
<!--        <v-col v-else-if="[501, 502, 503, 504].indexOf(alert.status) !== -1">-->
<!--          <v-row v-if="(alert.date_time || alert.from)" no-gutters>-->
<!--            <v-col v-if="alert.date_time" class="d-flex justify-start" >{{alert.date_time}}<br></v-col>-->
<!--            <v-col v-if="alert.from"      class="d-flex justify-end "><p class="font-weight-thin mb-0" style="font-size: 12px">Отправитель {{alert.from}}</p></v-col>-->
<!--          </v-row>-->

<!--          <v-divider dark v-if="(alert.date_time || alert.from)"></v-divider>-->

<!--          <div>{{alert.content}}</div>-->

<!--        </v-col>-->
<!--      </v-row>-->
<!--    </v-alert>-->
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
      453: 'Нет прав на добавление/изменение геометрии',
      454: 'Нет прав на добавление/изменение данных',
      470: 'Ошибка выполнения пользовательского сценария',
      480: 'Некорректный тип запроса',
      496: 'Ошибка базы данных(чтение)',
      497: 'Ошибка базы данных(запись)',
      498: 'Неизвестная ошибка  Сапфира',
      500: 'Произошла внутренняя ошибка сервера',
      'no connect': 'Нет соединения с сервером. Проверьте ваше соединение с сетью, либо подождите некоторое время.'
    },
    alertType: {
      501: '#43A047',
      502: '#039BE5',
      503: '#8E24AA',
      504: '#D32F2F',
    }
  }),
  props: {
    alert: Object
  },
  computed: {
    status: function () { return this.alert.status in this.alertType ? this.alertType[this.alert.status] : '#D32F2F' },
    icon: function () {
      if (this.status === '#D32F2F') return 'mdi-alert-rhombus-outline'
      if (this.status === '#43A047') {
        if (this.alert.file) return 'mdi-file-download-outline'
        else return 'mdi-check'
      }
      if (this.status === '#039BE5') return 'mdi-alert-circle-outline'
      if (this.status === '#8E24AA') return 'mdi-alert-rhombus-outline'
    }
  },
  created () {
    if (this.alert.show_time) {
      setTimeout(() => { this.$emit('removeAlert', this.alert) }, this.alert.show_time*1000);
      return;
    }
    if (this.status === '#D32F2F') setTimeout(() => { this.$emit('removeAlert', this.alert) }, 5000)
  }
}
</script>

<style scoped>
::-webkit-scrollbar {
  width: 0;
}
</style>
