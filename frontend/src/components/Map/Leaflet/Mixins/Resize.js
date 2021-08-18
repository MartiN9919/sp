// вызывает методы при изменении размеров элемента
// по умолчанию this.onResize на компонент
export default {
  data: ()     => ({ ro_list: [], }),
  mounted()        { this.roAdd(this.$el, this.onResize); },
  beforeDestroy () { this.roDel(); },
  methods: {
    roAdd(element, fun) {
      if (fun) {
        let obj = new ResizeObserver(fun);
        obj.observe(element);
        this.ro_list.push( obj );
      };
    },
    roDel() {
      for (let ro of this.ro_list) { ro.disconnect(); }
      this.ro_list = [];
    },
  },
};
