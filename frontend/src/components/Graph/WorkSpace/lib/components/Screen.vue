<template>
  <svg class="screen" ref="screen" @mousedown.ctrl="startDrawFrame" @contextmenu.prevent="">
    <g id="screen">
      <slot/>
    </g>
    <rect v-bind="disableFrame" class="disable-frame" @mouseenter.stop="" @mouseleave.stop=""/>
    <rect v-show="frame.active" :x="frame.x" :y="frame.y" :width="frame.width" :height="frame.height" class="frame"/>
  </svg>
</template>

<script>
import SvgPanZoom from '../svg-pan-zoom/svg-pan-zoom'
export default {
  props: {
    options: {
      type: Object,
      default: () => ({})
    }
  },
  data() {
    return {
      panzoom: null,
      frame: {active: false}
    }
  },
  computed: {
    disableFrame: function () {
      if(this.frame.active) {
        const offset = 100 / this.panzoom.getZoom()
        return {
          x: this.frame.x - offset,
          y: this.frame.y - offset,
          width: this.frame.width + offset*2,
          height: this.frame.height + offset*2
        }
      }
      else {
        return {x:0, y: 0, width: 0, height: 0}
      }
    },
  },
  mounted () {
    this.panzoom = SvgPanZoom(this.$refs.screen, Object.assign({
      dblClickZoomEnabled: false,
      mouseWheelZoomEnabled: true,
      preventMouseEventsDefault: true,
      fit: false,
      contain: false,
      center: false,
      zoomScaleSensitivity: 0.4,
      minZoom: 0.1,
      maxZoom: 5,
      onZoom: scale => {},
      onPan: pan => {},
      onUserZoom: e => {},
      onUserPan: e => {},
      onDoubleClick: () => {},
      onUpdatedCTM: m => {}
    }, this.options))

    this.panzoom.zoomRect = this.zoomRect
    this.panzoom.zoomNode = this.zoomNode
    this.panzoom.panNode = this.panNode
  },
  methods: {
    startDrawFrame(event){
      let position = this.getScreenPosition(event.offsetX, event.offsetY)
      this.frame = {x0:position.x, y0: position.y, xn: position.x, yn: position.y,
        x:position.x, y: position.y, width: 0, height: 0, active: true}
      document.addEventListener('mousemove', this.drawFrame)
      document.addEventListener('mouseleave', this.stopDrawFrame)
      document.addEventListener('mouseup', this.stopDrawFrame)
    },
    stopDrawFrame(){
      this.$emit('selectNodes', {x: this.frame.x, y: this.frame.y, width: this.frame.width, height: this.frame.height})
      this.frame = {active: false, height: 0, width: 0}
      document.removeEventListener('mousemove', this.drawFrame)
      document.removeEventListener('mouseup', this.stopDrawFrame)
      document.removeEventListener('mouseleave', this.stopDrawFrame)
    },
    drawFrame(event){
      if(this.frame.active){
        const zoom = this.panzoom.getZoom()
        if(event.offsetX < this.$refs.screen.clientWidth)
          this.frame.xn += event.movementX / zoom
        if(event.offsetY < this.$refs.screen.clientHeight)
          this.frame.yn += event.movementY / zoom
        if(this.frame.xn > this.frame.x0)
          this.frame.x = this.frame.x0
        else
          this.frame.x = this.frame.xn
        if(this.frame.yn > this.frame.y0)
          this.frame.y = this.frame.y0
        else
          this.frame.y = this.frame.yn
        this.frame.width = Math.abs(this.frame.xn - this.frame.x0)
        this.frame.height = Math.abs(this.frame.yn - this.frame.y0)
      }
    },
    zoomTo ({x, y, scale}) {
      this.panzoom.zoom(scale)
      this.panzoom.pan( x,y )
    },
    /**
     * Centers and zooms a rectangle
     * @param rect { left, right, top, bottom }
     * @param scale force zoom to a specific value (eg: 1)
     */
    zoomRect (rect, opts = {scale: null}) {
      let scale = opts.scale
      const screen = this.$refs.screen
      const width = rect.right - rect.left
      const height = rect.bottom - rect.top
      if (!scale) {
        const dx = width / screen.clientWidth
        const dy = height / screen.clientHeight
        scale = 1 / Math.max(dx, dy)
      }
      const x = -rect.left * scale + ((screen.clientWidth / scale - width) / 2) * scale
      const y = -rect.top * scale + ((screen.clientHeight / scale - height) / 2) * scale

      this.panzoom.zoom(scale)
      this.panzoom.pan({ x, y })
    },
    zoomNode (node, scale=null) {
      const screen = this.$refs.screen
      const marginX = screen.clientWidth / 2 - node.size / 6
      const marginY = screen.clientHeight / 2 - node.size / 6

      this.zoomRect({
        left: node.x - marginX,
        right: node.x + node.size / 3 + marginX,
        top: node.y - marginY,
        bottom: node.y + node.size / 3 + marginY
      }, { scale })
    },
    /**
     * centers the view and zoom on a group nodes
     */
    zoomNodes (nodes, opts = { padding: 50, scale: null }) {
      if (!nodes || !nodes.length) {
        return
      }
      const padding = opts.padding || 50
      const scale = opts.scale
      let left = Infinity
      let top = Infinity
      let right = -Infinity
      let bottom = -Infinity

      nodes.forEach(node => {
        if (node.x < left) left = node.x
        if (node.x + node.width > right) right = node.x + node.width
        if (node.y < top) top = node.y
        if (node.y + node.height > bottom) bottom = node.y + node.height
      })

      this.zoomRect({
        left: left - padding,
        top: top - padding,
        right: right + padding,
        bottom: bottom + padding,
      }, { scale })
    },
    panNode (node, opts = { offsetX, offsetY }) { // centers node on screen
      const offsetX = opts.offsetX || 0
      const offsetY = opts.offsetY || 0
      const zoom = this.panzoom.getZoom()
      const x = this.$el.clientWidth / 2 - (node.x + node.width / 2) * zoom + offsetX
      const y = this.$el.clientHeight / 2 - (node.y + node.height / 2) * zoom + offsetY
      this.panzoom.pan({ x, y })
    },
    getScreenPosition(x=this.$el.clientWidth, y=this.$el.clientHeight) {
      let position = {x: 0, y: 0}
      const zoom = this.panzoom.getZoom()
      const pan = this.panzoom.getPan()
      position.x = (x - pan.x) / zoom
      position.y = (y - pan.y) / zoom
      return position
    },
    visibleArea() {
      const zoom = this.panzoom.getZoom()
      let position = this.getScreenPosition()
      position.width = this.$el.clientWidth / zoom
      position.height = this.$el.clientHeight / zoom
      return position
    },

  },
}
</script>

<style scoped>
.screen {
  width: 100%;
  height: 100%;
}
.frame {
  fill:rgba(0, 0, 255, 0.1);
}

.disable-frame {
  fill: rgba(0, 0, 0, 0)
}
</style>