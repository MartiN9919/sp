<template>
  <div tabindex="-1">
    <v-row
        @click="click"
        @keyup.enter.exact="status = !status"
        @keyup.ctrl.enter.exact="click"
        no-gutters
        :class="classes"
        class="select-off cursor-pointer flex-nowrap header"
        justify="space-between"
        align="center"
        tabindex="0"
    >
      <v-card-subtitle class="py-1">
        <slot name="title"></slot>
      </v-card-subtitle>
      <v-btn @click.stop="status = !status" icon :dark="status" tabindex="-1">
        <v-icon>{{ icon }}</v-icon>
      </v-btn>
    </v-row>
    <v-expand-transition>
      <div v-show="status">
        <slot name="body"></slot>
      </div>
    </v-expand-transition>
  </div>
</template>

<script>
export default {
  name: "RecordBody",
  model: {
    prop: 'opened',
    event: 'change'
  },
  props: {
    opened: Array
  },
  computed: {
    status: {
      get: function () {
        return this.opened.includes(this.$vnode.key)
      },
      set: function (value) {
        if(value) {
          this.opened.push(this.$vnode.key)
        } else {
          this.opened.splice(this.opened.findIndex(k => k === this.$vnode.key), 1)
        }
      }
    },
    classes: function () {
      return this.status ? 'open-header' : 'close-header'
    },
    icon: function () {
      return this.status ? 'mdi-chevron-up' : 'mdi-chevron-down'
    }
  },
  methods: {
    click(e) {
      this.$emit('click', this.$vnode.key)
    }
  }
}
</script>

<style scoped>
.close-header, .open-header {
  transition: all 0.2s;
  border-bottom: solid 1px darkgray;
}

.close-header {
  background-color: #efefef;
  color: black;
}
.close-header:hover {
  background-color: #dadada !important;
}
.close-header:focus {
  outline: none;
  background-color: #c2c2c2 !important;
}

.open-header {
  background-color: #c4c4c4;
  color: white;
}
.open-header:hover {
  background-color: #a6a6a6 !important;
}
.open-header:focus {
  outline: none;
  background-color: #939393 !important;
}
</style>