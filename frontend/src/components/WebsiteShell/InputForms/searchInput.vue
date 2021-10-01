<template>
  <div class="search-input-form">
    <drop-down-menu
      min-width="96%"
      max-width="96%"
      max-height="40%"
      nudge-bottom="5"
      attach offset-y
      :close-on-content-click="false"
    >
      <template v-slot:activator="{ on }">
        <div v-on="on" class="main-input">
          <body-input-form
            v-model="value"
            v-bind="$attrs"
            :class="bodyInputClasses"
            :icon="baseObject(selectorObject).icon"
            :placeholder="$attrs.placeholder || 'Выберете необходимую дату'"
            @deletable="$emit('deletable')"
            readonly
            clearable
          >
            <template v-slot:message>
              <slot name="message"></slot>
            </template>
          </body-input-form>
        </div>
      </template>
      <template v-slot:body="{ closeMenu,  status }">
        <v-list width="100%">
          <v-list-item style="max-height: 48px">
            <v-text-field v-model="searchString" dense color="teal" hide-details autocomplete="off">
              <template v-slot:append>
                <v-btn icon small @click="search">
                  <v-icon>mdi-magnify</v-icon>
                </v-btn>
              </template>
              <template v-slot:prepend-inner>
                <v-icon v-if="$attrs['type-load']">{{baseObject(selectorObject).icon}}</v-icon>
                <drop-down-menu v-else min-width="auto" max-height="40%" offset-y close-on-click>
                  <template v-slot:activator="{ on }">
                    <v-icon v-on="on">{{baseObject(selectorObject).icon}}</v-icon>
                  </template>
                  <template v-slot:body>
                    <v-list>
                      <v-list-item v-for="object in baseObjects" :key="object.id" @click="selectorObject = object.id">
                        <v-list-item-icon><v-icon>{{object.icon}}</v-icon></v-list-item-icon>
                        <v-list-item-subtitle>
                          {{object.title}}
                        </v-list-item-subtitle>
                      </v-list-item>
                    </v-list>
                  </template>
                </drop-down-menu>
              </template>
            </v-text-field>
          </v-list-item>
          <div class="scroll-content">
            <v-list-item v-for="object in findObjects" :key="object.rec_id" @click="value=object; closeMenu()">
              <v-list-item-subtitle style="white-space: normal">
                {{object.title}}
              </v-list-item-subtitle>
            </v-list-item>
          </div>
        </v-list>
      </template>
    </drop-down-menu>
  </div>
</template>

<script>
import DropDownMenu from "@/components/WebsiteShell/UI/dropDownMenu"
import BodyInputForm from "@/components/WebsiteShell/UI/bodyInputForm"
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
    bodyInputClasses: function () { return this.$attrs.hasOwnProperty('label') ? '' : 'pt-0' },
    value: {
      get: function () { return this.inputString ? this.inputString.title : '' },
      set: function (value) { this.$emit('changeInputString', {
        objectId: value.object_id, recId: value.rec_id, title: value.title
      }) },
    },
  },
  methods: {
    ...mapActions(['simpleFindObject']),
    search() {
      this.simpleFindObject({objectId: this.selectorObject, searchRequest: this.searchString})
      .then(response => { this.findObjects = response.data })
    }
  },
  created() {
    this.selectorObject = this.$attrs['type-load'] || this.baseObjects[0].id
  }
}
</script>

<style scoped>
.search-input-form >>> .v-menu__content {
  display: flex;
  overflow: hidden;
}
.scroll-content {
  overflow: auto;
  height: calc(100% - 48px);
}
.search-input-form >>> .v-input__append-outer {
  margin: 0 0 0 8px;
}
.main-input >>> input {
  cursor: pointer;
}
.main-input >>> .v-input__slot {
  cursor: pointer;
}
.main-input {
  width: 100%;
}
</style>