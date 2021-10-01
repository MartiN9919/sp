<template>
  <div class="search-input-form">
    <drop-down-menu min-width="100%" close-on-click :close-on-content-click="false" attach :offset-x="false" :offset-y="false">
      <template v-slot:activator="{ on }">
        <div v-on="on">
          <body-input-form readonly>
<!--            <template v-slot:label>-->
<!--              {{title}}-->
<!--            </template>-->
            <template v-slot:append="{ hover }" class="action-icon">
              <v-icon
                  v-if="hover"
                  @click.stop="$emit('deletable')"
                  size="24"
              >mdi-delete</v-icon>
              <v-icon v-else size="24" >mdi-calendar</v-icon>
            </template>
            <template v-slot:message>
              <slot name="message"></slot>
            </template>
          </body-input-form>
        </div>
      </template>
      <template v-slot:body="{ closeMenu,  status }">
        <h1>hello</h1>
      </template>
    </drop-down-menu>
  </div>
</template>

<script>
import DropDownMenu from "@/components/WebsiteShell/UI/dropDownMenu";
import BodyInputForm from "@/components/WebsiteShell/UI/bodyInputForm";
export default {
name: "searchInput",
  components: {BodyInputForm, DropDownMenu}
}
</script>

<style scoped>

</style>