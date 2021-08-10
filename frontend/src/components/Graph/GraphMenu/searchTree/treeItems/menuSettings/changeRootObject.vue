<template>
  <v-card flat>
    <v-card-text class="pa-0">
      <v-list>
        <v-list-item>
          <custom-autocomplete
            v-model="newObject"
            :items="listOfPrimaryObjects"
            :item-text="'title'"
          ></custom-autocomplete>
        </v-list-item>
        <v-list-item>
          <boolean-input v-model="newActual" :title="'Поиск только по актуальным значениям'"></boolean-input>
        </v-list-item>
      </v-list>
    </v-card-text>
    <v-card-actions>
      <v-btn @click="cancel" outlined color="teal" width="40%">Отмена</v-btn>
      <v-spacer></v-spacer>
      <v-btn @click="confirm" outlined color="teal" width="40%">Готово</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import CustomAutocomplete from "../../../../../WebsiteShell/UI/customAutocomplete"
import BooleanInput from "../../../../../WebsiteShell/InputForms/booleanInput"
import {mapActions, mapGetters} from "vuex"

export default {
  name: "changeRootObject",
  components: { CustomAutocomplete, BooleanInput, },
  props: {
    object: Object,
  },
  data: () => ({
    newObject: null,
    newActual: null,
  }),
  computed: {
    ...mapGetters(['primaryObject', 'listOfPrimaryObjects', ]),
  },
  methods: {
    ...mapActions(['setRootSearchTreeGraph', ]),
    confirm() {
      this.$emit('change', { objectId: this.newObject.id, actual: this.newActual })
      this.cancel()
    },
    cancel() {
      this.$emit('cancel')
    },
  },
  mounted() {
    this.newActual = this.object.actual
    this.newObject = this.primaryObject(this.object.object_id)
  },
}
</script>

<style scoped>

</style>