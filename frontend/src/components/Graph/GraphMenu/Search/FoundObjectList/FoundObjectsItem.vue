<template>
  <v-hover v-slot="{ hover }">
    <v-list-item
        @keyup.ctrl.enter="select"
        @keyup.alt.enter="change"
        class="px-0 py-1 v-list-item--link"
    >
      <v-list-item-icon class="mx-1 my-0">
        <trigger-information :active-triggers="object.triggers"/>
      </v-list-item-icon>
      <v-list-item-subtitle class="text-pre-wrap mx-1 text-info">
        {{object.title}}
      </v-list-item-subtitle>
      <v-list-item-action v-show="hover" class="flex-row ma-0 action-buttons">
        <v-btn icon @click="select" tabindex="-1">
          <v-icon>mdi-plus</v-icon>
        </v-btn>
        <v-btn icon @click="change" tabindex="-1">
          <v-icon>mdi-pencil-outline</v-icon>
        </v-btn>
      </v-list-item-action>
    </v-list-item>
  </v-hover>
</template>

<script>
import {mapActions} from "vuex"
import TriggerInformation from "@/components/WebsiteShell/CustomComponents/triggerInformation"

export default {
  name: "FoundObjectItem",
  components: {TriggerInformation},
  props: {
    object: Object
  },
  methods: {
    ...mapActions(['setEditableObject', 'addObjectToGraph']),
    select() {
      this.addObjectToGraph({
        object: this.object,
        action: {
          name: 'addObjectToGraph',
          payload: this.object.title
        }
      })
    },
    change() {
      this.setEditableObject(this.object)
    }
  }
}
</script>

<style scoped>
.v-list-item {
  min-height: 36px;
}
.text-info {
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}
.action-buttons {
  min-width: auto;
}
</style>