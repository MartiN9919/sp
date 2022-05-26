<template>
  <v-card class="ma-2">
    <v-list class="pt-0">
      <item-settings v-model="state" :title="trigger.title" :sub-title="trigger.subTitle"/>
      <v-divider v-if="trigger.variables.length" class="pb-2"/>
      <v-form :ref="'form' + trigger.id" onSubmit="return false;">
        <v-list-item v-for="param in trigger.variables" :key="param.name">
          <custom-tooltip
              :description="param.hint"
              :type="param.type"
              :value="param.value"
              nudge-right="20"
              right
          >
            <template v-slot:activator="{on}">
              <div v-on="on" class="w-100">
                <responsive-input-form
                    v-model="param.value"
                    @changeInputString="state = false"
                    :input-type="param.type"
                    :label="param.title"
                    :list-rules="param.necessary ? ['notEmpty'] : []"
                />
              </div>
            </template>
          </custom-tooltip>
        </v-list-item>
      </v-form>
    </v-list>
  </v-card>
</template>

<script>
import ResponsiveInputForm from "@/components/WebsiteShell/CustomComponents/responsiveInputForm"
import ItemSettings from "@/components/Graph/GraphMenu/Settings/Modules/ItemSettings"
import {mapActions} from "vuex"
import CustomTooltip from "@/components/WebsiteShell/CustomComponents/Tooltip/customTooltip";

export default {
  name: "ItemTriggerSettings",
  components: {CustomTooltip, ItemSettings, ResponsiveInputForm},
  props: {
    trigger: Object
  },
  computed: {
    state: {
      get: function () {
        return this.trigger.state
      },
      set: function (value) {
        const setTrigger = value => this.setTriggerState({triggerId: this.trigger.id, value})
        if(value) {
          if (this.$refs['form' + this.trigger.id].validate()) {
            setTrigger(value)
          }
        } else {
          setTrigger(value)
        }
      }
    }
  },
  methods: mapActions(['setTriggerState'])
}
</script>

<style scoped>

</style>