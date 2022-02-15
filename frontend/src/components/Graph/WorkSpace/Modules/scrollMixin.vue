<script>
export default {
  name: "scrollMixin",
  methods: {
    scrollObject(object, event) {
      const minSize = 100
      const maxSize = 700
      const coefficient = 1.5
      if(event.deltaY < 0 && object.width * coefficient <= maxSize)
        this.changeObjectForScrolling(object, coefficient)
      else if (event.deltaY > 0 && object.width / coefficient >= minSize)
        this.changeObjectForScrolling(object, 1/ coefficient)
    },
    changeObjectForScrolling(object, coefficient) {
      const bodyWidth = object.width
      const bodyHeight = object.height
      const offsetX = (bodyWidth - bodyWidth * coefficient) / 2
      const offsetY = (bodyHeight - bodyHeight * coefficient) / 2
      object.x += offsetX
      object.y += offsetY
      object.width *= coefficient
      object.height *= coefficient
    }
  }
}
</script>
