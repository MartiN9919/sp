<template>
  <v-text-field
    :label="variable.title"
    v-model="variable.value"
    placeholder="Выберете объект на карте"
    hide-details color="teal" readonly class="pt-0 mt-0" type="text">
    <template v-slot:append>
      <map-dialog-for-geometry-input
        :value="variable.value !== null ? variable.value : []"
        @changeValueGeometry="variable.value = $event"
      ></map-dialog-for-geometry-input>
    </template>
  </v-text-field>
</template>

<script>
import mapDialogForGeometryInput from "./mapDialogForGeometryInput";
export default {
  name: "geometryInput",
  components: {mapDialogForGeometryInput, },
  props: {
    variable: Object,
  }

}
</script>

<style scoped>

</style>