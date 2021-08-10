<template>
  <div>

  </div>
</template>

<script>
import DropDownMenu from "../../../WebsiteShell/InputForms/BodyToForm/dropDownMenu"

export default {
  name: "dossier",
  components: { DropDownMenu, },
  data: () => ({
    overlay: false,
    selectMenu: false,
    bodyItems: ['asdas dads as d asd asd as das das das dasd 12312312312312312312312312312', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
  }),
  methods: {
    tezt(){
      console.log('tezt')
    }
  }
}
</script>

<style scoped>

</style>