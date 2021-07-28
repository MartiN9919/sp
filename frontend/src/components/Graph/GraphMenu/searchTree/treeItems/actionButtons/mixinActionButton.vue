<script>
let menu = null

export default {
  name: "mixinActionButton",
  props: {
    object: Object,
  },
  data: () => ({
    menuModal: false,
  }),
  methods: {
    cancel() { this.menuModal = false },
  },
  watch: {
    menuModal: function (value) {
      if (value) {
        if (menu && menu !== this)
          menu.menuModal = false
        menu = this
      }
    }
  }
}
</script>
