<template>
  <v-col class="notifications-list pa-0">
    <v-slide-x-reverse-transition group>
      <v-alert
        v-for="notification in notifications" :key="notification.id"
        @click="setReadNotification({notification})"
        :color="notificationType(notification).color"
        max-width="400" max-height="200" border="left" dark class="ma-2 notification"
      >
        <template v-slot:prepend>
          <div class="d-flex flex-column pr-2">
            <v-icon>{{notificationType(notification).icon}}</v-icon>
            <div v-if="!notificationType(notification)" class="text-subtitle-2">{{notification.status}}</div>
          </div>
        </template>
        <div class="type">{{notificationType(notification).text}}</div>
        <div class="font-italic time">{{notification.time}}</div>
        <v-divider class="my-1"></v-divider>
        <div class="text-body-2 content">{{notification.content}}</div>
      </v-alert>
    </v-slide-x-reverse-transition>
  </v-col>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'alertsList',
  computed: mapGetters(['notifications', 'notificationType']),
  methods: mapActions(['setReadNotification']),
}
</script>

<style scoped>
  ::-webkit-scrollbar {
    width: 0;
  }
  .notifications-list {
    position: absolute;
    z-index: 100002;
    bottom: 0;
    max-width: 25em;
    max-height: 50%;
    overflow-y: auto;
    overflow-x: hidden;
    right: 0;
  }
  .notifications-list >>> .v-alert__content {
    border-left: 1px solid rgba(255, 255, 255, 0.1);
    padding-left: 0.9em;
  }
  .notification {
    cursor: pointer;
  }
  .content {
    word-break: break-all;
    max-height: 110px;
    overflow-y: auto;
  }
  .type {
    line-height: 1em
  }
  .time {
    font-size: 0.8em
  }
</style>
