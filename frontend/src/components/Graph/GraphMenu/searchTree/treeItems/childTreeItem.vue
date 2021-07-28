<template>
  <body-input-tree-item
    v-model="object.request"
    :hover="hover"
    @changeHover="changeHover"
  >
    <template v-slot:message>
      <tree-item-info :object="object"></tree-item-info>
    </template>
    <template v-slot:append>
      <div v-show="hover">
        <change-tree-item-btn
          :object="object"
          :parent-object="parentObject"
          @change="changeChildObject"
        ></change-tree-item-btn>
        <create-tree-item-btn
          :object="object"
          @create="createNewObject"
        ></create-tree-item-btn>
        <delete-tree-item-btn
          @deleteChildObject="deleteChildObject"
        ></delete-tree-item-btn>
      </div>
    </template>
  </body-input-tree-item>
</template>

<script>
import mixinTreeItems from "./mixinTreeItems"

export default {
  name: "childTreeItem",
  mixins: [ mixinTreeItems, ],
  props: {
    parentObject: Object,
  },
  methods: {
    createNewObject(newObject) {
      this.$emit('createNewObject', newObject)
    },
    changeChildObject(newData) {
      this.$emit('changeChildObject', newData)
    },
    deleteChildObject() {
      this.$emit('deleteChildObject')
    }
  }
}
</script>

<style scoped>

</style>