<template>
  <div class="px-2 py-4" style="min-width: 400px">
    <v-autocomplete
        solo
        v-model="selectedEditableObject"
        :items="baseObjects"
        item-text="titleSingle"
        item-value="id"
        item-color="teal"
        color="teal"
        label="Выберете объект"
        hide-details
        class="mb-2"
    ></v-autocomplete>
    <v-card class="mb-2">
      <v-row no-gutters align="center">
        <v-col>
          <v-card-title>Информация об объекте</v-card-title>
          <v-card-subtitle>Список старых значений объекта</v-card-subtitle>
        </v-col>
        <v-col cols="auto">
          <custom-tooltip bottom description="Добавить на граф">
            <template v-slot:activator="{on}">
              <v-btn v-on="on" icon color="success">
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </template>
          </custom-tooltip>
          <custom-tooltip bottom description="Отменить изменение">
            <template v-slot:activator="{on}">
              <v-btn v-on="on" icon color="error">
                <v-icon>mdi-close</v-icon>
              </v-btn>
            </template>
          </custom-tooltip>
        </v-col>
      </v-row>
      <v-card-text>
        <v-row no-gutters>
          <v-col cols="3">
            <div>ФИО</div>
          </v-col>
          <v-col>
            <div>Стасюк Кирилл Андреевич</div>
            <div>Бурень Максим Николаевич</div>
          </v-col>
          <v-col cols="auto">
            <div>23.06.2022 16:10</div>
            <div>23.06.2022 16:10</div>
          </v-col>
        </v-row>
        <v-divider></v-divider>
        <v-row no-gutters>
          <v-col cols="3">
            <div>Дата рождения</div>
          </v-col>
          <v-col>
            <div>13.08.1998</div>
            <div>24.09.1965</div>
          </v-col>
          <v-col cols="auto">
            <div>23.06.2022 16:10</div>
            <div>23.06.2022 16:10</div>
          </v-col>
        </v-row>
        <v-divider></v-divider>
        <v-row no-gutters>
          <v-col cols="3">
            <div>Пол</div>
          </v-col>
          <v-col>
            <div>Мужской</div>
          </v-col>
          <v-col cols="auto">
            <div>23.06.2022 16:10</div>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
    <v-card class="mb-2">
      <v-row no-gutters align="center">
        <v-col>
          <v-card-title>Внесение информации</v-card-title>
          <v-card-subtitle>Внесение значений полей для Физлицо</v-card-subtitle>
        </v-col>
        <v-col cols="auto">
          <v-btn-toggle dense group>
            <custom-tooltip bottom description="Добавить">
              <template v-slot:activator="{on}">
                <v-btn v-on="on" :value="1" text color="success">
                  <v-icon>mdi-plus</v-icon>
                </v-btn>
              </template>
            </custom-tooltip>
            <custom-tooltip bottom description="Очистить">
              <template v-slot:activator="{on}">
                <v-btn v-on="on" :value="2" text color="warning">
                  <v-icon>mdi-filter-remove-outline</v-icon>
                </v-btn>
              </template>
            </custom-tooltip>
            <custom-tooltip bottom description="Удалить">
              <template v-slot:activator="{on}">
                <v-btn v-on="on" :value="3" text color="error">
                  <v-icon>mdi-delete-outline</v-icon>
                </v-btn>
              </template>
            </custom-tooltip>
          </v-btn-toggle>
        </v-col>
      </v-row>
      <v-divider/>

      <v-card-text>
        <v-row no-gutters>
          <v-col>
            <v-text-field
                dense
                persistent-placeholder
                autofocus
                outlined
                color="teal"
                label="ФИО"
                placeholder="Фамилия Имя Отчество"
                messages="Введите данные в формате: 'Фамилия Имя Отчество'"
                counter
                maxlength="255"
                append-icon="mdi-format-color-text"
            ></v-text-field>
          </v-col>
          <v-col style="max-width: 150px" class="pl-1">
            <v-text-field
                tabindex="-1"
                value="23.06.2022 16:41"
                dense
                outlined
                color="teal"
                reverse
                label="Дата установки"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row no-gutters>
          <v-col>
            <v-text-field
                dense
                persistent-placeholder
                outlined
                color="teal"
                label="Дата рождения"
                placeholder="**.**.****"
                messages="Введите данные в формате: 'День.Месяц.Год'"
                counter
                maxlength="10"
                append-icon="mdi-calendar"
            ></v-text-field>
          </v-col>
          <v-col style="max-width: 150px" class="pl-1">
            <v-text-field
                tabindex="-1"
                value="23.06.2022 16:41"
                dense
                outlined
                color="teal"
                reverse
                label="Дата установки"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row no-gutters>
          <v-col>
            <v-autocomplete
                :items="['Мужчина', 'Женщина']"
                item-color="teal"
                dense
                persistent-placeholder
                outlined
                color="teal"
                label="Пол"
                placeholder="Необходимо выбрать значение"
                messages="Выберете значения из списка"
                append-icon="mdi-format-list-bulleted"
            ></v-autocomplete>
          </v-col>
          <v-col style="max-width: 150px" class="pl-1">
            <v-text-field
                tabindex="-1"
                value="23.06.2022 16:41"
                dense
                outlined
                color="teal"
                reverse
                label="Дата установки"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row no-gutters>
          <v-col>
            <v-autocomplete
                :items="['Белорус', 'Русский', 'Румын', 'Иранец', 'Македонец']"
                item-color="teal"
                dense
                persistent-placeholder
                outlined
                color="teal"
                label="Национальность"
                placeholder="Необходимо выбрать значение"
                messages="Выберете значения из списка"
                append-icon="mdi-format-list-bulleted"
            ></v-autocomplete>
          </v-col>
          <v-col style="max-width: 150px" class="pl-1">
            <v-text-field
                tabindex="-1"
                value="23.06.2022 16:41"
                dense
                outlined
                color="teal"
                reverse
                label="Дата установки"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row no-gutters>
          <v-col>
            <v-file-input
                dense
                persistent-placeholder
                outlined
                color="teal"
                label="Фото"
                placeholder="Выберете необходимые фотографии"
                messages="Данные фото будут являться основными фото физлица"
                append-icon="mdi-file"
                prepend-icon=""
                multiple
            ></v-file-input>
          </v-col>
          <v-col style="max-width: 150px" class="pl-1">
            <v-text-field
                tabindex="-1"
                value="23.06.2022 16:41"
                dense
                outlined
                color="teal"
                reverse
                label="Дата установки"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row no-gutters>
          <v-col>
            <v-textarea
                dense
                persistent-placeholder
                outlined
                color="teal"
                label="Дополнительные данные"
                placeholder="Введите текст неограниченной длинны"
                messages="Дополнительная информация о физлице"
                append-icon="mdi-text-long"
            ></v-textarea>
          </v-col>
          <v-col style="max-width: 150px" class="pl-1">
            <v-text-field
                tabindex="-1"
                value="23.06.2022 16:41"
                dense
                outlined
                color="teal"
                reverse
                label="Дата установки"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import CustomTooltip from "@/components/WebsiteShell/CustomComponents/Tooltip/customTooltip"
import {mapActions, mapGetters} from "vuex"

export default {
  name: "CreateObjectPageAlternative",
  components: {CustomTooltip},
  computed: {
    ...mapGetters(['baseObjects']),
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
      'setEditableObject',
    ]),
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