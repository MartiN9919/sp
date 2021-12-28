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
      oldNodeSize: {width: 0, height: 0},
      perc: 50,
    }
  },
  mounted () {
    this.checkTypeElement()
    this.offset = {
      x: 0,
      y: -((this.element.hasOwnProperty('from') ? 40 : this.element.size / 3) + this.node.height)
    }
    this.oldNodeSize = {width: this.node.width, height: this.node.height}
  },
  methods: {
    checkTypeElement() {
      if(this.element.hasOwnProperty('type'))
        this.$nextTick(this.getPositionForEdge)
      else this.$nextTick(this.getPositionForNode)
    },
    getPositionForNode () {
      this.pos = {x: this.element.x + this.element.size / 6, y: this.element.y + this.element.size / 6}
    },
    getPositionForEdge () {
      const el = document.getElementById(this.element.id)
      const length = el.getTotalLength() * (this.perc/100)
      this.pos = el.getPointAtLength(length)
    },
    updatePos(){
      this.updateOffsetBySize()
      this.node.x = this.pos.x + this.offset.x - this.element.size/2
      this.node.y = this.pos.y + this.offset.y
    },
    updateOffset(x=0, y=0){
      let offsetX = this.offset.x + (x || 0) + (this.node.width/2)
      let offsetY = this.offset.y + (y || 0) + (this.node.height/2)
      let totalOffset = Math.sqrt(Math.pow(offsetX,2) + Math.pow(offsetY,2))
      if(totalOffset < this.node.width*2){
          this.offset.x += (x || 0)
          this.offset.y += (y || 0)
        }
      this.updatePos()
    },
    updateOffsetBySize(){
      if(this.oldNodeSize.width - this.element.size !== 0){
        if(this.oldNodeSize.width - this.element.size > 0 && !this.element.hasOwnProperty('type')){
          this.offset.y /= 1.5
        }
        if(this.oldNodeSize.width - this.element.size < 0 && !this.element.hasOwnProperty('type')){
          this.offset.y *= 1.5
        }
        this.oldNodeSize.width = this.element.size
      }
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
    element: {deep: true, handler: 'checkTypeElement'},
    pos: {deep: true, handler: 'updatePos'},
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

