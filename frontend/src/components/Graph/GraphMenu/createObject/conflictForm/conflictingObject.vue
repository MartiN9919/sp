<template>
  <v-col>
    <v-card flat height="100%" style="display: flex; flex-direction: column; justify-content: space-between">
      <div style="height: calc(100% - 4em)">
        <v-card-title class="headline justify-center pt-2" style="height: 1.9em">
          <span class="text-no-wrap">
            Объект "{{$store.getters.primaryObject(object.object_id).title_single}}" №{{object.rec_id}}
          </span>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="px-3 overflow-y-auto" style="height: calc(100% - 2.7em)">
          <form-show-find-objects :object="object"></form-show-find-objects>
        </v-card-text>
      </div>
      <v-card-actions class="justify-end" style="height: 3.5em">
        <v-btn @click="$emit('saveObject', object)" outlined color="teal">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-col>
</template>

<script>
import formShowFindObjects from '../../foundObjects/formShowFindObjects'

export default {
  name: "conflictingObject",
  components: { formShowFindObjects, },
  props: {
    object: Object,
  }
}
</script>

<style scoped>

</style>