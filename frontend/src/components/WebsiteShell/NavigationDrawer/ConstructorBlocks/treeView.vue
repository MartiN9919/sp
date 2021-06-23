<template>
  <v-treeview
    :items=treeViewItems
    :open.sync="listOpenFolder"
    class="py-1"
    open-on-click
    active-class=""
    color=""
    @update:active="activateItem"
    activatable
    hoverable
    return-object
    transition
    dense>

    <template v-slot:label="{ item, open }">
      <v-tooltip bottom open-delay="1000" color="teal" style="z-index: 10001" max-width="20%">
        <template v-slot:activator="{ on, attrs }">
          <div v-bind="attrs" v-on="on">
            <v-icon
                :id="'btn' + item.id"
                :color="selectedTreeViewItem.id === item.id
                || findFolders.find(folder => folder.id === item.id) ?
                'teal' : 'grey lighten-1'"
            >
              {{ item.icon ? open ? 'mdi-folder-open-outline' : 'mdi-folder-outline' : 'mdi-script-text-outline' }}
            </v-icon>
            <span
                :class="item.icon ? 'text-uppercase' : 'text-lowercase'"
                class="pl-2"
                :style="selectedTreeViewItem.id === item.id ? {color: 'teal'} : {}">{{ item.name }}</span>
          </div>
        </template>
        <p class="text-justify ma-0">{{ item.hint ? item.hint : 'Описание отсутствует' }}</p>
      </v-tooltip>
    </template>

  </v-treeview>
</template>

<script>
function sleep (time) {
  return new Promise((resolve) => setTimeout(resolve, time))
}

export default {
  name: 'treeView',
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
            '#btn' + item.id,
            { duration: 300, offset: 100, easing: 'easeInOutCubic', container: '.v-treeview' })
        })
      } else this.findFolders = []
    }
  },
  methods: {

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
            if (this.findFolders.indexOf(treeViewItem) === -1) { this.findFolders.push(treeViewItem) }
            if (this.findItemInTreeView(item, treeViewItem.children)) { return true } else this.findFolders.splice(this.findFolders.indexOf(treeViewItem))
          }
        } else return true
      }
      return false
    }
  },
}
</script>
