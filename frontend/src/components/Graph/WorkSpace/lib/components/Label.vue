<template>
  <g>
    <path v-if="connector" :d="getLineCoordinates" class="connector"></path>
    <node ref="node" :data="node" @drag="onDrag">
      <slot></slot>
    </node>
  </g>
</template>

<script>
import uuid from 'uuid'
import Node from './Node'

export default {
  components: {Node},
  props: {
    element: {type: Object, required: true},
    useDrag: {type: Boolean, default: false},
    connector: {type: Boolean, default: true},
    edgeCoordinates: {type: Object, default: null},
  },
  data() {
    return {
      pos: { x: 0, y: 0 },
      node: { id: uuid() ,x: 250, y: 0, width: 100, height: 100},
      offset: {x: 0, y: 0},
      oldElementSize: {width: 0, height: 0},
      oldNodeSize: {width: 0, height: 0},
      perc: 50,
      elementType: 'node'
    }
  },
  mounted () {
    if(this.element.hasOwnProperty('type'))
      this.elementType = 'edge'
    else this.elementType = 'node'
    this.offset = {
      x: 0,
      y: -((this.element.hasOwnProperty('from') ? 40 : this.element.width) + this.node.height)
    }
    this.oldElementSize = {width: this.element.width, height: this.element.height}
    this.oldNodeSize = {width: this.node.width, height: this.node.height}
    this.getPosition()
  },
  methods: {
    getPosition() {
      if(this.elementType === 'edge') {
        const el = document.getElementById(this.element.id)
        const length = el.getTotalLength() * (this.perc/100)
        this.pos = el.getPointAtLength(length)
      }
      else {
        this.pos = {x: this.element.x + this.element.width / 2, y: this.element.y + this.element.height / 2}
      }
      this.updatePos()
    },
    updatePos(){
      this.node.x = this.pos.x + this.offset.x - this.node.width/2
      this.node.y = this.pos.y + this.offset.y
    },
    updateOffset(x=0, y=0){
      let oldTotalOffset = Math.sqrt(Math.pow(this.offset.x,2) + Math.pow(this.offset.y,2))
      let offsetX = this.offset.x + (x || 0)
      let offsetY = this.offset.y + (y || 0)
      let totalOffset = Math.sqrt(Math.pow(offsetX,2) + Math.pow(offsetY,2))
      if(totalOffset < this.node.width*2 || oldTotalOffset >= totalOffset) {
          this.offset.x += (x || 0)
          this.offset.y += (y || 0)
      }
      this.updatePos()
    },
    updateOffsetByClassifier() {
      if(this.oldElementSize.width === this.element.width) {
        this.offset.y -= this.node.height - this.oldNodeSize.height
        this.oldNodeSize.height = this.node.height
        this.updatePos()
      }
    },
    updateOffsetBySize(){
      if(this.oldElementSize.width - this.element.width  > 0){
        this.offset.y /= 1.5
        this.offset.x /= 1.5
        this.updatePos()
      }
      if(this.oldElementSize.width - this.element.width  < 0){
        this.offset.y *= 1.5
        this.offset.x *= 1.5
        this.updatePos()
      }
      this.oldElementSize.width = this.element.width
      this.oldNodeSize.height = this.node.height
    },
    onDrag (d) {
      this.updateOffset(d.x || 0, d.y || 0)
    }
  },
  computed: {
    getLineCoordinates() {
      return `M ${this.pos.x} ${this.pos.y} L ${this.node.x + this.node.width / 2} ${this.node.y + this.node.height / 2}`
    }
  },
  updated() {
     this.$refs.node.fitContent()
  },
  watch: {
    'node.width': {handler: 'updatePos'},
    'node.height': {handler: 'updateOffsetByClassifier'},
    'element.width': {handler: 'updateOffsetBySize'},
    'element.pathd': {handler: 'getPosition'},
    'element.x': {handler: 'getPosition'},
    'element.y': {handler: 'getPosition'},
  },
}
</script>

<style scoped>
.connector {
  stroke-width: 1px;
  stroke: #aaaaaa;
  stroke-dasharray: 1em;

}
</style>

