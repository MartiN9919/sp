<template>
  <v-list class="py-0">
    <v-list-item class="title-table">
      <v-list-item-subtitle>Найдено объектов: {{objects.length}}</v-list-item-subtitle>
    </v-list-item>
    <div class="body-table">
    <v-list-item v-for="object in objects" :key="object.rel_id" class="px-0" @click="">
      <v-hover v-slot="{ hover }">
        <v-card tile flat width="100%" height="100%" :class="bodyContentClasses">
          <v-card-text class="pr-0">{{object.title}}</v-card-text>
          <div v-if="hover" class="d-flex align-center list-icons" :class="listIconsClasses">
            <v-btn icon><v-icon>mdi-plus</v-icon></v-btn>
            <v-btn icon><v-icon>mdi-check</v-icon></v-btn>
            <v-btn icon><v-icon>mdi-close</v-icon></v-btn>
          </div>
        </v-card>
      </v-hover>
    </v-list-item>
    </div>
  </v-list>
</template>

<script>
export default {
  name: "foundObjects",
  props: {
    objects: Array,
  },
  computed: {
    bodyContentClasses: function () { return this.hover ? ['body-content-hover', 'body-content'] : ['body-content'] },
    listIconsClasses: function () { return this.hover ? ['list-icons-hover', 'list-icons'] : ['list-icons'] },
  },
}
</script>

<style scoped>
.title-table {
  background-color: #f5f5f5;
  max-height: 2em;
}
.body-table {
  overflow-y: auto;
  height: calc(100% - 2em);
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