<script>
import router from '@/router'
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'NavigationDrawer',
  data: () => ({
    sizeNavigation: 30,
  }),
  mounted () {
    if (localStorage['size' + router.currentRoute.name + 'Menu']) {
      this.sizeNavigation = parseInt(localStorage['size' + router.currentRoute.name + 'Menu'])
    }
    document.getElementsByClassName('column')[0].classList.add('shadow-effect')
  },
  watch: {
    sizeNavigation (newSizeMenu) {
      localStorage['size' + router.currentRoute.name + 'Menu'] = newSizeMenu
    }
  },
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
