<template>
  <create-page-body v-model="activeTab" :editable="editableObjects">
    <template v-slot:header>
      <selector-object v-model="selectedEditableObject" :items="baseObjects" class="selector-object">
        <template v-slot:prepend-inner>
          <v-btn small @click.stop="getFormFile" icon tabindex="-1">
            <v-icon>mdi-download</v-icon>
          </v-btn>
        </template>
      </selector-object>
    </template>
    <template v-slot:body>
      <v-tab-item v-for="(object, key) in editableObjects" :key="key" eager transition="none">
        <v-form :ref="'form' + key" v-model="valid" onSubmit="return false;" autofocus>
          <record-area
              conflict
              :params="object.params"
              :title="object.title"
              :settings="{objectId: object.ids.object_id, recId: object.ids.rec_id}"
          />
        </v-form>
      </v-tab-item>
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
import {DataBaseObject} from '@/store/modules/graph/general'

export default {
  name: "CreateObjectPage",
  components: {CreatePageBody, ControlMenu, RecordArea, SelectorObject},
  data: () => ({
    valid: false,
    activeTab: 0,
  }),
  computed: {
    ...mapGetters(['baseObjects', 'editableObjects', 'turnConflicts']),
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
          title: this.activeTab > 0 ? 'Объединить' : this.editableObjects[this.activeTab]?.recId ? 'Сохранить' : 'Создать',
          action: 'save',
          disabled: !!(
              (this.activeTab > 0 && this.valid) ||
              (this.valid
              && this.editableObjects[this.activeTab]
              && 'form' + this.activeTab in this.$refs
              && this.$refs['form' + this.activeTab][0]?.inputs?.length)
          )
        },
      ]
    },
    selectedEditableObject: {
      get: function () {
        if (this.editableObjects) return this.editableObjects[0].ids.object_id
      },
      set: function (id) {
        this.setEditableObject({object_id: id})
      },
    }
  },
  methods: {
    ...mapActions([
      'saveEditableObject',
      'setEditableObject',
      'addEditableObjects',
      'saveFormFile',
      'addResolvedConflict'
    ]),
    saveObject() {
      if (this.$refs['form' + this.activeTab][0].validate()) {
        if (this.turnConflicts) {
          this.addResolvedConflict(this.activeTab)
        } else {
          this.saveEditableObject(this.activeTab)
        }
        this.activeTab = 0
      }
    },
    recreateObject() {
      this.selectedEditableObject = this.selectedEditableObject
    },
    getFormFile() {
      const saveFormFile = this.saveFormFile
      let obj = document.createElement('input')
      obj.style.cssText = 'display:none'
      obj.type = 'file'
      obj.accept = '.docm'
      let input = document.getElementById("app").appendChild(obj)
      input.click()
      input.addEventListener('change', () => saveFormFile(input.files[0]))
      obj.remove()
    },
  },
  watch: {
    turnConflicts: function (conflicts) {
      if(conflicts && conflicts.length) {
        const conflict = conflicts[0]
        const db = new DataBaseObject({object_id: conflict.object.object_id})
        db.addNewValues(conflict.object.params)
        this.setEditableObject(db)
        this.addEditableObjects(conflict.objects)
      } else if(conflicts) {
        this.saveFormFile()
      }
    }
  }
}
</script>

<style scoped>
.selector-object {
  height: 44px;
}

.control-menu {
  height: 44px;
  align-items: flex-end;
}
</style>