<template>
  <drop-down-menu min-width="350" left :close-on-content-click="false">
    <template v-slot:activator="{ on }">
      <v-icon v-on="on" size="22">mdi-pencil-outline</v-icon>
    </template>
    <template v-slot:body="{ status, closeMenu }">
      <form-create
        v-if="status && !!parent"
        :object-id="parent.object.id"
        :change-object="item"
        @confirm="$emit('change', $event)"
        @cancel="closeMenu()"
      />
      <form-change
        v-else-if="status && !parent"
        :object-settings="{ object_id: item.object.id, actual: item.actual }"
        @confirm="$emit('change', $event)"
        @cancel="closeMenu()"
      />
    </template>
  </drop-down-menu>
</template>

<script>
import FormChange from "@/components/Graph/GraphMenu/Search/SearchTree/ControllForms/FormChange"
import FormCreate from "@/components/Graph/GraphMenu/Search/SearchTree/ControllForms/FormCreate"
import DropDownMenu from "@/components/WebsiteShell/CustomComponents/dropDownMenu"

export default {
  name: "BtnChange",
  components: {DropDownMenu, FormCreate, FormChange},
  props: {
    item: Object,
    parent: {
      type: Object,
      default: () => null
    }
  }
}
</script>
