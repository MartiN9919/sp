<template>
  <foreignObject
      :id="data.id"
      :x="data.x"
      :y="data.y"
      :width="1"
      :height="1"
      overflow="visible"
      @mousedown="onMousedown"
    >
      <div class="content" ref="content">
        <slot>{{ data.id }}</slot>
      </div>
  </foreignObject>
</template>

<script>
import dragMixin from '../mixins/drag'

export default {
  mixins: [dragMixin],
  props: {
    data: {},
  },
  mounted () {
    this.fitContent()
    this.$on('drag', ({ x, y }) => {
      if(this.data.hasOwnProperty('size')){
        this.data.x += x
        this.data.y += y
      }
    })
  },
  methods: {
    fitContent () {
      this.data.width = this.$refs.content.clientWidth
      this.data.height = this.$refs.content.clientHeight
    },
    onMousedown (e) {
      e.stopPropagation()
      this.startDrag(e);
    }
  },
}
</script>

<style>
.content {
  background-color: white;
  border-radius: 100%;
  position: initial;
  white-space: nowrap;
  width: fit-content;
}
</style>