// Добавляет позицию контрола
// https://stackoverflow.com/questions/33614912/how-to-locate-leaflet-zoom-control-in-a-desired-position

export default {
  mounted: function() {
    let map     = this.$refs.map.mapObject;
    let corners = map._controlCorners,
      l = 'leaflet-',
      container = map._controlContainer;

    function createCorner(vSide, hSide) {
      var className = l + vSide + ' ' + l + hSide;
      corners[vSide + hSide] = L.DomUtil.create('div', className, container);
    }
    createCorner('centervertical',   'left');
    createCorner('centervertical',   'right');
    createCorner('top',              'centerhorizontal');
    createCorner('bottom',           'centerhorizontal');

    // map.zoomControl.setPosition('bottomcenterhorizontal');           пример
    // L.control.scale({position: 'verticalcenterright'}).addTo(map);   пример
  },

};
