<template>
  <custom-tooltip bottom>
    <template v-slot:activator="{ on }">
      <v-chip
        @click:close="$emit('deleteActiveAnalytics', analytics)"
        @click="$emit('returnSelectAnalytics', analytics)"
        :class="{'pulse': selectedTreeViewItem === analytics}"
        :color=color :style="pulseAnimation" close
        outlined v-on="on" class="ma-1"
      >
        <p class="text-formatter-for-window-size font-for-color-background mb-0">{{ analytics.name }}</p>
        <custom-color-picker v-if="analytics.hasOwnProperty('fc')" v-model="color"></custom-color-picker>
      </v-chip>
    </template>
    <template v-slot:body>
      <div class="ma-2">
        <table>
          <tr>
            <th>Название переменной</th>
            <th>Введенное значение</th>
          </tr>
          <tr v-for="variable in analytics.variables">
            <td>{{variable.title}}</td>
            <td>{{ getValue(variable) }}</td>
          </tr>
        </table>
        <v-divider dark class="py-1"></v-divider>
        <p v-if="analytics.hint"
           class="text-formatter-for-window-size additional-text text-justify ma-0"
        >{{analytics.hint}}</p>
      </div>
    </template>
  </custom-tooltip>
</template>

<script>
import CustomTooltip from "@/components/WebsiteShell/CustomComponents/customTooltip"
import CustomColorPicker from "@/components/WebsiteShell/CustomComponents/customColorPicker"
import {mapGetters} from "vuex"

export default {
  name: 'chipAnalytics',
  components: {CustomColorPicker, CustomTooltip},
  props: {
    analytics: Object,
    selectedTreeViewItem: Object
  },
  computed: {
    ...mapGetters(['baseLists']),
    pulseAnimation: function () {
      return { '--selected-analytics-color': this.selectedTreeViewItem.color }
    },
    color: {
      get: function () { return this.analytics.color },
      set: function (color) { this.$emit('changeColor', { analytics: this.analytics, color: color }) }
    },
  },
  methods: {
    getValue(variable) {
      switch (variable.type.title) {
        case 'list':
          let value
          for (const [listId, list] of Object.entries(this.baseLists)) {
            value = list.values.find(item => item.id === variable.value)
            if (value) return value.value
          }
          return value
        case 'checkbox':
          return variable.value ? 'ДА' : 'НЕТ'
        case 'geometry':
          return variable.value ? variable.type.value === 'polygon' ? 'Геометрия' : 'Точка' : ''
        case 'search':
          return variable.value ? variable.value.title : ''
        default:
          if(variable.type.title.startsWith('file'))
            return variable.value ? variable.value.file.name : ''
          else return variable.value
      }
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
