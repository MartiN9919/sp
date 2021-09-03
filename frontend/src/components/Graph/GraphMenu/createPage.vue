<template>
  <v-col>
    <div class="work-place">
      <selector-object
        v-model="selectedEditableObject"
        :items="baseObjects"
        class="selector-object py-2"
      ></selector-object>
      <v-tabs id="tabs" v-model="activeTab" :color="sliderColor" grow show-arrows center-active :class="tabClasses">
        <v-tab v-for="(item, key) in editableObjects" :key="key">
          <v-icon :color="tabColor(key)">{{ item.object.id.icon }}</v-icon>
          <span :style="{color: tabColor(key)}">
            {{key === 0 ? 'Исходныйобъект' : 'Схожий объект'}}
            {{key + 1}}
          </span>
        </v-tab>
        <v-tab-item v-for="(object, key) in editableObjects" :key="key" eager>
          <v-form :ref="'form' + key" v-model="valid">
            <object-record-area
              :params="object.params"
              @createNewParam="createNewParam"
              @deleteNewParam="deleteNewParam"
            ></object-record-area>
          </v-form>
        </v-tab-item>
      </v-tabs>
    </div>
    <v-divider></v-divider>
    <control-menu
      v-if="editableObjects"
      :buttons="controlButtons"
      @save="saveObject"
      @recreate="selectedEditableObject = selectedEditableObject"
      class="control-menu"
    ></control-menu>
  </v-col>
</template>

<script>
import SelectorObject from "./createPageComponents/selectorObject"
import ObjectRecordArea from "./createPageComponents/objectRecordArea"
import ControlMenu from "./createPageComponents/controlMenu"
import {mapActions, mapGetters} from "vuex"

export default {
  name: "createPage",
  components: {ControlMenu, ObjectRecordArea, SelectorObject},
  data: () => ({
    valid: true,
    activeTab: 0,
  }),
  computed: {
    ...mapGetters(['baseObjects', 'editableObjects']),
    sliderColor: function () { return this.activeTab ? '#FF0000' : '#009688' },
    controlButtons: function () {
      return [
        {
          title: 'Новый',
          action: 'recreate',
          disabled: !!(
            this.editableObjects[this.activeTab]
            && this.editableObjects[this.activeTab].params.find(
              param => param.values.length || param.new_values.length
            )
          ),
        },
        {
          title: this.editableObjects[this.activeTab]?.recId ? 'Сохранить' : 'Создать',
          action: 'save',
          disabled: !!(
            this.valid
            && this.editableObjects[this.activeTab]
            && 'form'+ this.activeTab in this.$refs
            && this.$refs['form' + this.activeTab][0].inputs.length
          )
        },
      ]
    },
    selectedEditableObject: {
      get: function () {
        if(this.editableObjects) return this.editableObjects[0].object.id },
      set: function (id) { this.setEditableObject({object_id: id}) },
    },
    tabClasses: function () {
      if(this.editableObjects)
        if(this.editableObjects.length > 1)
          return 'height-with-tabs'
      return 'height-without-tabs'
    }
  },
  methods: {
    ...mapActions(['getBaseClassifiers', 'addNewParamEditableObject', 'deleteNewParamEditableObject',
      'saveEditableObject', 'setEditableObject', ]),
    tabColor(key) {
      return key ? '#FF0000' : '#009688'
    },
    saveObject () {
      if(this.$refs['form' + this.activeTab][0].validate())
        this.saveEditableObject(this.activeTab)
    },
    createNewParam(event) {
      this.addNewParamEditableObject({id: event, position: this.activeTab})
    },
    deleteNewParam(event) {
      this.deleteNewParamEditableObject({param: event.param, id: event.id, position: this.activeTab})
    },
    tabStatus(objects) {
      this.$el.querySelector('#tabs > .v-item-group').style.display = objects.length <= 1 ? 'none' : 'flex'
    }
  },
  watch: {
    editableObjects: function (objects) {
      this.tabStatus(objects)
    },
  },
  mounted() {
    if(this.editableObjects)
      this.tabStatus(this.editableObjects)
  }
}
</script>

<style scoped>
.work-place {
  height: calc(100% - 3em);
}
.selector-object {
  height: 3.3em;
}
.height-with-tabs, .height-without-tabs  {
  max-height: calc(100% - 3.3em);
}
.control-menu {
  height: 3em;
  align-items: flex-end;
}
.height-with-tabs >>> .v-tab, .height-without-tabs >>> .v-tab {
  min-height: 48px;
}
.height-with-tabs >>> .v-tabs-items, .height-without-tabs >>> .v-tabs-items {
  overflow-y: auto;
}
.height-with-tabs >>> .v-tabs-items {
 max-height: calc(100% - 3.3em - 48px);
}
.height-without-tabs >>> .v-tabs-items {
  max-height: calc(100% - 3.3em);
}
.height-with-tabs >>> .v-slide-group__wrapper, .height-without-tabs  >>> .v-slide-group__wrapper {
  overflow-y: auto;
}
.conflict-title {
  color: #FF0000;
  white-space: nowrap;
}
</style>