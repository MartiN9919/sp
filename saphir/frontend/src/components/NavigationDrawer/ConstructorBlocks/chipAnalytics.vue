<template>
  <v-tooltip bottom transition="false"  style="z-index: 10001">
    <template v-slot:activator="{ on, attrs }">
      <v-chip
        @click:close="$emit('deleteActiveAnalytics', analytics)"
        @click="$emit('returnSelectAnalytics', analytics)"
        :class="{'pulse': selectedTreeViewItem === analytics}"
        :style="pulseAnimation"
        class="ma-1"
        :color=color
        v-bind="attrs"
        v-on="on"
        close
        dark
      >

        <p style="overflow: hidden; text-overflow: ellipsis; max-width: 100%; margin-bottom: 0">{{ analytics.name }}</p>

        <!-- объект меню, содержищий палитру, для выбора цвета -->
        <v-menu v-if="'result' in analytics" offset-y :close-on-content-click=false style="z-index: 10001">

          <template v-slot:activator="{ on, attrs }">
            <v-icon right v-bind="attrs" v-on="on">mdi-brush</v-icon>
          </template>

          <v-list>
            <v-list-item>
              <v-list-item-title>
                <v-color-picker class="ma-2" v-model="color" hide-inputs></v-color-picker>
              </v-list-item-title>
            </v-list-item>
          </v-list>

        </v-menu>

      </v-chip>
    </template>
    <div>Введенные значения:</div>
    <div v-for="variable in analytics.variables">&ndash; {{variable.title}}: {{variable.value}}</div>
  </v-tooltip>
</template>

<script>
export default {
  name: 'chipAnalytics',
  props: {
    analytics: Object,
    selectedTreeViewItem: Object
  },
  computed: {
    color: {
      get: function () { return this.analytics.color },
      set: function (color) { this.$emit('changeColor', { analytics: this.analytics, color: color }) }
    },
    pulseAnimation () {
      return { '--selected-analytics-color': this.selectedTreeViewItem.color }
    }

  }
}
</script>

<style scoped>
.pulse {
  animation: pulse-animation 1s infinite;
}

@keyframes pulse-animation {
  0% {
    box-shadow: 0 0 0 0px var(--selected-analytics-color);
  }
  100% {
    box-shadow: 0 0 0 10px rgba(255, 0, 0, 0);
  }
}

</style>
