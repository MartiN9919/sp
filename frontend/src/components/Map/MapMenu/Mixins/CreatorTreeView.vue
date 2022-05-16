<script>
import router from '@/router'
import { mapActions, mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters(['treeViewItems', 'selectedTreeViewItem', 'scriptSearch']),
    search: {
      get: function () {
        return this.scriptSearch(router.currentRoute.name)
      },
      set: function (search) {
        this.setScriptSearch(search)
      }
    },
    treeView: function () { return this.treeViewItems(router.currentRoute.name) },
    selectedItem: function () { return this.selectedTreeViewItem(router.currentRoute.name) }
  },
  methods: mapActions(['getTreeViewItemsFromServer', 'setScriptSearch']),
  mounted () {
    this.getTreeViewItemsFromServer({ params: { script_type: router.currentRoute.name } })
  }
}
</script>
