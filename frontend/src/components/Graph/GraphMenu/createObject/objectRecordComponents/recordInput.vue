<template>
  <v-col>
    <settings-analytics
        v-model="param.value"
        :type="type"
        :list="list"
        :rules="[ v => !!v || 'Поле должно быть заполнено', ]"
        :hide-details="false"
        deletable
        class="pt-1"
        @deletable="$emit('deletable')"
    >
      <template v-slot:message>
        <drop-down-menu nudge-left="290" min-width="auto" close-on-click :close-on-content-click="false">
          <template v-slot:activator="{ on }">
            <div style="width: 100%" class="text-end text-no-wrap">
              <span v-on="on" class="v-messages" style="cursor: pointer; color: #004D40; font-size: 0.9em">{{param.date}}</span>
            </div>
          </template>
          <template v-slot:body="{ closeMenu, status }">
            <menu-date-time v-if="status" v-model="param.date" :close-menu="closeMenu"></menu-date-time>
          </template>
        </drop-down-menu>
      </template>
    </settings-analytics>
  </v-col>
</template>

<script>
import MenuDateTime from "../../../../WebsiteShell/InputForms/InputFormsUI/menuDateTime"
import SettingsAnalytics from "../../../../Map/MapMenu/scriptsPage/settingsAnalytics"
import DropDownMenu from "../../../../WebsiteShell/InputForms/BodyToForm/dropDownMenu"

export default {
  name: "recordInput",
  components: {DropDownMenu, MenuDateTime, SettingsAnalytics, },
  props: {
    param: Object,
    type: String,
    list: Array,
  },
}
</script>

<style scoped>

</style>