<template>
  <v-dialog v-model="dialog" width="60%" scrollable content-class="overflow-hidden">
    <template v-slot:activator="{ on, attrs }">
      <slot :on="on"></slot>
    </template>
    <v-card>
      <v-card-title>
        Руководство пользователя
      </v-card-title>
      <v-card-subtitle>
        Рекомендации, руководства, методики
      </v-card-subtitle>
      <v-divider/>
      <v-card-text>
        <v-data-table
            disable-pagination
            hide-default-footer
            :headers="headers"
            :items="desserts"
            item-key="id"
            no-data-text="Инструкции отсутствуют"
        >
          <template v-slot:item.download="{ item }">
            <a tabindex="-1" :href="download(item)">
              <v-icon small color="teal">mdi-download</v-icon>
            </a>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import {getDownloadManualLink} from "@/plugins/axiosSettings"
import {mapActions} from "vuex";

export default {
  name: "ManualList",
  data: () => ({
    dialog: false,
    desserts: [],
    headers: [
      {text: 'Название', value: 'title', align: 'start', sortable: true,},
      {text: 'Дата изменения', value: 'update', sortable: true, align: 'center'},
      {text: 'Скачать', value: 'download', sortable: false, align: 'end'},
    ],
  }),
  methods: {
    ...mapActions(['getManuals']),
    download(item) {
      return getDownloadManualLink(item.id)
    }
  },
  mounted() {
    this.getManuals().then(response => {
      this.desserts = response.data
    })
  }
}
</script>

<style scoped>
>>> .v-dialog {
  max-height: 60% !important;
}
.manual-table {
  max-height: calc(100% - 80px);
}
</style>