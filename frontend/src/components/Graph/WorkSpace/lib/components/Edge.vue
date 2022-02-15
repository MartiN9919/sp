<template>
  <path :id="`${edge.id}-edge`" :d="path" :class="relationClass" class="edge"/>
</template>

<script>
export default {
  props: {
    edge: {
      type: Object,
      required: true
    },
    nodes: Array,
    inHover: Boolean,
  },

  computed: {
    relationClass() {
      if(this.inHover) {
        return 'hover-relation'
      } else return 'base-relation'
    },

    from: function () {
      return this.nodes.find(n => n.id === this.edge.from)
    },

    to: function () {
      return this.nodes.find(n => n.id === this.edge.to)
    },

    pos () {
      let x1 = this.from.x + this.from.size / 6
      let y1 = this.from.y + this.from.size / 6
      let x2 = this.to.x + this.to.size / 6
      let y2 = this.to.y + this.to.size / 6
      return { x1, x2, y1, y2 }
    },

    path () {
      const pos = Object.assign({}, this.pos)
      this.edge.pathd = `M ${pos.x1},${pos.y1} ${pos.x2} ${pos.y2}`
      return this.edge.pathd
    },
  },
}
</script>

<style scoped>
.edge {
  marker-end: none;
  fill: none;
}

.base-relation {
  stroke-width: 2px;
  stroke: #aaaaaa;
}

.hover-relation {
  stroke-width: 5px;
  stroke: rgba(0, 0, 255, 0.3);
}

.added-relation {
  stroke-width: 5px;
  stroke: rgba(0, 255, 0, 0.3);
}
</style>
