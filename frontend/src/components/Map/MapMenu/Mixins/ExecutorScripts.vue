<script>
import { mapActions } from 'vuex'
import router from '@/router'

export default {
  name: 'ExecutorScripts',
  methods: {
    ...mapActions(['executeMapScript', 'executeReportScript']),
    executeScript: function (script) {
     // if(this.$refs.form.validate()) {
       if (router.currentRoute.name === 'Map') this.executeMapScript({ request: script, config: {} })
       if (router.currentRoute.name === 'Report') this.executeReportScript({ request: script, config: {} })
     // }
    }
  }
}
</script>
