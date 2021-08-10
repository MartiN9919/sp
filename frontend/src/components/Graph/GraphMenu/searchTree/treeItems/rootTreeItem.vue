<template>
  <body-input-tree-item
    v-model="object.request"
    :hover="hover"
    @changeHover="changeHover"
  >
    <template v-slot:append-outer>
      <slot name="append-outer"></slot>
    </template>
    <template v-slot:message>
      <tree-item-info :object="object"></tree-item-info>
    </template>
    <template v-slot:append>
      <div v-show="hover">
        <change-tree-item-btn
          :object="object"
          @change="changeRootObject"
        ></change-tree-item-btn>
        <create-tree-item-btn
          :object="object"
          @create="createNewObject"
        ></create-tree-item-btn>
      </div>
    </template>
  </body-input-tree-item>
</template>

<script>
import mixinTreeItems from "./mixinTreeItems"

export default {
  name: "rootTreeItem",
  mixins: [ mixinTreeItems, ],
  methods: {
    createNewObject(newObject) {
      this.$emit('createNewObject', newObject)
    },
    changeRootObject(newData) {
      this.$emit('changeRootObject', newData)
    },
  },
}
</script>

<style scoped>

</style>