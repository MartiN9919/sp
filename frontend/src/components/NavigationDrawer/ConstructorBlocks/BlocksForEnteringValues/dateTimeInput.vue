<template>
  <v-text-field
    v-model="variable.value"
    :label="variable.title"
    placeholder="Выберете необходимую дату значение"
    hide-details readonly class="pt-0 mt-0" color="teal" type="text"
  >
    <template v-slot:append>
      <v-menu offset-x z-index="10001" left :close-on-content-click="false" transition="slide-x-reverse-transition">
        <template v-slot:activator="{ on, attrs }">
          <v-icon
            v-bind="attrs" v-on="on"
            :color="attrs['aria-expanded'] === 'true' ? 'teal' : ''"
          >mdi-timetable</v-icon>
        </template>
        <v-container fluid>
          <v-row no-gutters>
            <v-col>
              <v-card>
                <v-date-picker
                  no-title
                  v-model="variable.value"
                  show-adjacent-months
                  first-day-of-week="1"
                  color="teal" locale="ru"
                  style="border-radius: 0"
                ></v-date-picker>
              </v-card>
            </v-col>
            <v-divider vertical></v-divider>
            <v-col>
              <v-row no-gutters>
                <v-virtual-scroll
                  :items="items"
                  item-height="40"
                  width="50"
                  height="300"
                >
                  <template v-slot:default="{ item }">
                    <v-list-item :key="item" link>
                      {{item}}
                    </v-list-item>
                  </template>
                </v-virtual-scroll>
                <v-virtual-scroll
                  :items="items"
                  item-height="40"
                  width="50"
                  height="300"
                >
                  <template v-slot:default="{ item }">
                    <v-list-item :key="item" light>
                      {{item}}
                    </v-list-item>
                  </template>
                </v-virtual-scroll>
              </v-row>
            </v-col>
          </v-row>
        </v-container>
      </v-menu>
    </template>
  </v-text-field>
</template>

<script>
export default {
  name: "dateTimeInput",
  data: () => ({
    datePicker: true,
  }),
  props: {
    variable: Object,
  },
  computed: {
    items () {
      return Array.from({ length: this.length }, (k, v) => v + 1)
    },
    length () {
      return 7000
    },
  },
}
</script>

<style scoped>

</style>