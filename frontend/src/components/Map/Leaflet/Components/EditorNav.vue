<template>
  <div
    style="height:100%;"
  >
    <h1>555</h1>
    <h3>444555</h3>
  </div>
</template>

<script>

export default {
  name:       'EditorNav',
  data: () => ({
    drawer: true,
  }),
}

/*
  <v-treeview
    :items=treeViewItems :open.sync="listOpenFolder" @update:active="activateItem"
    return-object hoverable transition dense open-on-click activatable active-class="" color=""
  >
    <template v-slot:label="{ item, open }">
      <custom-tooltip>
        <template v-slot:activator="{ on }">
          <div v-on="on">
            <v-icon :id="iconId(item.id)" :color="colorIcon(item)">{{ typeIcon(item, open) }}</v-icon>
            <span :class="itemTextStyle(item.icon)" :style="itemTextColor(item)">{{ item.name }}</span>
          </div>
        </template>
        <template v-slot:body>
          <p class="text-justify ma-0">{{ checkHintInItem(item) }}</p>
        </template>
      </custom-tooltip>
    </template>
  </v-treeview>

*/

</script>