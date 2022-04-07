<template>
  <create-page-body :editable="!editableObjects" info="Выберите тип объекта для создания">
    <template v-slot:header>
      <selector-object v-model="selectedEditableObject" :items="baseObjects" class="selector-object"/>
    </template>
    <template v-slot:body>
      <v-tabs id="tabs" v-model="activeTab" :color="sliderColor" grow show-arrows center-active :class="tabClasses">
        <v-tab v-for="(item, key) in editableObjects" :key="key">
          <v-icon :color="tabColor(key)">{{ item.base.icon }}</v-icon>
          <span :style="{color: tabColor(key)}">
            {{key === 0 ? 'Исходный объект' : 'Схожий объект'}}
            {{key + 1}}
          </span>
        </v-tab>
        <v-tab-item v-for="(object, key) in editableObjects" :key="key" eager>
          <v-form :ref="'form' + key" v-model="valid" onSubmit="return false;">
            <record-area
              :params="object.params"
              :title="object.title"
              :settings="{objectId: object.ids.object_id, recId: object.ids.rec_id}"
              @createNewParam="createNewParam"
              @deleteNewParam="deleteNewParam"
            />
          </v-form>
        </v-tab-item>
      </v-tabs>
    </template>
    <template v-slot:control>
      <control-menu :buttons="controlButtons" @save="saveObject" @recreate="recreateObject" class="control-menu"/>
    </template>
  </create-page-body>
</template>

<script>
import CreatePageBody from "@/components/Graph/GraphMenu/Create/Modules/CreatePageBody"
import SelectorObject from "@/components/Graph/GraphMenu/Create/Headers/SelectorObject"
import RecordArea from "@/components/Graph/GraphMenu/Create/Record/RecordArea"
import ControlMenu from "@/components/Graph/GraphMenu/Create/Modules/ControlMenu"
import {mapActions, mapGetters} from "vuex"

export default {
  name: "CreateObjectPage",
  components: {CreatePageBody, ControlMenu, RecordArea, SelectorObject},
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
          title: 'Очистить',
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
        if(this.editableObjects) return this.editableObjects[0].ids.object_id },
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
    ...mapActions(['addNewParamEditableObject', 'deleteNewParamEditableObject', 'saveEditableObject', 'setEditableObject']),
    tabColor(key) {
      return key ? '#FF0000' : '#009688'
    },
    saveObject () {
      if(this.$refs['form' + this.activeTab][0].validate())
        this.saveEditableObject(this.activeTab)
    },
    recreateObject() {
      this.selectedEditableObject = this.selectedEditableObject
    },
    createNewParam(event) {
      this.addNewParamEditableObject({id: event, position: this.activeTab})
    },
    deleteNewParam(event) {
      this.deleteNewParamEditableObject({param: event.param, id: event.id, position: this.activeTab})
    },
    tabStatus(objects) {
      this.$nextTick(() => {
        this.$el.querySelector('#tabs > .v-item-group').style.display = objects.length <= 1 ? 'none' : 'flex'
      })

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
  height: calc(100% - 44px);
  overflow-y: auto;
  overflow-x: hidden;
}
.selector-object {
  height: 44px;
}
.height-with-tabs, .height-without-tabs  {
  max-height: calc(100% - 44px);
}
.control-menu {
  height: 44px;
  align-items: flex-end;
}
.height-with-tabs >>> .v-tab, .height-without-tabs >>> .v-tab {
  min-height: 48px;
}
.height-with-tabs >>> .v-tabs-items, .height-without-tabs >>> .v-tabs-items {
  overflow-y: auto;
}
.height-with-tabs >>> .v-tabs-items {
 max-height: calc(100% - 44px - 48px);
}
.height-without-tabs >>> .v-tabs-items {
  max-height: calc(100% - 44px);
}
.height-with-tabs >>> .v-slide-group__wrapper, .height-without-tabs  >>> .v-slide-group__wrapper {
  overflow-y: auto;
}
.conflict-title {
  color: #FF0000;
  white-space: nowrap;
}
</style>