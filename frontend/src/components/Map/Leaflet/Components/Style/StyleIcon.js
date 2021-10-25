// инициализация маркеров

import { MAP_ITEM } from '@/components/Map/Leaflet/Lib/Const';
import { Icon } from 'leaflet';
import { data_icon } from '@/components/Map/Leaflet/Components/Style/StyleIconData';



// устранение бага с путями
export function icon_ini() {
  delete Icon.Default.prototype._getIconUrl;
  Icon.Default.mergeOptions({
    iconRetinaUrl: icon_path('blue-2x'),
    iconUrl:       icon_path('blue'),
    shadowUrl:     icon_path('shadow-marker'),
  });
}


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
  let color  = style [MAP_ITEM.FC.STYLE._COLOR_.KEY    ] ?? MAP_ITEM.COLOR.DEF;
  let marker = style [MAP_ITEM.FC.STYLE.MARKER.KEY     ] ?? {};
  let icon   = marker[MAP_ITEM.FC.STYLE.MARKER.ICON.KEY] ?? MAP_ITEM.FC.STYLE.MARKER.ICON.DEF;
  let zoom   = marker[MAP_ITEM.FC.STYLE.MARKER.ZOOM.KEY] ?? 1;

  //data_icon('icon-mdi-flag sss icon-mdi-spin tst')
  let ret = data_icon(className, color);
  if (ret) return ret;

  // DEFAULT
  if (icon==MAP_ITEM.FC.STYLE.MARKER.ICON.DEF) {
    return undefined;
  }


  // FONT.MDI
  if (icon.slice(0, MAP_ITEM.FC.STYLE.MARKER.ICON.PREF_MDI.length) == MAP_ITEM.FC.STYLE.MARKER.ICON.PREF_MDI) {
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
  if (icon.slice(0, MAP_ITEM.FC.STYLE.MARKER.ICON.PREF_FS.length) == MAP_ITEM.FC.STYLE.MARKER.ICON.PREF_FS) {
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
  if (icon==MAP_ITEM.FC.STYLE.MARKER.ICON.PULSE) {
    let size  = (marker[MAP_ITEM.FC.STYLE.MARKER.SIZE.KEY] ?? 12) * zoom|0;
    return L.icon.pulse({
      className: className,
      iconSize:  [size, size],
      color:     color,
      fillColor: color,
    });
  };


  // FILE
  const equ = {
    '#000': 'black',
    '#f00': 'red',
    '#0f0': 'green',
    '#00f': 'blue',
  };
  if (equ[icon]) { icon = equ[icon]; }
  let size_w = (marker[MAP_ITEM.FC.STYLE.MARKER.SIZE_W.KEY] ?? 25) * zoom|0;
  let size_h = (marker[MAP_ITEM.FC.STYLE.MARKER.SIZE_H.KEY] ?? 41) * zoom|0;
  return new L.Icon({
    className:   className,
    shadowUrl:   icon_path('shadow-marker'),
    shadowSize:  [size_h, size_h],
    iconUrl:     icon_path(icon),
    iconSize:    [size_w, size_h],
    iconAnchor:  [size_w/2|0, size_h],
    popupAnchor: [1, -34 * zoom|0],
  });
}


// иконка группировки
// select не имеет смысла, т.к. могут группироваться маркеры с разными id, только часть из которых sel
export function icon_get_group(color, title, select=false) {
  return new L.DivIcon({
    html: '<div style="background-color:'+color+';"><span>' + title + '</span></div>',
    className: 'marker-cluster marker-cluster-small marker-cluster-bg-new'+((select)?(' '+MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS.SEL):''),
    iconSize: new L.Point(40, 40),
  });
}


export function icon_path(name, ext='png') {
  // require('@/assets/img/markers/red.png');
  return process.env.BASE_URL+MAP_ITEM.FC.STYLE.MARKER.PATH+name+'.'+ext;
}
