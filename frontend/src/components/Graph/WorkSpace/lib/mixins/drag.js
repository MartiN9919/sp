/**
 * Adds drag behavior to Vue component
 * @drag event emmited
 */
import drag from "vnodes/src/mixins/drag";
let moved = false

export default {
  props: {
    dragThreshold: {
      type: Number,
      default: 10
    }
  },
  data () {
    return {
      drag: {
        zoom: 1,
        active: false,
        prev: { x: 0, y: 0 },
        threshold: { x: 0, y: 0, crossed: false }
      },
      screen: document.getElementById('screen'),
    }
  },
  beforeDestroy () {
    this.screen.removeEventListener('mousemove', this.applyDrag)
    this.screen.removeEventListener('mouseup', this.stopDrag)
  },
  methods: {
    isMoved() {
      return moved
    },
    startDrag (e) {
      let parent = this.$parent
      while (parent) {
        if (parent.panzoom) {
          this.drag.zoom = parent.panzoom.getZoom()
          break;
        }
        parent = parent.$parent
      }
      this.drag.active = true
      this.drag.prev = { x: e.clientX, y: e.clientY }
      this.drag.threshold = {x: 0, y: 0, crossed: false}
      this.screen.addEventListener('mouseup', this.stopDrag, true)
      this.screen.addEventListener('mousemove', this.applyDrag)
      this.screen.addEventListener('mouseleave', this.stopDrag)
    },
    stopDrag (e) {
      if(moved) {
        moved = false
        e.stopPropagation()
      }
      this.drag.active = false
      this.screen.removeEventListener('mouseup', this.stopDrag)
      this.screen.removeEventListener('mousemove', this.applyDrag)
      this.screen.removeEventListener('mouseleave', this.stopDrag)
    },
    applyDrag (e) {
      let x = (e.clientX - this.drag.prev.x) / this.drag.zoom
      let y = (e.clientY - this.drag.prev.y) / this.drag.zoom
      this.drag.prev = {x: e.clientX, y: e.clientY}
      moved = true
      if (!this.drag.threshold.crossed) {
        if (Math.abs(this.drag.threshold.x) < this.dragThreshold && Math.abs(this.drag.threshold.y) < this.dragThreshold) {
          this.drag.threshold.x += x
          this.drag.threshold.y += y
          return // don't apply drag until threshold is reached
        } else {
          this.drag.threshold.crossed = true
          x += this.drag.threshold.x
          y += this.drag.threshold.y
        }
      }
      this.$emit('drag', { x, y })
    },
  }
}
