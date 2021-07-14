<template>
  <v-dialog
    v-model="dialog"
    @input="show_dialog"
    persistent
  >
    <template v-slot:activator="{ on, attrs }">
      <v-textarea
        row-height="1" auto-grow
        autocomplete="off"
        append-icon="mdi-map-marker-outline"
        :label="title"
        :rules="rules"
        v-model="value"
        placeholder="Выберете объект на карте"
        hide-details color="teal" readonly class="pt-0 mt-0" type="text"
        v-on="on"
      ></v-textarea>
    </template>
    <v-card>

      <LeafletEditor
        v-if="dialog"
        v-model="fc"
        :options="edit_options()"
      />

      <v-divider></v-divider>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="teal" text @click="click_cancel">Отменить</v-btn>
        <v-btn color="teal" text @click="click_ok">Подтвердить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import LeafletEditor from '@/components/Map/Leaflet/LeafletEditor';

export default {
  name: "geometryInput",
  components: { LeafletEditor, },
  props: {
    rules: Array,
    title: String,
    inputString: Object,
  },
  model: { prop: 'inputString', event: 'changeInputString', },
  data: () => ({
    dialog: false,
    fc_temp: undefined,
  }),
  mounted: function() {
    this.value = {
          "type": "FeatureCollection",
          "features": [
            {
              "type": "Feature",
              "properties": {
                "hint": "Edit 1",
              },
              "geometry": {
                "type": "Polygon",
                "coordinates": [
                  [
                    [30.212402343750004,55.19141243527065],
                    [30.443115234375004,54.50832650029076],
                    [31.014404296875004,54.718275018302315],
                    [30.212402343750004,55.19141243527065],
                  ]
                ]
              }
            },
            {
              "type": "Feature",
              "properties": {
                "hint": "Edit 2",
              },
              "geometry": {
                "type":        "Point",
                "coordinates": [24.071044921875004,55.86914706303444]
              },
            },
          ],
        }
  },
  computed: {
    value: {
      get: function () { return this.inputString },
      set: function (value) { this.$emit('changeInputString', value) }
    },
    fc: {
      get() {
        return this.value;
      },
      set(val) {
        console.log(888, val)
        this.fc_temp = val;
      },
    },
  },

  methods: {
    show_dialog (e) {
       if (this.value == undefined) this.value = { "type": "FeatureCollection", "features": [], }
       this.fc = JSON.parse(JSON.stringify(this.value));
    },

    click_ok() {
      this.dialog = false;
      this.value = JSON.parse(JSON.stringify(this.fc_temp));
    },

    click_cancel() {
      this.dialog = false;
      //this.fc     = JSON.parse(JSON.stringify(this.value));
    },

    // задавать не обязательно
    edit_options() {
      return {
        mode_enabled: {
          marker:  true,
          line:    true,
          polygon: true,
        },
        mode_selected: 'Polygon',
      }
    },

  },

}
</script>

<style scoped>

</style>