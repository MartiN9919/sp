<script>
import router from '@/router'
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'NavigationDrawer',
  computed: {
    ...mapGetters(['navigationDrawerStatus']),
    drawer: {
      get: function () { return this.navigationDrawerStatus(router.currentRoute.name) },
      set: function (val) { this.setNavigationDrawerStatus(val) }
    }
  },
  methods: {
    ...mapActions(['setNavigationDrawerStatus']),
    changeNavigationDrawerStatus() {
      this.drawer = !this.drawer;
    }
  },
}
</script>
