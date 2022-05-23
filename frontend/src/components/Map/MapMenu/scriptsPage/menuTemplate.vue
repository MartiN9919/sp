<template>
  <v-combobox
      v-model="selected"
      :search-input.sync="search"
      :items="templates"
      :placeholder="inputLabel"
      :rules="rules"
      :hide-details="!errorMessage.length"
      :error-messages="errorMessage"
      dense
      required
      solo
      ref="form"
      color="teal"
      autocomplete="off"
      item-text="title"
      item-color="teal"
  >
    <template v-slot:label>
    </template>
    <template v-slot:append>
      <v-menu offset-x z-index="10001" max-height="50%" close-on-content-click>
        <template v-slot:activator="{ on, value }">
          <v-btn icon v-on="on" @mouseup.stop>
            <v-icon :color="iconColor(value)">mdi-cog-outline</v-icon>
          </v-btn>
        </template>
        <v-list rounded dense>
          <v-list-item @click="create">
            <v-list-item-icon>
              <v-icon>mdi-filter-variant-plus</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Создать новый</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item @click="put">
            <v-list-item-icon>
              <v-icon>mdi-content-save-edit-outline</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Изменить</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item @click="save">
            <v-list-item-icon>
              <v-icon>mdi-content-save-outline</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Сохранить</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item @click.stop="removeDialog">
            <v-list-item-icon>
              <v-icon>mdi-delete-outline</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Удалить</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-dialog v-model="dialogDeleteStatus" persistent max-width="460">
            <v-card>
              <v-card-title class="headline text-no-wrap select-off">
                Вы согласны с удалением шаблона?
              </v-card-title>
              <v-card-actions>
                <v-btn color="#00796B" text @click="dialogDeleteStatus = false">Отменить</v-btn>
                <v-spacer></v-spacer>
                <v-btn color="#00796B" text @click="remove">Подтвердить</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <v-divider/>
          <v-list-item @click.stop="isSaveLast = !isSaveLast">
            <v-list-item-content>
              <v-list-item-title>Запоминать выбор</v-list-item-title>
            </v-list-item-content>
            <v-list-item-action>
              <v-switch v-model="isSaveLast" color="teal" readonly></v-switch>
            </v-list-item-action>
          </v-list-item>
        </v-list>
      </v-menu>
    </template>
    <template v-slot:item="{item}">
      <v-list-item-title class="selector-item">{{item.title}}</v-list-item-title>
    </template>
  </v-combobox>
</template>

<script>
import DropDownMenu from "@/components/WebsiteShell/CustomComponents/dropDownMenu"

export default {
  name: 'menuTemplate',
  components: {DropDownMenu},
  data: () => ({
    dialogDeleteStatus: false,
    errorMessage: '',
    search: ''
  }),
  props: {
    templates: Array,
    selectedTemplate: Object
  },
  computed: {
    selected: {
      get: function () {
        return this.selectedTemplate.title.length ? this.selectedTemplate : null
      },
      set: function (template) {
        if(template.hasOwnProperty('id')) {
          this.get(template.id)
        }
      }
    },
    isSaveLast: {
      get: function () {
        return this.$store.getters.lastTemplateStatus
      },
      set: function (value) {
        this.$store.dispatch('changeLastTemplateStatus', value)
      }
    },
    rules: function () {
      return [this.search ? !!this.search.length : false, !!this.analystsListLength]
    },
    inputLabel: function () {
      return this.analystsListLength ? 'Введите название шаблона' : 'Шаблон'
    },
    analystsListLength: function () {
      return this.selectedTemplate.activeAnalysts.concat(this.selectedTemplate.passiveAnalysts).length
    }
  },
  methods: {
    iconColor (status) {
      return status ? '#00796B' : ''
    },
    get (id) {
      this.errorMessage = ''
      this.$emit('get', { params: { template_id: id } })
    },
    create () {
      this.errorMessage = ''
      this.$emit('create')
    },
    validate () {
      if (!this.$refs.form.rules[0]) {
        this.errorMessage = 'Заполните имя шаблона'
        return false
      } else if (!this.$refs.form.rules[1]) {
        this.errorMessage = 'Выберете скрипты'
        return false
      } else if (this.$refs.form.validate()) {
        this.errorMessage = ''
        return true
      }
    },
    put () {
      if (this.templates.find(t => t.title === this.search && t.id === this.selectedTemplate.id)) {
        this.errorMessage = 'Имя должно быть уникально'
        return false
      } else {
        if (this.validate()) {
          this.$emit('put', this.search)
        }
      }
    },
    save () {
      if (this.templates.find(t => t.title === this.search)) {
        this.errorMessage = 'Имя должно быть уникально'
        return false
      } else {
        if (this.validate()) {
          this.$emit('save', this.search)
        }
      }
    },
    removeDialog() {
      if(this.selected) {
        this.dialogDeleteStatus = true
      } else {
        this.errorMessage = 'Выберите шаблон, который хотите удалить'
      }
    },
    remove () {
      this.errorMessage = ''
      this.dialogDeleteStatus = false
      this.$emit('remove', {params: {template_id: this.selectedTemplate.id}})
    }
  }
}
</script>

<style scoped>
.v-text-field.v-text-field--enclosed >>> .v-text-field__details {
  margin-bottom: 0;
}
.selector-item {
  white-space: normal;
  width: 0;
}
</style>
