// import {
//   L,
// } from 'vue2-leaflet';


export default {
  methods: {
    // ВАЖНО
    // вызывать из родительского mounted или method.onMapReady
    // должна быть установлена переменная this.map
    mounted_after_svg(L) {
      let svg = document.createElement('svg');
      svg.innerHTML = `
      <defs>
        <pattern id="star" viewBox="0,0,10,10" width="10%" height="10%">
          <polygon points="0,0 2,5 0,10 5,8 10,10 8,5 10,0 5,2"/>
        </pattern>
      </defs>
      `;
      document.body.prepend(svg);


      // if (!this._defs) {
      //   this._defs = L.SVG.create('defs');
      //   document.body.prepend(this._defs);
      //   //this._container.appendChild(this._defs);
      // }

      //var _p = document.getElementById(_ref_id);

      // // this.map.addEventListener('keydown', this.key_down);
      // // this.key_load_pos(1);
      // debugger
      // var _p = L.SVG.create('pattern');
      // console.log(2, _p)
    },
  },




}
