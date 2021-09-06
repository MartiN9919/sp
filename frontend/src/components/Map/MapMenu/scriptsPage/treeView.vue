<template>
  <v-treeview
    :items=treeViewItems :open.sync="listOpenFolder" @update:active="activateItem"
    return-object open-on-click activatable dense active-class="" color=""
  >
    <template v-slot:label="{ item, open }">
      <custom-tooltip :body-text="item.hint">
        <template v-slot:activator="{ on }">
          <div v-on="on">
            <v-icon :id="iconId(item.id)" :color="colorIcon(item)">{{ typeIcon(item, open) }}</v-icon>
            <span :class="itemTextStyle(item.icon)" :style="itemTextColor(item)">{{ item.name }}</span>
          </div>
        </template>
      </custom-tooltip>
    </template>
  </v-treeview>
</template>

<script>
import CustomTooltip from "../../../WebsiteShell/UI/customTooltip"

function sleep (time) {
  return new Promise((resolve) => setTimeout(resolve, time))
}

export default {
  name: 'treeView',
  components: {CustomTooltip},
  data: () => ({
    listOpenFolder: [],
    findFolders: [],
    lastActiveItem: null
  }),
  props: {
    treeViewItems: Array,
    selectedTreeViewItem: Object
  },
  watch: {
    selectedTreeViewItem: function (item) {
      if (item.id) {
        this.findFolders = []
        this.findItemInTreeView(item, this.treeViewItems)
        this.listOpenFolder = this.listOpenFolder.concat(this.findFolders)
        sleep(500).then(() => {
          this.$vuetify.goTo(
            '#' + this.iconId(item.id),
            { duration: 300, offset: 100, easing: 'easeInOutCubic', container: '.v-treeview' })
        })
      } else this.findFolders = []
    }
  },
  methods: {
    itemTextColor(item) {
      return this.checkForSelectedItem(item) ? { color: '#00796B' } : {}
    },
    checkForSelectedItem(item) {
      return this.selectedTreeViewItem.id === item.id
    },
    itemTextStyle(status) {
      return status ? 'text-uppercase pl-2' : 'text-lowercase pl-2'
    },
    typeIcon(item, open) {
      return item.icon ? open ? 'mdi-folder-open-outline' : 'mdi-folder-outline' : 'mdi-script-text-outline'
    },
    iconId(id) {
      return 'btn' + id
    },
    colorIcon(item) {
      return this.checkForSelectedItem(item) ||
      this.findFolders.find(folder => folder.id === item.id) ? '#00796B' : '#616161'
    },

    /** Вызов родительского метода обработки выбора скрипта */
    activateItem (item) {
      /** Функция преобразования функционала v-treeview "активации" в функционал "выбора" */
      if (item.length) {
        /** Вызов родительского метода и передача ему глубокой копии выбранного скрипта */
        this.$emit('changeSelectedTreeViewItem', JSON.parse(JSON.stringify(item[0])))
        this.lastActiveItem = item[0]
      } else {
        /** Вызов родительского метода и передача ему глубокой копии выбранного скрипта */
        this.$emit('changeSelectedTreeViewItem', JSON.parse(JSON.stringify(this.lastActiveItem)))
        this.lastActiveItem = null
      }
    },

    /**
     * Рекурсивная функция обхода дерева и нахождение скрипта по его id
     * @param {Object} item - Переменная которую ищем
     * @param {Array} treeViewItems - Массив по которому ищем
     * @returns {boolean}
     */
    findItemInTreeView (item, treeViewItems) {
      for (const treeViewItem of treeViewItems) {
        if (treeViewItem.id !== item.id) {
          if ('children' in treeViewItem) {
            if (this.findFolders.indexOf(treeViewItem) === -1)
              this.findFolders.push(treeViewItem)
            if (this.findItemInTreeView(item, treeViewItem.children))
              return true
            else this.findFolders.splice(this.findFolders.indexOf(treeViewItem))
          }
        } else return true
      }
      return false
    }
  }
}
</script>
