<template>
  <drop-down-menu min-width="350" left :close-on-content-click="false">
    <template v-slot:activator="{ on }">
      <v-btn icon v-on="on">
        <v-icon>mdi-pencil-outline</v-icon>
      </v-btn>
    </template>
    <template v-slot:body="{ status, closeMenu }">
      <creator-object
        v-if="status && !!parentItem"
        :object-id="parentItem.object.id"
        :change-object="item"
        @confirm="$emit('change', $event)"
        @cancel="closeMenu()"
      ></creator-object>
      <change-root-object
        v-else-if="status && !parentItem"
        :object-settings="{ object_id: item.object.id, actual: item.actual }"
        @confirm="$emit('change', $event)"
        @cancel="closeMenu()"
      ></change-root-object>
    </template>
  </drop-down-menu>
</template>

<script>
import ChangeRootObject from "@/components/Graph/GraphMenu/searchPageComponents/changeRootObject"
import CreatorObject from "@/components/Graph/GraphMenu/searchPageComponents/creatorObject"
import DropDownMenu from "@/components/WebsiteShell/CustomComponents/dropDownMenu"

export default {
  name: "changeTreeItemBtn",
  components: {DropDownMenu, CreatorObject, ChangeRootObject},
  props: {
    item: Object,
    parentItem: {
      type: Object,
      default: function () { return null },
    },
  },
}
</script>
