<template>
  <v-autocomplete
      ref="ser"
      v-model="value"
      :search-input.sync="searchString"
      no-filter
      @keyup.enter="search"
      v-bind="$attrs"
      :items="findObjects || []"
      :class="bodyInputClasses"
      :placeholder="$attrs.placeholder || 'Выберите объект'"
      dense
      color="teal"
      item-color="teal"
      item-text="title"
      item-value="recId"
      hide-no-data
      autocomplete="off"
      messages=" "
      class="search-input-form"
      :menu-props="{closeOnContentClick: true}"
  >
    <template v-slot:message>
      <slot name="message"></slot>
    </template>
    <template v-slot:append>
      <v-hover v-slot="{ hover }" class="action-icon">
        <v-icon
            v-if="$attrs.hasOwnProperty('deletable') && hover"
            @click.stop="$emit('deletable')"
            @mouseup.stop
            size="24"
            class="action-icon"
        >mdi-delete</v-icon>
        <v-icon v-else-if="searchString" @click="search" @mouseup.stop>mdi-magnify</v-icon>
        <v-icon v-else-if="$attrs['type-load']">{{baseObject(selectorObject).icon}}</v-icon>
        <drop-down-menu v-else min-width="auto" max-height="30%" z-index="100000" offset-y close-on-click>
          <template v-slot:activator="{ on }">
            <v-icon v-on="on" @mouseup.stop>{{baseObject(selectorObject).icon}}</v-icon>
          </template>
          <template v-slot:body>
            <v-list dense>
              <v-list-item v-for="object in baseObjects" :key="object.id" @click="selectorObject = object.id">
                <v-list-item-icon>
                  <v-icon>{{object.icon}}</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>
                    {{object.title}}
                  </v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </template>
        </drop-down-menu>
      </v-hover>
    </template>
    <template v-slot:item="{item}">
      <v-list-item @click="value=item" class="my-2">
        <v-list-item-subtitle style="white-space: normal; width: 0">
          {{item.title}}
        </v-list-item-subtitle>
      </v-list-item>
    </template>
  </v-autocomplete>
</template>

<script>
import DropDownMenu from "@/components/WebsiteShell/CustomComponents/dropDownMenu"
import BodyInputForm from "@/components/WebsiteShell/CustomComponents/bodyInputForm"
import {mapActions, mapGetters} from "vuex"

export default {
name: "searchInput",
  components: {BodyInputForm, DropDownMenu},
  model: { prop: 'inputString', event: 'changeInputString'},
  props: {
    inputString: Object,
  },
  data: () => ({
    selectorObject: null,
    searchString: '',
    findObjects: []
  }),
  computed: {
  ...mapGetters(['baseObject', 'baseObjects']),
    bodyInputClasses: function () { return this.$attrs.hasOwnProperty('label') ? 'pt-2' : '' },
    value: {
      get: function () { return this.inputString},
      set: function (value) {this.$emit('changeInputString', value)},
    },
  },
  methods: {
    ...mapActions(['simpleFindObject']),
    search() {
      this.simpleFindObject({objectId: this.selectorObject, searchRequest: this.searchString})
      .then(response => {
        this.findObjects = response.data.map(i => {
          return {objectId: i.object_id, recId: i.rec_id, title: i.title}
        })
      })
    }
  },
  created() {
    if(this.inputString) {
      this.findObjects.push(this.inputString)
    }
    this.selectorObject = this.$attrs['type-load'] || this.baseObjects[0].id
  }
}
</script>

<style scoped>
.v-text-field {
  margin-top: 0;
  padding-top: 12px;
}
.search-input-form >>> input {
  padding: 0;
}
.search-input-form >>> .v-input__slot {
  align-items: flex-end;
  margin-bottom: 0;
}
.search-input-form >>> .v-input__append-inner {
  margin-top: 0 !important;
}
.search-input-form >>> .v-messages {
  min-height: 0;
}
.search-input-form >>> .v-text-field__details {
  min-height: 0;
}
.search-input-form >>> .v-select__slot {
  cursor: pointer;
}
</style>