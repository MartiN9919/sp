<template>
  <drop-down-menu min-width="350" left :close-on-content-click="false">
    <template v-slot:activator="{ on }">
      <v-btn icon v-on="on">
        <v-icon>mdi-pencil-outline</v-icon>
      </v-btn>
    </template>
    <template v-slot:body="{ status, closeMenu }">
      <creator-object
        v-if="status && !!parentObject"
        :object-id="parentObject.object_id"
        :change-object="object"
        @confirm="$emit('change', $event)"
        @cancel="closeMenu()"
      ></creator-object>
      <change-root-object
        v-else-if="status && !parentObject"
        :object-settings="{ object_id: object.object_id, actual: object.actual }"
        @confirm="$emit('change', $event)"
        @cancel="closeMenu()"
      ></change-root-object>
    </template>
  </drop-down-menu>
</template>

<script>
import DropDownMenu from "../../../WebsiteShell/UI/dropDownMenu"
import ChangeRootObject from "./changeRootObject"
import CreatorObject from "./creatorObject"

export default {
  name: "changeTreeItemBtn",
  components: {DropDownMenu, CreatorObject, ChangeRootObject},
  props: {
    object: Object,
    parentObject: {
      type: Object,
      default: function () { return null },
    },
  },
}
</script>
