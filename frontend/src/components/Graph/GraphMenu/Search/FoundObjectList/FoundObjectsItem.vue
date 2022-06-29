<template>
  <v-lazy :options="{threshold: .5}" min-height="36" transition="fade-transition">
    <v-list-item
        @click.exact="showDescription"
        @keyup.ctrl.enter="change"
        link
        class="px-0 py-1"
    >
      <v-list-item-icon class="mx-1 my-0 align-self-center">
        <v-badge overlap bottom offset-y="18" offset-x="20" color="rgba(0, 0, 0, 0)" class="badge">
          <template v-slot:badge>
            <trigger-information :active-triggers="object.triggers" size="20px"/>
          </template>
          <v-icon>{{$store.getters.baseObject(object.object_id).icon}}</v-icon>
        </v-badge>
      </v-list-item-icon>
      <v-list-item-subtitle class="text-pre-wrap mx-1 text-info">{{object.title}}</v-list-item-subtitle>
      <description :viewDat="description"/>
    </v-list-item>
  </v-lazy>
</template>

<script>
import {mapActions} from "vuex"
import TriggerInformation from "@/components/WebsiteShell/CustomComponents/triggerInformation"
import Description from "@/components/Map/Leaflet/Description"

export default {
  name: "FoundObjectItem",
  components: {Description, TriggerInformation},
  props: {
    object: Object
  },
  data: () => ({
    description: null
  }),
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
    showDescription() {
      this.description = [this.object.object_id, this.object.rec_id]
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
</style>