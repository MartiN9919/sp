<template>
  <foreignObject
    :x="data.x"
    :y="data.y"
    :width="1"
    :height="1"
    overflow="visible"
    @mousedown="onMousedown"
  >
    <div class="content" ref="content">
      <slot/>
    </div>
  </foreignObject>
</template>

<script>
import dragMixin from '../mixins/drag'

export default {
  mixins: [dragMixin],
  props: {
    data: {},
    inSelected: {
      type: Boolean,
      default: null
    },
    selectedObjects: {
      type: Array,
      default: null
    }
  },
  mounted () {
    this.fitContent()
  },
  methods: {
    fitContent () {
      if(this.data.hasOwnProperty('width') && this.data.hasOwnProperty('height')) {
        this.data.width = this.$refs.content.clientWidth
        this.data.height = this.$refs.content.clientHeight
      }
    },
    setDrag({x, y}) {
      this.inSelected
        ? this.selectedObjects.map(o => this.onDragNode(o,{x, y}))
        : this.onDragNode(this.data, {x, y})
    },
    onDragNode(node, {x, y}) {
      node.x += x
      node.y += y
    },
    onMousedown (e) {
      e.stopPropagation()
      this.startDrag(e)
    },
  },
  watch: {
    inSelected: {
      handler: function(val) {
        if(val !== null) {
          this.$off('drag')
          this.$on('drag', e => this.setDrag(e))
        }
      },
      immediate: true,
    },
  },
  updated() {
    this.fitContent()
  }
}
</script>

<style scoped>
.content {
  background-color: white;
  border-radius: 100%;
  position: initial;
  white-space: nowrap;
  width: fit-content;
}
</style>