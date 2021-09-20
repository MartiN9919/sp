<template>
  <drop-down-menu :close-on-content-click=false>
    <template v-slot:activator="{ on }">
      <v-icon right v-on="on" :color="color">mdi-brush</v-icon>
    </template>
    <template v-slot:body>
      <v-color-picker :value="color" @input="$emit('changeColor', $event)" hide-inputs></v-color-picker>
    </template>
  </drop-down-menu>
</template>

<script>
import DropDownMenu from "@/components/WebsiteShell/UI/dropDownMenu";
export default {
  name: "customColorPicker",
  components: {DropDownMenu},
  props: {color: String},
  model: {prop: 'color', event: 'changeColor'},

}
</script>

<style scoped>

</style>