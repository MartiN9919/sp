<script>
import router from '@/router'
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'CreatorTreeView',
  data: () => ({
    sizeMenuColumn: 30,
    findFolders: []
  }),
  mounted () {
    if (localStorage['size' + router.currentRoute.name + 'MenuColumn']) {
      this.sizeMenuColumn = parseInt(localStorage['size' + router.currentRoute.name + 'MenuColumn'])
    }
  },
  watch: {
    sizeMenuColumn (newSizeMenuColumn) {
      localStorage['size' + router.currentRoute.name + 'MenuColumn'] = newSizeMenuColumn
    }
  },
  computed: {
    ...mapGetters(['treeViewItems', 'selectedTreeViewItem']),

    treeView: function () { return this.treeViewItems(router.currentRoute.name) },

    selectedItem: function () { return this.selectedTreeViewItem(router.currentRoute.name) }

  },
  created () {
    this.getTreeViewItemsFromServer({ params: { script_type: router.currentRoute.name } })
  },
  methods: {
    ...mapActions(['getTreeViewItemsFromServer'])
  }
}
</script>
