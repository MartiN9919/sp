<template>
  <v-container>
    <v-card elevation="15" height="auto" class="overflow-y-auto">
      <v-data-table
        :items-per-page='15'
        :headers="headers"
        :items="listFiles"
        :search="search"
        :footer-props="{
          showFirstLastPage: true,
          showCurrentPage: true,
          'items-per-page-options': [5, 10, 15],
          'items-per-page-text':'Количество отчетов на странице',
        }"
      >
        <template v-slot:top>
          <v-spacer></v-spacer>
          <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="Поиск"
              single-line
              hide-details
              color="teal"
              class="mx-4"
          ></v-text-field>
        </template>
        <template v-slot:item="{ item }">
          <tr @click="changeSelectedReport(item)" :style="selectedReportStyle(item)" style="cursor: pointer">
            <td class="text-center">{{ item.name }}</td>
            <td class="text-center">
              <div v-for="variable in item.params.variables">{{ variable.title }}: {{ variable.value }}</div>
            </td>
            <td class="text-center">{{ item.date }}</td>
            <td class="text-center">
              <v-hover v-slot="{ hover }" v-if="item.status === 'in_progress'">
                <v-btn icon v-if="hover">
                  <v-icon>mdi-close</v-icon>
                </v-btn>
                <v-progress-circular v-else indeterminate color="teal" width="2" size="20"></v-progress-circular>
              </v-hover>

              <v-hover v-slot="{ hover }" v-if="item.status === 'error'">
                <v-btn icon v-if="hover">
                  <v-icon color="black">mdi-delete-outline</v-icon>
                </v-btn>
                <v-icon v-else color="red">mdi-file-cancel-outline</v-icon>
              </v-hover>
              <v-hover v-slot="{ hover }" v-if="item.status === 'done'">
                <v-btn icon v-if="hover" @click.stop="downloadFile(item.id)">
                  <v-icon v-if="hover" color="blue">mdi-cloud-download-outline</v-icon>
                </v-btn>
                <v-icon v-else color="green">mdi-file-check-outline</v-icon>
              </v-hover>
            </td>
          </tr>
        </template>
<!--        <template v-slot:footer.page-text="{ pageStart, pageStop, itemsLength }">-->
<!--          {{pageStart}}-{{pageStop}} из {{itemsLength}}-->
<!--        </template>-->
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script>
import {mapActions, mapGetters} from 'vuex'
import router from '@/router'

export default {
  name: 'reportsList',
  data() {
    return {
      search: '',
      headers: [
        {text: 'Название файла', value: 'name', align: 'center'},
        {
          text: 'Параметры, с которыми был вызван скрипт',
          value: 'params',
          filterable: false,
          align: 'center',
          sortable: false
        },
        {text: 'Время удаления', value: 'date', filterable: false, align: 'center'},
        {text: 'Статус отчета', value: 'status', filterable: false, align: 'center'}
      ]
    }
  },
  props: {
    drawer: Boolean,
  },
  computed: {
    ...mapGetters(['listFiles', 'selectedTreeViewItem']),

    selectReport() { return this.selectedTreeViewItem(router.currentRoute.name) },
  },
  methods: {
    ...mapActions(['getListFiles', 'changeSelectedTreeViewItem', 'changeNavigationDrawerStatus', ]),

    downloadFile: (id) => console.log(id),
    changeSelectedReport: function (item) {
      if (!this.drawer) this.changeNavigationDrawerStatus()
      if (this.selectReport && this.selectReport === item.params)
        this.changeSelectedTreeViewItem()
      else this.changeSelectedTreeViewItem(item.params)
    },
    selectedReportStyle(item) {
      if (this.selectReport && this.selectReport === item.params)
        return {color: 'teal', backgroundColor: '#E0F2F1'}
      else return {color: 'black'}
    },
  },
  created() {
    this.getListFiles()
  }
}
</script>

<style scoped>

</style>
