<template>
  <v-menu offset-y :disabled="!templates.length" max-height="50%" z-index="10001">
    <template v-slot:activator="{ on, attrs }">
      <v-row dense no-gutters class="pa-4 pr-2 pb-2 pt-2 noselect">
        <v-text-field
          ref="form"
          v-model="templateTitle"
          :label="inputLabel"
          :rules="[templateTitle.length !== 0, analystsListLength !== 0]"
          :error-messages="errorMessage"
          dense required
          single-line
          color="teal"
          class="pa-0 mt-0"
        >
          <template slot="append-outer">
            <v-btn icon v-bind="attrs" v-on="on">
              <v-icon :color="attrs['aria-expanded'] === 'true' ? 'teal' : ''">mdi-menu-down-outline</v-icon>
            </v-btn>
            <v-menu offset-x z-index="10001" max-height="50%">
              <template v-slot:activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" v-on="on">
                  <v-icon :color="attrs['aria-expanded'] === 'true' ? 'teal' : ''">mdi-cog-outline</v-icon>
                </v-btn>
              </template>
              <v-list oncontextmenu="return false" rounded>
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
                  <template v-slot:activator="{ on, attrs }">
                    <v-list-item  v-bind="attrs" v-on="on">
                      <v-list-item-icon>
                        <v-icon>mdi-delete-outline</v-icon>
                      </v-list-item-icon>
                      <v-list-item-title>Удалить шаблон</v-list-item-title>
                    </v-list-item>
                  </template>
                  <v-card>
                    <v-card-title class="headline noselect">
                      Вы согласны с удалением шаблона?
                    </v-card-title>
                    <v-card-actions>
                      <v-btn color="teal" text @click="dialogDeleteStatus = false">
                        Отменить
                      </v-btn>
                      <v-spacer></v-spacer>
                      <v-btn color="teal" text @click="deleteTemplate">
                        Подтвердить
                      </v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </v-list>
            </v-menu>
          </template>
        </v-text-field>
      </v-row>
    </template>

    <v-list oncontextmenu="return false" rounded>
      <v-list-item
        v-for="temp in templates"
        :disabled="temp.id === parseInt(selectedTemplate.id)"
        @click="getTemplate(temp.id)"
        link
      >
        <v-list-item-title>{{temp.title}}</v-list-item-title>
      </v-list-item>
    </v-list>

  </v-menu>
</template>

<script>
import '@/assets/css/noselect.css'

export default {
  name: 'menuTemplate',
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
    inputLabel: function () { return this.analystsListLength ? 'Введите название шаблона' : 'Меню шаблонов' },
    analystsListLength: function () {
      return this.selectedTemplate.activeAnalysts.concat(
        this.selectedTemplate.passiveAnalysts).length
    }
  },
  methods: {
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

</style>
