<template>
  <v-list class="py-0" v-if="foundObjects">
    <custom-tooltip right>
      <template v-slot:activator="{ on }">
        <v-list-item v-on="on" class="title-table">
          <v-list-item-subtitle class="text-title-table align-center">
            Найдено объектов: {{foundObjects.length}}
          </v-list-item-subtitle>
        </v-list-item>
      </template>
      <template v-slot:body>
        <v-card dark>
          <v-list dense color="teal darken-2">
            <v-list-item v-for="(objects, title) in combination" :key="title">
              <v-list-item-title>{{ title }}: {{ objects.length }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-card>
      </template>
    </custom-tooltip>
    <div class="body-table">
      <template v-if="searchGroup">
        <found-object-group v-for="(objects, title) in combination" :key="title" :objects="objects" :title="title"/>
      </template>
      <found-object-group v-else :objects="foundObjects"/>
    </div>
  </v-list>
</template>

<script>
import FoundObjectItem from "@/components/Graph/GraphMenu/Search/FoundObjectList/FoundObjectsItem"
import {mapGetters} from "vuex"
import CustomTooltip from "@/components/WebsiteShell/CustomComponents/Tooltip/customTooltip";
import FoundObjectGroup from "@/components/Graph/GraphMenu/Search/FoundObjectList/FoundObjectGroup";

export default {
  name: "FoundObjectList",
  components: {FoundObjectGroup, CustomTooltip, FoundObjectItem},
  computed: {
    ...mapGetters(['foundObjects', 'baseObject', 'searchSettingsValue']),
    searchGroup: function () {
      return this.searchSettingsValue('searchGroup')
    },
    combination: function () {
      let comb = {}
      for(const object of this.foundObjects) {
        let base = this.baseObject(object.object_id).title
        if(comb.hasOwnProperty(base)) {
          comb[base].push(object)
        } else {
          comb[base] = [object]
        }
      }
      return comb
    }
  }
}
</script>

<style scoped>
.title-table {
  background-color: rgba(0, 0, 0, .1);
  min-height: 36px;
}
.text-title-table {
  display: flex;
  justify-content: space-around;
}
.body-table {
  overflow-y: auto;
  height: calc(100% - 36px);
}
</style>