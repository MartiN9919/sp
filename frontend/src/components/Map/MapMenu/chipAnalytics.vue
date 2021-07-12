<template>
  <v-tooltip bottom transition="false" color="#00796B" z-index="10001" max-width="20%">
    <template v-slot:activator="{ on }">
      <v-chip
        @click:close="$emit('deleteActiveAnalytics', analytics)"
        @click="$emit('returnSelectAnalytics', analytics)"
        :class="{'pulse': selectedTreeViewItem === analytics}"
        :color=color :style="pulseAnimation" close
        outlined class="ma-1" v-on="on"
      >
        <p class="text-formatter-for-window-size font-for-color-background mb-0">{{ analytics.name }}</p>
        <!-- объект меню, содержищий палитру, для выбора цвета -->
        <v-menu v-if="'fc' in analytics" offset-y :close-on-content-click=false z-index="10001">
          <template v-slot:activator="{ on }">
            <v-icon right v-on="on">mdi-brush</v-icon>
          </template>
          <v-color-picker v-model="color" hide-inputs></v-color-picker>
        </v-menu>
      </v-chip>
    </template>
    <div class="my-2">
      <table>
        <tr>
          <th>Название переменной</th>
          <th>Введенное значение</th>
        </tr>
        <tr v-for="variable in analytics.variables">
          <td>{{variable.title}}</td>
          <td v-if="typeof variable.value !== 'object'">{{variable.value}}</td>
          <td v-else><span v-for="(value) in variable.value">{{value}} </span></td>
        </tr>
      </table>
      <v-divider dark class="py-1"></v-divider>
      <p v-if="analytics.hint"
         class="text-formatter-for-window-size additional-text text-justify ma-0"
      >{{analytics.hint}}</p>
    </div>
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
    pulseAnimation () { return { '--selected-analytics-color': this.selectedTreeViewItem.color } },
    color: {
      get: function () { return this.analytics.color },
      set: function (color) { this.$emit('changeColor', { analytics: this.analytics, color: color }) }
    },
  }
}
</script>

<style scoped>
table {
  border-collapse: collapse;
  table-layout: fixed;
  font-size: 0.80em;
  color: white;
  width: 100%;
}

th {
  text-align: center;
}

td, th {
  border: 1px solid white;
  padding-left: 5px;
  padding-right: 5px;
  padding-top: 2px;
  padding-bottom: 2px;
  white-space: nowrap;
}

.text-formatter-for-window-size, td, th {
  overflow: hidden;
  text-overflow: ellipsis;
}

.font-for-color-background {
  color: black;
}

.additional-text {
  font-weight: lighter;
  line-height: 1.25em;
  font-size: 0.9em;
  color: #CFD8DC;
}

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
