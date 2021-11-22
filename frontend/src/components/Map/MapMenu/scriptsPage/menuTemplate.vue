<template>
  <div>
    <drop-down-menu offset-y :disabled="!templates.length" max-height="50%" min-width="95%" max-width="95%" attach>
      <template v-slot:activator="{ on, value }">
        <v-text-field
          autocomplete="off" ref="form"
          v-model="templateTitle" :label="inputLabel"
          :rules="[!!templateTitle.length, !!analystsListLength]"
          :hide-details="!errorMessage.length"
          :messages="errorMessage"
          dense required solo
          color="teal"
        >
          <template slot="append">
            <v-btn icon v-on="on">
              <v-icon :color="iconColor(value)">mdi-menu-down-outline</v-icon>
            </v-btn>
            <v-menu offset-x z-index="10001" max-height="50%">
              <template v-slot:activator="{ on, value }">
                <v-btn icon v-on="on">
                  <v-icon :color="iconColor(value)">mdi-cog-outline</v-icon>
                </v-btn>
              </template>
              <v-list rounded>
                <v-list-item @click="createNewTemplate()">
                  <v-list-item-icon>
                    <v-icon>mdi-filter-variant-plus</v-icon>
                  </v-list-item-icon>
                  <v-list-item-title>Создать новый шаблон</v-list-item-title>
                </v-list-item>
                <v-list-item @click="saveTemplate">
                  <v-list-item-icon>
                    <v-icon>mdi-content-save-outline</v-icon>
                  </v-list-item-icon>
                  <v-list-item-title>Сохранить шаблон</v-list-item-title>
                </v-list-item>
                <v-dialog v-if="'id' in selectedTemplate" v-model="dialogDeleteStatus" persistent max-width="460">
                  <template v-slot:activator="{ on }">
                    <v-list-item v-on="on">
                      <v-list-item-icon>
                        <v-icon>mdi-delete-outline</v-icon>
                      </v-list-item-icon>
                      <v-list-item-title>Удалить шаблон</v-list-item-title>
                    </v-list-item>
                  </template>
                  <v-card>
                    <v-card-title class="headline select_off">
                      Вы согласны с удалением шаблона?
                    </v-card-title>
                    <v-card-actions>
                      <v-btn color="#00796B" text @click="dialogDeleteStatus = false">Отменить</v-btn>
                      <v-spacer></v-spacer>
                      <v-btn color="#00796B" text @click="deleteTemplate">Подтвердить</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </v-list>
            </v-menu>
          </template>
        </v-text-field>
      </template>
      <template v-slot:body="{ closeMenu, status }">
        <v-list v-if="status" rounded>
          <v-list-item
            v-for="temp in templates" :key="temp.id"
            :disabled="temp.id === parseInt(selectedTemplate.id)"
            @click="getTemplate(temp.id)"
          >
            <v-list-item-title>{{temp.title}}</v-list-item-title>
          </v-list-item>
        </v-list>
      </template>
    </drop-down-menu>
  </div>
</template>

<script>
import DropDownMenu from "@/components/WebsiteShell/CustomComponents/dropDownMenu"

export default {
  name: 'menuTemplate',
  components: {DropDownMenu},
  data: () => ({
    dialogDeleteStatus: false,
    errorMessage: ''
  }),
  props: {
    templates: Array,
    selectedTemplate: Object
  },
  computed: {
    templateTitle: {
      get: function () { return this.selectedTemplate.title },
      set: function (title) { this.$emit('changeTitle', title) }
    },
    inputLabel: function () { return this.analystsListLength ? 'Введите название шаблона' : 'Шаблон' },
    analystsListLength: function () {
      return this.selectedTemplate.activeAnalysts.concat(
          this.selectedTemplate.passiveAnalysts).length
    }
  },
  methods: {
    iconColor (status) {
      return status ? '#00796B' : ''
    },
    getTemplate (id) {
      this.errorMessage = ''
      this.$emit('getTemplate', id)
    },
    createNewTemplate () {
      this.errorMessage = ''
      this.$emit('createNewTemplate')
    },
    saveTemplate () {
      if (this.$refs.form.validate()) {
        this.$emit('saveTemplate')
        this.errorMessage = ''
      } else if (!this.$refs.form.rules[0]) this.errorMessage = 'Заполните имя шаблона'
      else if (!this.$refs.form.rules[1]) this.errorMessage = 'Выберете скрипты'
    },
    deleteTemplate () {
      this.errorMessage = ''
      this.dialogDeleteStatus = false
      this.$emit('deleteTemplate', { params: { template_id: this.selectedTemplate.id } })
    }
  }
}
</script>

<style scoped>
.v-text-field.v-text-field--enclosed >>> .v-text-field__details {
  margin-bottom: 0;
}
</style>
