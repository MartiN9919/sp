<script>
import router from '@/router'
import { mapActions, mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters(['treeViewItems', 'selectedTreeViewItem']),
    treeView: function () { return this.treeViewItems(router.currentRoute.name) },
    selectedItem: function () { return this.selectedTreeViewItem(router.currentRoute.name) }
  },
  methods: mapActions(['getTreeViewItemsFromServer']),
  mounted () {
    this.getTreeViewItemsFromServer({ params: { script_type: router.currentRoute.name } })
  }
}
</script>
