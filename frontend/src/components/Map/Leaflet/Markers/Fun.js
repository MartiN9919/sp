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
  var file = icon_path('icon');
  проверить доступность файла

  if (icon==STYLE.MARKER.ICON) {
    let ret = {
      shadowUrl:   icon_path('marker-shadow'),
      iconSize:    [25, 41],
      iconAnchor:  [12, 41],
      popupAnchor: [1, -34],
      shadowSize:  [41, 41],
      className:   className,
    };

    switch(style.color) {
      case 'red':
      case '#f00':
        ret.iconUrl = icon_path('marker-red');
        break;

      case 'green':
      case '#0f0':
        ret.iconUrl = icon_path('marker-2x-green');
        break;

      case 'blue':
      case '#00f':
        ret.iconUrl = icon_path('marker-2x-blue');
        break;

      case 'gold':
        ret.iconUrl = icon_path('marker-2x-gold');
        break;

      case 'orange':
        ret.iconUrl = icon_path('marker-2x-orange');
        break;

      case 'yellow':
        ret.iconUrl = icon_path('marker-2x-yellow');
        break;

      case 'violet':
        ret.iconUrl = icon_path('marker-2x-violet');
        break;

      case 'grey':
        ret.iconUrl = icon_path('marker-2x-grey');
        break;

      case 'black':
        ret.iconUrl = icon_path('marker-2x-black');
        break;

      default:
        return undefined;
    };
    return new L.Icon(ret);
  };


  return undefined;




  // //
  // // MAP_STYLE.MARKER.TYPE.DEF
  // //
  // if (type==STYLE.MARKER.TYPE.DEF) {
  //   return undefined;
  // };


  // //
  // // MAP_ITEM.MARKER.IMAGE
  // // имя маркера = имя файла.png
  // if (type==MAP_ITEM.MARKER.IMAGE) {
  //   let ret = {
  //     shadowUrl:   icon_path('marker-shadow'),
  //     iconSize:    [25, 41],
  //     iconAnchor:  [12, 41],
  //     popupAnchor: [1, -34],
  //     shadowSize:  [41, 41],
  //     className:   className,
  //   };

  // };

  // //
  // // MAP_ITEM.MARKER.COLOR
  // // невозможна плавная смена цвета, только заданные значения
  // if (type==MAP_ITEM.MARKER.COLOR) {
  //   let ret = {
  //     shadowUrl:   icon_path('marker-shadow'),
  //     iconSize:    [25, 41],
  //     iconAnchor:  [12, 41],
  //     popupAnchor: [1, -34],
  //     shadowSize:  [41, 41],
  //     className:   className,
  //   };

  //   switch(style.color) {
  //     case 'red':
  //     case '#f00':
  //       ret.iconUrl = icon_path('marker-red');
  //       break;

  //     case 'green':
  //     case '#0f0':
  //       ret.iconUrl = icon_path('marker-2x-green');
  //       break;

  //     case 'blue':
  //     case '#00f':
  //       ret.iconUrl = icon_path('marker-2x-blue');
  //       break;

  //     case 'gold':
  //       ret.iconUrl = icon_path('marker-2x-gold');
  //       break;

  //     case 'orange':
  //       ret.iconUrl = icon_path('marker-2x-orange');
  //       break;

  //     case 'yellow':
  //       ret.iconUrl = icon_path('marker-2x-yellow');
  //       break;

  //     case 'violet':
  //       ret.iconUrl = icon_path('marker-2x-violet');
  //       break;

  //     case 'grey':
  //       ret.iconUrl = icon_path('marker-2x-grey');
  //       break;

  //     case 'black':
  //       ret.iconUrl = icon_path('marker-2x-black');
  //       break;

  //     default:
  //       return undefined;
  //   };
  //   return new L.Icon(ret);
  // };





}

function icon_path(name) {
  // require('@/assets/img/markers/marker-icon-red.png');
  return process.env.BASE_URL+MAP_ITEM.MARKER.PATH+name+'.png';
}
