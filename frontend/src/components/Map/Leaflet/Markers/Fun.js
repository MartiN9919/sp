// инициализация маркеров

import { MAP_ITEM } from '@/components/Map/Leaflet/Lib/ConstOld';
import { MAP_STYLE } from '@/components/Map/Leaflet/Lib/Const';
var STYLE = MAP_STYLE;


export function marker_get(latlng, style={}, className='') {
  let icon = icon_get(style, className);
  return icon_2_marker(latlng, icon, undefined, className);
}

export function icon_2_marker(latlng, icon, style={}, className='') {
  let param = (icon) ? { icon:icon, } : {};
  let ret = L.marker(latlng, {...param, ...style});

  // класс при отсутствии иконки. Для заданных иконок он установлен в icon_get
  if (!icon) { ret.options.icon.options.className = className; }

  return ret

}

export function icon_get(style={}, className='') {
  var color  = style[STYLE.COLOR.KEY ] ?? STYLE.COLOR.DEF;
  var marker = style[STYLE.MARKER.KEY] ?? {};
  var icon   = marker[STYLE.MARKER.ICON.KEY] ?? STYLE.MARKER.ICON.DEF;


  // DEFAULT
  if (icon==STYLE.MARKER.ICON.DEF) {
    return undefined;
  }


  // FONT.MDI
  if (icon.slice(0, STYLE.MARKER.ICON.PREF_MDI.length) == STYLE.MARKER.ICON.PREF_MDI) {
    return L.divIcon({
      className: className,
      iconSize:  null,
      color:     color,
      icon:      icon,
      html:
        '<div class="marker-font">'+
          '<div class="marker-font-content" style="border-color: '+color+';">'+
            '<span class="v-icon mdi '+icon+'" style="color: '+color+';">'+
          '</div>'+
          '<div class="marker-font-arrow" style="border-top-color: '+color+';"></div>'+
        '</div>',
    });
  };
  // БЕЗ FRAME
  // '<div class="marker-font" style="color: '+color+';">'+
  //   '<span class="marker-font-mdi mdi mdi-map-marker style="color: '+color+';">'+
  // '</div>',


  // FONT.FS
  if (icon.slice(0, STYLE.MARKER.ICON.PREF_FS.length) == STYLE.MARKER.ICON.PREF_FS) {
    return L.divIcon({
      className: className,
      iconSize:  null,
      color:     color,
      icon:      icon,
      html:
        '<div class="marker-font" style="color: '+color+';">'+
          '<div class="fs '+icon+'" style="border-color: '+color+';">'+
          '</div>'+
        '</div>',
    });
  };


  // PULSE
  if (icon==STYLE.MARKER.ICON.PULSE) {
    var size  = marker[STYLE.MARKER.SIZE.KEY] ?? 12;
    return L.icon.pulse({
      className: className,
      iconSize:  [size, size],
      color:     color,
      fillColor: color,
    });
  };


  // FILE
  const equ = {
    '#f00': 'red',
    '#0f0': 'green',
    '#00f': 'blue',
  };
  if (equ[icon]) { icon = equ[icon]; }
  var size_w = marker[STYLE.MARKER.SIZE.KEY] ?? 25;
  var size_h = marker[STYLE.MARKER.SIZE.KEY] ?? 41;
  return new L.Icon({
    className:   className,
    shadowUrl:   icon_path('shadow-marker'),
    shadowSize:  [size_h, size_h],
    iconUrl:     icon_path(icon),
    iconSize:    [size_w, size_h],
    iconAnchor:  [size_w/2|0, size_h],
    popupAnchor: [1, -34],
  });
}

function icon_path(name) {
  // require('@/assets/img/markers/marker-icon-red.png');
  return process.env.BASE_URL+MAP_ITEM.MARKER.PATH+name+'.png';
}
