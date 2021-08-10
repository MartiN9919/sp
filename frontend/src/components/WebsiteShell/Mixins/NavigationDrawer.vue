<script>
import router from '@/router'
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'NavigationDrawer',
  computed: {
    ...mapGetters(['navigationDrawerStatus']),

    drawer: {
      get: function () {
        return this.navigationDrawerStatus(router.currentRoute.name)
      },
      set: function (val) {
        if (val !== this.navigationDrawerStatus(router.currentRoute.name)) { this.changeNavigationDrawerStatus() }
      }
    }
  },
  methods: {
    ...mapActions(['changeNavigationDrawerStatus']),
  },
}
</script>
