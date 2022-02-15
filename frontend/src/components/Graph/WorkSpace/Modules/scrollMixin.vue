<script>
export default {
  name: "scrollMixin",
  methods: {
    scrollObject(object, event) {
      const minSize = 300
      const maxSize = 2100
      const coefficient = 1.5
      if(event.deltaY < 0 && object.size * coefficient <= maxSize)
        this.changeObjectForScrolling(object, coefficient)
      else if (event.deltaY > 0 && object.size / coefficient >= minSize)
        this.changeObjectForScrolling(object, 1/ coefficient)
    },
    changeObjectForScrolling(object, coefficient) {
      const offset = (object.size - object.size * coefficient) / 6
      object.x += offset
      object.y += offset
      object.size *= coefficient
    }
  }
}
</script>
