<template>
  <v-card>
    <v-card-title class="headline justify-center">
      При создании объекта {{ primaryObject(activeObject.object_id).title_single }} возник конфликт!
    </v-card-title>
    <v-divider></v-divider>
    <v-row no-gutters>
      <v-col>
        <v-tabs vertical color="teal">
          <v-tab v-for="(object, key) in conflictingObjects" :key="object.rec_id">
            <v-icon left>
              {{primaryObject(activeObject.object_id).icon}}
            </v-icon>
            - {{key}}
          </v-tab>
          <v-tab-item v-for="object in conflictingObjects" :key="object.rec_id" style="border-left: 1px solid rgba(0, 0, 0, 0.12)">
            <v-card flat class="pl-2">
              <v-card-title class="headline justify-center">
                Возможные объекты
              </v-card-title>
              <v-card-text class="px-0">
                <form-show-find-objects :object="object"></form-show-find-objects>
              </v-card-text>
              <v-card-actions class="justify-end pt-0">
                <v-btn outlined color="teal">Выбрать</v-btn>
              </v-card-actions>
            </v-card>
          </v-tab-item>
        </v-tabs>
      </v-col>
      <v-divider vertical class="mx-2"></v-divider>
      <v-col style=" display: flex; flex-direction: column;">
        <v-card flat height="100%">
          <v-card-title class="headline justify-center">
            Объект, который вы пытаетесь создать
          </v-card-title>
          <v-card-text>
            <v-textarea
                v-for="(classifier, key) in activeObject.params" :key="key"
                v-model="classifier.value"
                :label="getClassifier(activeObject.object_id, classifier.id).title"
                readonly hide-details rows="1" auto-grow color="teal" class="py-2"
            ></v-textarea>
          </v-card-text>
          <v-card-actions class="justify-start pt-0">
            <v-btn outlined color="teal">Выбрать</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import { mapGetters } from "vuex"
import formShowFindObjects from '../searchTree/formShowFindObjects'

export default {
  name: "conflictForm",
  props: {
    conflictingObjects: Array,
  },
  components: { formShowFindObjects, },
  computed: {
    ...mapGetters(['activeObject', 'primaryObject', 'listOfClassifiersOfObjects', ]),
  },
  methods: {
    getClassifier(objectId, classifierId) {
      return this.listOfClassifiersOfObjects(objectId).find(classifier => classifier.id === classifierId)
    },
    getClassifierHint(objectId, classifierId) {
      let classifier =  this.getClassifier(objectId, classifierId)
      return classifier.hint ?  classifier.hint : 'Описание отсутствует'
    },
  },
}
</script>

<style scoped>

</style>