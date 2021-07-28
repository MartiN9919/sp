<template>
  <span class="message-text-style v-messages">
    <v-icon size="15">{{objectIcon}}</v-icon>
    {{informationAboutObject}}
    Актуальность: <v-icon size="15" :color="objectActual.color">{{objectActual.icon}}</v-icon>
  </span>
</template>

<script>
import {mapGetters} from "vuex";

export default {
  name: "treeItemInfo",
  props: {
    object: Object,
  },
  computed: {
    ...mapGetters(['primaryObject', 'relationObject', ]),
    objectIcon: function () { return this.primaryObject(this.object.object_id).icon },
    objectActual: function () {
      return this.object.actual ? { icon: 'mdi-check', color: 'green' } : { icon: 'mdi-close', color: 'red'}
    },
    informationAboutObject: function() {
      let message = ''
      if (this.object.rel) {
        let relation = this.relationObject(this.object.rel.id)
        if (this.object.rel.id)
          message += relation.title
        if (this.object.rel.value)
          message += '(' + relation.list.find(i => i.id === this.object.rel.value).value + ')'
        if (this.object.rel.date_time_start)
          message += ' c ' + this.object.rel.date_time_start
        if (this.object.rel.date_time_end)
          message += ' по ' + this.object.rel.date_time_end
      }
      return message
    },
  }
}
</script>

<style scoped>
  .message-text-style {
    white-space: normal
  }
</style>