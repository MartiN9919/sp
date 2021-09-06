<template>
  <v-list class="py-0">
    <v-list-item class="title-table">
      <v-list-item-subtitle class="text-title-table">Найдено объектов: {{objects.length}}</v-list-item-subtitle>
    </v-list-item>
    <div class="body-table">
    <v-list-item v-for="object in objects" :key="object.rel_id" class="px-0" @click="">
      <v-hover v-slot="{ hover }">
        <v-card
          tile flat width="100%" height="100%"
          :class="hover ? ['body-content-hover', 'body-content'] : ['body-content']"
        >
          <v-card-text class="pr-0">{{object.title}}</v-card-text>
          <div
              v-if="hover" class="d-flex align-center list-icons"
              :class="hover ? ['list-icons-hover', 'list-icons'] : ['list-icons']">
            <v-btn icon @click="$emit('select', object)"><v-icon>mdi-plus</v-icon></v-btn>
            <v-btn icon @click="$emit('change', object)"><v-icon>mdi-pencil-outline</v-icon></v-btn>
            <v-btn icon><v-icon>mdi-close</v-icon></v-btn>
          </div>
        </v-card>
      </v-hover>
    </v-list-item>
    </div>
  </v-list>
</template>

<script>
import {mapActions} from "vuex";

export default {
  name: "foundObjects",
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
  height: calc(100% - 2.5em);
}
.body-content {
  display: flex;
  flex-direction: row;
  align-items: center;
}
.list-icons {
  position:absolute;
  background-color: white;
  right: 0;
  height: 100%
}
.list-icons-hover  {
  background-color: #f5f5f5;
}
.body-content-hover {
  background-color: #f5f5f5;
}
</style>