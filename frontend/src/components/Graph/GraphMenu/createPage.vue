<template>
  <v-col>
    <div class="work-place">
      <selector-object
        v-model="selectedEditableObject"
        :items="listOfPrimaryObjects"
        class="selector-object py-2"
      ></selector-object>
      <span v-if="conflictStatus" class="px-2 conflict-title">Схожие объекты</span>
      <v-tabs v-model="activeTab" :color="sliderColor" grow class="object-record-area">
        <v-tab v-for="(object, key) in editableObjects" :key="key">
          <v-icon :color="tabColor(key)">{{ primaryObject(object.object_id).icon }}</v-icon>
          <span :style="{color: tabColor(key)}">{{key + 1}}</span>
        </v-tab>
        <v-tab-item v-for="(object, key) in editableObjects" :key="key" eager>
          <v-form ref="form" v-model="valid">
            <object-record-area
              :object-id="object.object_id"
              :classifiers="object.params"
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
    ...mapGetters(['primaryObject', 'listOfPrimaryObjects', 'editableObjects']),
    conflictStatus: function () { if(this.editableObjects) return this.editableObjects.length > 1 },
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
          title: this.editableObjects[this.activeTab]?.rec_id ? 'Сохранить' : 'Создать',
          action: 'save',
          disabled: !!(
            this.valid
            && this.editableObjects[this.activeTab]
            && 'form' in this.$refs
            && this.$refs.form[0].inputs.length
          )
        },
      ]
    },
    selectedEditableObject: {
      get: function () {
        if(this.editableObjects)
          return this.primaryObject(this.editableObjects[0].object_id)
      },
      set: function (object) {
        this.getListOfClassifiersOfObjects({params: {object_id: object.id}})
          .then(() => { this.setEditableObject({object_id: object.id}) })
      },
    },
  },
  methods: {
    ...mapActions(['getListOfClassifiersOfObjects', 'addNewParamEditableObject', 'deleteNewParamEditableObject',
      'saveEditableObject', 'setEditableObject', ]),
    tabColor(key) {
      return key ? '#FF0000' : '#009688'
    },
    saveObject () {
      if(this.$refs.form[0].validate())
        this.saveEditableObject({
          object: this.editableObjects[this.activeTab],
          force: this.conflictStatus,
        })
    },
    createNewParam(event) {
      this.addNewParamEditableObject({
        classifierId: event,
        positionEditableObject: this.activeTab
      })
    },
    deleteNewParam(event) {
      this.deleteNewParamEditableObject({
        param: event.param,
        classifierId: event.classifierId,
        positionEditableObject: this.activeTab
      })
    }
  },
  watch: {
    editableObjects: function (objects) {
      this.$el.querySelector('.object-record-area > .v-item-group').style.display = objects.length <= 1 ? 'none' : 'flex'
    },
  },
}
</script>

<style scoped>
.work-place {
  height: calc(100% - 3em);
}
.selector-object {
  height: 3.3em;
}
.object-record-area {
  max-height: calc(100% - 3.3em);
}
.control-menu {
  height: 3em;
  align-items: flex-end;
}
.object-record-area >>> .v-tab {
  min-height: 48px;
}
.object-record-area >>> .v-tabs-items {
  overflow-y: auto;
}
.object-record-area >>> .v-slide-group__wrapper {
  overflow-y: auto;
}
.conflict-title {
  color: #FF0000;
  white-space: nowrap;
}
</style>