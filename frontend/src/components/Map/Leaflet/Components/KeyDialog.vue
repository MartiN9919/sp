<template>
  <v-dialog
    v-model="dialog"
    width="400px"
    height="100px"
    style="z-index: 99999999"
    persistent
    @keydown.enter="click_ok"
    @keydown.esc="dialog = false"
  >
    <v-card>
      <v-card-title class="text-h7">Сохранить фрагмент в слот {{ ind }}</v-card-title>
      <v-card-text>
        <v-text-field
          v-model="val"
          :label="'Название слота '+ind"
          :color="$CONST.APP.COLOR_OBJ"
          hide-details
          outlined
          clearable
          dense
          autofocus
          @keydown.esc="dialog = false"
        />
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn :color="$CONST.APP.COLOR_OBJ" text @click="click_cancel">Отмена</v-btn>
        <v-btn :color="$CONST.APP.COLOR_OBJ" text @click="click_ok">Ок</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>

export default {
  name: "KeyDialog",

  data: () => ({
    dialog: false,
    ind:    undefined,
    val:    undefined,
  }),

  methods: {
    exec(ind, val) {
      this.ind    = ind;
      this.val    = val;
      this.dialog = true;
    },

    click_ok() {
      this.dialog = false;
      this.$emit('ok', this.ind, this.val);
    },

    click_cancel() {
      this.dialog = false;
    },

  },

}

</script>
