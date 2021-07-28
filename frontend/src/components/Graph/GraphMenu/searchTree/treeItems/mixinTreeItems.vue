<script>
import DeleteTreeItemBtn from "./actionButtons/deleteTreeItemBtn"
import CreateTreeItemBtn from "./actionButtons/createTreeItemBtn"
import ChangeTreeItemBtn from "./actionButtons/changeTreeItemBtn"
import TreeItemInfo from "./treeItemInfo"
import BodyInputTreeItem from "./bodyInputTreeItem"

export default {
  name: "mixinTreeItems",
  components: { DeleteTreeItemBtn, CreateTreeItemBtn, ChangeTreeItemBtn, TreeItemInfo, BodyInputTreeItem, },
  props: {
    object: Object,
  },
  data: () => ({
    hover: false,
  }),
  methods: {
    changeHover(value) {
      this.hover = value
    },
  },
}
</script>
