<template>
  <v-col>
    <v-text-field
      autocomplete="off"
      v-model="searchInput"
      v-on:keyup.enter="findObject"
      @click="showList = true"
      placeholder="Выберете необходимое значение"
      hide-details class="pt-0 mt-0" color="teal" type="text"
    >
      <template slot="append-outer">
        <v-btn icon @click="showList = !showList">
          <v-icon :color="showList ? 'teal' : ''">mdi-menu-down-outline</v-icon>
        </v-btn>
      </template>
    </v-text-field>
    <v-scroll-y-transition v-if="showList">
      <v-card elevation="5">
        <v-list class="py-0 overflow-y-auto" max-height="88%">
          <v-btn
              :disabled="!searchInput.length || this.searchInput === this.pastSearchInput"
              @click.stop="findObject" color="teal" width="100%" outlined tile
          >Искать в базе данных</v-btn>
          <v-btn outlined tile color="teal" width="100%">Создать новый объект</v-btn>
          <v-divider v-if="searchInput && this.searchInput !== this.pastSearchInput"></v-divider>
          <v-list-item v-for="(item, key) in items" :key="key">
            <v-list-item-title>
              {{item}}
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-card>
    </v-scroll-y-transition>
  </v-col>
</template>

<script>
export default {
  name: "searchList",
  data: () => ({
    items: [],
    showList: false,
    searchInput: '',
    pastSearchInput: '',
  }),
  props: {
    variable: Object,
  },
  methods: {
    findObject() {
      if (this.searchInput && this.searchInput !== this.pastSearchInput) {
        this.pastSearchInput = this.searchInput
        this.items = ['Programming', 'Design', 'Vue', 'Vuetify','Design', 'Vue', ]
      }
    }
  }
}
</script>

<style scoped>
.text-formatter-for-window-size {
  overflow: hidden;
  text-overflow: ellipsis;
}

</style>