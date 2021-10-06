// инициализация маркеров

import { MAP_ITEM } from '@/components/Map/Leaflet/Lib/Const';


export function marker_get(latlng, options={}) {
  let icon = icon_get(options);
  return icon_2_marker(latlng, icon, options.className);
}

export function icon_2_marker(latlng, icon, className='', options={}) {
  let param = (icon) ? { icon:icon, } : {};
  let ret = L.marker(latlng, {...param, ...options});

  // класс при отсутствии иконки. Для заданных иконок он установлен в icon_get
  if (!icon) { ret.options.icon.options.className = className; }

  return ret

}

export function icon_get(options={}) {
  let name = options.name || MAP_ITEM.MARKER.DEFAULT;

  //
  // MAP_ITEM.MARKER.DEFAULT
  //
  if (name==MAP_ITEM.MARKER.DEFAULT) {
    return undefined;
  };


  //
  // MAP_ITEM.MARKER.IMAGE
  // имя маркера = имя файла.png
  if (name==MAP_ITEM.MARKER.IMAGE) {
    let ret = {
      shadowUrl:   icon_path('marker-shadow'),
      iconSize:    [25, 41],
      iconAnchor:  [12, 41],
      popupAnchor: [1, -34],
      shadowSize:  [41, 41],
      className:   options.className || '',
    };

  };

  //
  // MAP_ITEM.MARKER.COLOR
  // невозможна плавная смена цвета, только заданные значения
  if (name==MAP_ITEM.MARKER.COLOR) {
    let ret = {
      shadowUrl:   icon_path('marker-shadow'),
      iconSize:    [25, 41],
      iconAnchor:  [12, 41],
      popupAnchor: [1, -34],
      shadowSize:  [41, 41],
      className:   options.className || '',
    };

    switch(options.color) {
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



  //
  // MAP_ITEM.MARKER.PULSE
  //
  if (name==MAP_ITEM.MARKER.PULSE) {
    let color2 = options.color;
    let size   = options.size || 12;
    return L.icon.pulse({
      className: options.className || '',
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
    let icon   = options.icon;
    return L.divIcon({
      className: options.className || '',
      iconSize:  null,
      color:     color2,
      icon:      icon,
      html:
        // '<div class="marker-font" style="color: '+color2+';">'+
        //   '<div class="fs fs-spec0 fs-test" style="border-color: '+color2+';">'+
        //   '</div>'+
        // '</div>',

        // '<div class="marker-font" style="color: '+color2+';">'+
        //   '<span class="marker-font-mdi mdi mdi-map-marker style="color: '+color2+';">'+
        // '</div>',

        '<div class="marker-font">'+
          '<div class="marker-font-content" style="border-color: '+color2+';">'+
            '<span class="v-icon mdi '+icon+'" style="color: '+color2+';">'+
          '</div>'+
          '<div class="marker-font-arrow" style="border-top-color: '+color2+';"></div>'+
        '</div>',
    });
  };


}

function icon_path(name) {
  // require('@/assets/img/markers/marker-icon-red.png');
  return process.env.BASE_URL+MAP_ITEM.MARKER.PATH+name+'.png';
}
