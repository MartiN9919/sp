<script>
export default {
  name: "scrollMixin",
  methods: {
    scrollObject(object, event) {
      const minSize = 300
      const maxSize = 1500
      const coefficient = 1.5
      if(event.deltaY < 0 && object.size * coefficient < maxSize)
        this.changeObjectForScrolling(object, coefficient)
      else if (event.deltaY > 0 && object.size / coefficient > minSize)
        this.changeObjectForScrolling(object, 1/ coefficient)
    },
    changeObjectForScrolling(object, coefficient) {
      const bodySize = object.size / 3
      const offset = (bodySize - bodySize * coefficient) / 2
      object.x += offset
      object.y += offset
      object.size *= coefficient
    }
  }
}
</script>
