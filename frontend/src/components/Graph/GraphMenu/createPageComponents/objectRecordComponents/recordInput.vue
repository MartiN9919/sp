<template>
  <v-col>
    <responsive-input-form
      v-model="param.value"
      :type="type"
      :items="list"
      :rules="[v => !!v || 'Поле должно быть заполнено']"
      :hide-details="false"
      deletable
      class="pt-1"
      @deletable="$emit('deletable')"
    >
      <template v-slot:message>
        <drop-down-menu nudge-left="290" min-width="auto" close-on-click :close-on-content-click="false">
          <template v-slot:activator="{ on }">
            <div style="width: 100%; font-size: 1.2em; padding-top: 1px;" class="text-end text-no-wrap">
              <span v-on="on" class="v-messages" style="cursor: pointer; color: #004D40; font-size: 0.9em">{{param.date}}</span>
            </div>
          </template>
          <template v-slot:body="{ closeMenu, status }">
            <select-date-time v-if="status" v-model="param.date" :close-menu="closeMenu"></select-date-time>
          </template>
        </drop-down-menu>
      </template>
    </responsive-input-form>
  </v-col>
</template>

<script>
import ResponsiveInputForm from "../../../../WebsiteShell/UI/responsiveInputForm"
import DropDownMenu from "../../../../WebsiteShell/UI/dropDownMenu"
import SelectDateTime from "../../../../WebsiteShell/UI/selectDateTime"

export default {
  name: "recordInput",
  components: {DropDownMenu, SelectDateTime, ResponsiveInputForm},
  props: {
    param: Object,
    type: String,
    list: Array,
  },
}
</script>

<style scoped>

</style>