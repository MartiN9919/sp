// вызывает методы при изменении размеров элемента
// по умолчанию this.onResize на компонент
export default {
  data: ()     => ({ ro_list: [], }),
  mounted()        { this.resize_add(this.$el, this.on_resize); },
  beforeDestroy () { this.resize_del(); },
  methods: {
    resize_add(element, fun=this.on_resize) {
      if (fun) {
        let obj = new ResizeObserver(fun);
        obj.observe(element);
        this.ro_list.push( obj );
      };
    },
    resize_del() {
      for (let ro of this.ro_list) { ro.disconnect(); }
      this.ro_list = [];
    },
  },
};
