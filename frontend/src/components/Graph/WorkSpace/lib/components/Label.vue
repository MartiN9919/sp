<template>
  <g>
    <path :d="getLineCoordinates" class="connector"/>
    <node ref="node" :data="node" @drag="onDrag">
      <slot/>
    </node>
  </g>
</template>

<script>
import uuid from 'uuid'
import Node from './Node'
import {Edge} from '@/components/Graph/WorkSpace/lib/graph'

export default {
  components: {Node},
  props: {
    element: {type: Object, required: true},
  },
  data() {
    return {
      pos: { x: 0, y: 0 },
      node: {id: uuid(), x: 0, y: 0, width: 0, height: 0},
      offset: {x: 0, y: 0},
      oldElementSize: 600,
      oldNodeSize: {width: 0, height: 0},
      elementType: 'node'
    }
  },
  mounted () {
    if(this.element instanceof Edge)
      this.elementType = 'edge'
    else this.elementType = 'node'
    this.offset = {
      x: 0,
      y: -((this.elementType === 'edge' ? 20 : this.element.size / 3) + this.node.height)
    }
    this.oldElementSize = this.element.size
    this.oldNodeSize = {width: this.node.width, height: this.node.height}
    this.getPosition()
  },
  methods: {
    getPosition() {
      if(this.elementType === 'edge') {
        const el = document.getElementById(`${this.element.id}-edge`)
        const length = el.getTotalLength() / 2
        this.pos = el.getPointAtLength(length)
      }
      else {
        this.pos = {x: this.element.x + this.element.size / 6, y: this.element.y + this.element.size / 6}
      }
      this.updatePos()
    },
    updatePos(){
      this.node.x = this.pos.x + this.offset.x - this.node.width / 2
      this.node.y = this.pos.y + this.offset.y
    },
    updateOffset(x, y){
      let oldTotalOffset = Math.sqrt(Math.pow(this.offset.x,2) + Math.pow(this.offset.y,2))
      let totalOffset = Math.sqrt(Math.pow(this.offset.x + x,2) + Math.pow(this.offset.y + y,2))
      if(totalOffset < this.node.width * 2 || oldTotalOffset >= totalOffset) {
          this.offset.x += x
          this.offset.y += y
      }
      this.updatePos()
    },
    updateOffsetBySize() {
      if(this.oldElementSize === this.element.size) {
        this.offset.y -= this.node.height - this.oldNodeSize.height
      }
      else {
        if(this.oldElementSize - this.element.size > 0){
          this.offset.y /= 1.5
          this.offset.x /= 1.5
        }
        if(this.oldElementSize - this.element.size < 0){
          this.offset.y *= 1.5
          this.offset.x *= 1.5
        }
        this.oldElementSize = this.element.size
      }
      this.oldNodeSize.height = this.node.height
      this.updatePos()
    },
    onDrag (d) {
      this.updateOffset(d.x || 0, d.y || 0)
    },
  },
  computed: {
    getLineCoordinates() {
      return `M ${this.pos.x} ${this.pos.y} L ${this.node.x + this.node.width / 2} ${this.node.y + this.node.height / 2}`
    }
  },
  watch: {
    'node.height': {handler: 'updateOffsetBySize'},
    'node.width': {handler: 'updateOffsetBySize'},
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

