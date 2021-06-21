<template>
  <v-text-field
    :label="variable.title"
    v-model="variable.value"
    placeholder="Выберете объект на карте"
    hide-details color="teal" readonly class="pt-0 mt-0" type="text">
    <template v-slot:append>
      <geometry-input-dialog
        :value="variable.value !== null ? variable.value : []"
        @changeValueGeometry="variable.value = $event"
      ></geometry-input-dialog>
    </template>
  </v-text-field>
</template>

<script>
import geometryInputDialog from "./geometryInputDialog";
export default {
  name: "geometryInput",
  components: { geometryInputDialog, },
  props: {
    variable: Object,
  }

}
</script>

<style scoped>

</style>