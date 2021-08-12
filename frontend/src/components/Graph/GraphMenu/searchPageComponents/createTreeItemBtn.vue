<template>
  <drop-down-menu min-width="350" left :close-on-content-click="false">
    <template v-slot:activator="{ on }">
      <v-btn icon v-on="on">
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </template>
    <template v-slot:body="{ status, closeMenu }">
      <creator-object
        v-if="status"
        :object-id="objectId"
        @confirm="$emit('create', $event)"
        @cancel="closeMenu()"
      ></creator-object>
    </template>
  </drop-down-menu>
</template>

<script>
import CreatorObject from "./creatorObject"
import DropDownMenu from "../../../WebsiteShell/UI/dropDownMenu"

export default {
  name: "createButton",
  components: {DropDownMenu, CreatorObject},
  props: {
    objectId: Number,
  },
}
</script>

<style scoped>

</style>