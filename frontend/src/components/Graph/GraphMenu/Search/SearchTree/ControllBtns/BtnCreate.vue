<template>
  <drop-down-menu min-width="350" left :close-on-content-click="false">
    <template v-slot:activator="{ on }">
      <v-icon v-on="on">mdi-plus</v-icon>
    </template>
    <template v-slot:body="{ status, closeMenu }">
      <form-create v-if="status" :object-id="objectId" @confirm="$emit('create', $event)" @cancel="closeMenu()"/>
    </template>
  </drop-down-menu>
</template>

<script>
import FormCreate from "@/components/Graph/GraphMenu/Search/SearchTree/ControllForms/FormCreate"
import DropDownMenu from "@/components/WebsiteShell/CustomComponents/dropDownMenu"

export default {
  name: "BtnCreate",
  components: {DropDownMenu, FormCreate},
  props: {
    objectId: Number,
  },
}
</script>

<style scoped>

</style>