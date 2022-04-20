<template>
  <v-container class="h-100 d-flex">
    <v-data-table
      :headers="headers"
      :items="reportsSlice"
      :options.sync="options"
      :footer-props="footer"
      :server-items-length="numsTotalReports"
      no-data-text=""
      class="elevation-11"
      height="100%"
      fixed-header
    >
      <template v-slot:item="{ item }">
        <v-hover v-slot="{ hover }">
          <tr @click="changeSelectedReport(item)" :style="selectedReportStyle(item)" style="cursor: pointer">
            <td class="text-center">{{ item.name }}</td>
            <td class="text-center">
              <div v-for="variable in item.params.variables">
                {{ variable.title }}: {{ typeof variable.value === 'object' ? variable.value.title : variable.value }}
              </div>
            </td>
            <td class="text-center">{{ item.date }}</td>
            <td class="text-center">
              <v-progress-circular v-if="item.status === 'in_progress'" indeterminate color="teal" width="2" size="20"/>
              <v-icon v-else-if="item.status === 'error'" color="red">mdi-file-cancel-outline</v-icon>
              <v-btn icon v-else-if="item.status === 'done' && hover" @click.stop="downloadFile(item.id)">
                <v-icon color="blue">mdi-cloud-download-outline</v-icon>
              </v-btn>
              <v-icon v-else color="green">mdi-file-check-outline</v-icon>
            </td>
          </tr>
        </v-hover>
      </template>
      <template v-slot:footer.page-text="{ pageStart, pageStop, itemsLength }">
        {{pageStart}}-{{pageStop}} из {{itemsLength}}
      </template>
    </v-data-table>
  </v-container>
</template>

<script>
import {getDownloadReportLink} from "@/plugins/axiosSettings"
import {mapActions, mapGetters} from 'vuex'
import router from '@/router'

export default {
  name: 'reportsList',
  data: () => ({
    headers: [
      {
        text: 'Название файла',
        value: 'name',
        align: 'center',
        sortable: false
      },
      {
        text: 'Параметры, с которыми был вызван скрипт',
        value: 'params',
        align: 'center',
        sortable: false
      },
      {
        text: 'Время создания',
        value: 'date',
        align: 'center',
        sortable: false
      },
      {
        text: 'Статус отчета',
        value: 'status',
        align: 'center',
        sortable: false
      }
    ],
    footer: {
      showFirstLastPage: true,
      showCurrentPage: true,
      'items-per-page-options': [5, 10, 15],
      'items-per-page-text':'Количество на странице',
    },
  }),
  computed: {
    ...mapGetters(['reportsSlice', 'selectedTreeViewItem', 'reportTableOptions', 'numsTotalReports', 'inProgressFiles']),
    selectReport() { return this.selectedTreeViewItem(router.currentRoute.name) },
    options: {
      get: function () { return this.reportTableOptions },
      set: function (value) { return this.setReportTableOptions(value) },
    },
  },
  methods: {
    ...mapActions(['setNavigationDrawerStatus', 'changeSelectedTreeViewItem', 'setReportTableOptions']),

    downloadFile(id) {
      let fileURL = getDownloadReportLink(id);
      let fileLink = document.createElement('a');
      fileLink.href = fileURL;
      fileLink.setAttribute('download', 'file.docx');
      document.body.appendChild(fileLink);
      fileLink.click();
    },
    changeSelectedReport: function (item) {
      this.setNavigationDrawerStatus(true)
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
}
</script>

<style scoped>
>>> .v-data-table__wrapper {
  max-height: calc(100% - 59px)
}
</style>
