<template>
  <svg class="screen" ref="screen">
    <g id="screen">
      <slot>
      </slot>
    </g>
  </svg>
</template>

<script>
import SvgPanZoom from '../../lib/svg-pan-zoom/svg-pan-zoom'
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
    }
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
    zoomNode (node) {
      const screen = this.$refs.screen
      const marginX = screen.clientWidth / 2 - node.width / 2
      const marginY = screen.clientHeight / 2 - node.height / 2

      this.zoomRect({
        left: node.x - marginX,
        right: node.x + node.width + marginX,
        top: node.y - marginY,
        bottom: node.y + node.height + marginY
      })
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
    getStartPosition() {
      let position = {x: 0, y: 0}
      const zoom = this.panzoom.getZoom()
      const pan = this.panzoom.getPan()
      position.x = (this.$el.clientWidth / 2 - pan.x) / zoom + Math.random() * 600 - 300
      position.y = (this.$el.clientHeight / 2 - pan.y) / zoom + Math.random() * 600 - 300
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
</style>