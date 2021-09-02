// инициализация маркеров

import { MAP_ITEM } from '@/components/Map/Leaflet/Lib/Const';


export function marker_get(latlng, options={}) {
  let icon = icon_get(options);
  return icon_2_marker(latlng, icon);
}

export function icon_2_marker(latlng, icon, options={}) {
  let param = (icon) ? { icon:icon, } : {};
  return L.marker(latlng, {...param, ...options});
}

export function icon_get(options={}) {
  let name = options.name || '';

  //
  // MAP_ITEM.MARKER.DEFAULT
  //
  if (name==MAP_ITEM.MARKER.DEFAULT) {
    return undefined;
  };


  //
  // MAP_ITEM.MARKER.COLOR
  // невозможна плавная смена цвета, только заданные значения
  if (name==MAP_ITEM.MARKER.COLOR) {
    let ret = {
      shadowUrl:   require('@/assets/img/markers/marker-shadow.png'),
      iconSize:    [25, 41],
      iconAnchor:  [12, 41],
      popupAnchor: [1, -34],
      shadowSize:  [41, 41],
    };

    switch(options.color) {
      case 'red':
      case '#f00':
        ret.iconUrl = require('@/assets/img/markers/marker-icon-2x-red.png');
        break;

      case 'green':
      case '#0f0':
        ret.iconUrl = require('@/assets/img/markers/marker-icon-2x-green.png');
        break;

      case 'blue':
      case '#00f':
        ret.iconUrl = require('@/assets/img/markers/marker-icon-2x-blue.png');
        break;

      case 'gold':
        ret.iconUrl = require('@/assets/img/markers/marker-icon-2x-gold.png');
        break;

      case 'orange':
        ret.iconUrl = require('@/assets/img/markers/marker-icon-2x-orange.png');
        break;

      case 'yellow':
        ret.iconUrl = require('@/assets/img/markers/marker-icon-2x-yellow.png');
        break;

      case 'violet':
        ret.iconUrl = require('@/assets/img/markers/marker-icon-2x-violet.png');
        break;

      case 'grey':
        ret.iconUrl = require('@/assets/img/markers/marker-icon-2x-grey.png');
        break;

      case 'black':
        ret.iconUrl = require('@/assets/img/markers/marker-icon-2x-black.png');
        break;

      default:
        return undefined;
    };
    return new L.Icon(ret);
  };



  //
  // MAP_ITEM.MARKER.PULSE
  //
  if (name==MAP_ITEM.MARKER.PULSE) {
    let color2 = options.color;
    let size   = options.size || 12;
    return L.icon.pulse({
      iconSize:  [size, size],
      color:     color2,
      fillColor: color2,
    });
  };


  //
  // MAP_ITEM.MARKER.FONT
  //
  if (name==MAP_ITEM.MARKER.FONT) {
    let color2 = options.color;
    let icon  = options.icon;
    return L.divIcon({
      iconSize: null,
      color:    color2,
      icon:     icon,
      html:
        '<div class="marker-font redborder">'+
          '<div class="marker-font-content" style="border-color: '+color2+';">'+
            '<span class="v-icon mdi '+icon+'" style="color: '+color2+';">'+
          '</div>'+
          '<div class="marker-font-arrow" style="border-top-color: '+color2+';"></div>'+
        '</div>',
    });
  };


}
