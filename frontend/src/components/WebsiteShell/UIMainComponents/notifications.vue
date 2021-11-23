<template>
  <v-col class="alert-list pa-0">
    <v-slide-x-reverse-transition group>
      <v-alert
        v-for="notification in notifications" :key="notification.id"
        @click="setReadNotification({notification})"
        :color="getColorNotification(notification)"
        max-width="400" max-height="200" border="left" dark class="ma-2" style="cursor: pointer"
      >
        <template v-slot:prepend>
          <div class="d-flex flex-column pr-2">
            <v-icon>{{getIconNotification(notification)}}</v-icon>
            <div v-if="showStatusNumber(notification)" class="text-subtitle-2">{{notification.status}}</div>
          </div>
        </template>
        <div style="line-height: 1em">Отправитель: {{notification.from}}</div>
        <div class="font-italic" style="font-size: 0.8em">{{notification.time}}</div>
        <v-divider class="my-1"></v-divider>
        <div class="text-body-2" style="word-break: break-all; max-height: 110px; overflow-y: auto">
          {{notification.content}}
        </div>
      </v-alert>
    </v-slide-x-reverse-transition>
  </v-col>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'alertsList',
  data: () => ({
    notificationTypes: {
      501: {
        color: '#43A047',
        icon: 'mdi-check'
      },
      502: {
        color: '#039BE5',
        icon: 'mdi-alert-circle-outline'
      },
      503: {
        color: '#8E24AA',
        icon: 'mdi-alert-rhombus-outline'
      },
      default: {
        color: '#D32F2F',
        icon: 'mdi-alert-rhombus-outline'
      },
    }
  }),
  computed: {
    ...mapGetters(['notifications']),
  },
  methods: {
    ...mapActions(['setReadNotification']),
    getTypeNotification(status) {
      return this.notificationTypes[status] || this.notificationTypes.default
    },
    getColorNotification(notification) {
      return this.getTypeNotification(notification.status).color
    },
    getIconNotification(notification) {
      return this.getTypeNotification(notification.status).icon
    },
    showStatusNumber(notification) {
      return !this.notificationTypes[notification.status]
    }
  }
}
</script>

<style scoped>
  ::-webkit-scrollbar {
    width: 0;
  }
  .alert-list {
    position: absolute;
    z-index: 100002;
    bottom: 0;
    max-width: 25em;
    max-height: 50%;
    overflow-y: auto;
    overflow-x: hidden;
    right: 0;
  }
  .alert-list >>> .v-alert__content {
    border-left: 1px solid rgba(255, 255, 255, 0.1);
    padding-left: 0.9em;
  }
</style>
