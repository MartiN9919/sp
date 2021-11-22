<template>
  <v-list class="py-0" v-if="objects">
    <v-list-item class="title-table">
      <v-list-item-subtitle class="text-title-table">Найдено объектов: {{objects.length}}</v-list-item-subtitle>
    </v-list-item>
    <div class="body-table">
    <v-hover v-for="object in objects" :key="object.rel_id" v-slot="{ hover }">
      <v-list-item class="px-0 py-1" @click="">
        <v-list-item-icon class="mx-1 my-0">
          <trigger-information :active-triggers="object.triggers"></trigger-information>
        </v-list-item-icon>
        <v-list-item-subtitle class="text-pre-wrap mx-1 text-info">{{object.title}}</v-list-item-subtitle>
        <v-list-item-action v-show="hover" class="flex-row ma-0 action-buttons">
          <v-btn icon @click="$emit('select', object)"><v-icon>mdi-plus</v-icon></v-btn>
          <v-btn icon @click="$emit('change', object)"><v-icon>mdi-pencil-outline</v-icon></v-btn>
          <v-btn icon><v-icon>mdi-close</v-icon></v-btn>
        </v-list-item-action>
      </v-list-item>
    </v-hover>
    </div>
  </v-list>
</template>

<script>
import CustomTooltip from "@/components/WebsiteShell/CustomComponents/customTooltip"
import TriggerInformation from "@/components/WebsiteShell/CustomComponents/triggerInformation"
export default {
  name: "foundObjects",
  components: {TriggerInformation, CustomTooltip},
  props: {
    objects: Array,
  },
}
</script>

<style scoped>
.title-table {
  background-color: rgba(0, 0, 0, .1);
  max-height: 2em;
}
.text-title-table {
  display: flex;
  justify-content: space-around;
}
.body-table {
  overflow-y: auto;
  height: calc(100% - 36px);
}
.list-icons {
  position:absolute;
  right: 0;
}
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