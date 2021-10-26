// инициализация маркеров

import { MAP_ITEM } from '@/components/Map/Leaflet/Lib/Const';
import { Icon } from 'leaflet';



// устранение бага с путями
export function icon_ini() {
  delete Icon.Default.prototype._getIconUrl;
  Icon.Default.mergeOptions({
    iconRetinaUrl: icon_file_path('blue-2x'),
    iconUrl:       icon_file_path('blue'),
    shadowUrl:     icon_file_path('shadow-marker'),
  });
}


export function marker_get(latlng, classes_str='', color='blue', param={}) {
  let icon = icon_get(classes_str, color);
  return icon_2_marker(latlng, icon, param);
}

export function icon_2_marker(latlng, icon, param={}) {
  let param2 = (icon) ? { icon:icon, } : {};
  let ret = L.marker(latlng, { ...param, ...param2, });
  return ret
  // // класс при отсутствии иконки. Для заданных иконок он установлен в icon_get
  // if (!icon) { ret.options.icon.options.className = classes_str; }
}

// export function icon_get(style={}, className='') {
//   let color  = style [MAP_ITEM.FC.STYLE._COLOR_.KEY    ] ?? MAP_ITEM.COLOR.DEF;
//   let marker = style [MAP_ITEM.FC.STYLE.MARKER.KEY     ] ?? {};
//   let icon   = marker[MAP_ITEM.FC.STYLE.MARKER.ICON.KEY] ?? MAP_ITEM.FC.STYLE.MARKER.ICON.DEF;
//   let zoom   = marker[MAP_ITEM.FC.STYLE.MARKER.ZOOM.KEY] ?? 1;

const COLOR_EQU = {
  '#000'    : 'black',
  '#000000' : 'black',
  '#f00'    : 'red',
  '#ff0000' : 'red',
  '#0f0'    : 'green',
  '#00ff00' : 'green',
  '#00f'    : 'blue',
  '#0000ff' : 'blue',
  '#ff0'    : 'yellow',
  '#ffff00' : 'yellow',
  '#808080' : 'gray',
  '#ee82ee' : 'violet',
  '#ffd700' : 'gold',
  '#ffa500' : 'orange',
};

// получить иконку
// icon_get('icon-mdi-flag sss icon-mdi-spin tst')
// icon_get(className, color, 2);
// icon_get('', 'green'); icon_get('', '#00f');  COLOR_EQU
// icon_get();
export function icon_get(classes_str='', color='blue', zoom=1) {
  let classes_list = classes_str.trim().replace(/\s+/g, ' ').split(' ');  // убрать лишние пробелы
  classes_list = [...new Set(classes_list)];                              // исключить повторы

  // парсить классы
  let icon_type          = undefined;                                     // тип иконки
  let classes_icon_list  = [];                                            // классы,    связанные с иконками: [[mdi, 'flag'], ['mdi', 'spin'], ...]
  let classes_other_list = [];                                            // классы, не связанные с иконками: ['class1', ...]
  for(let class_ind=0; class_ind<classes_list.length; class_ind++) {      // классы иконки
    let class_item_str  = classes_list[class_ind];                        // название класса строкой
    let class_item_list = class_item_str.split('-');                      // название класса списком
    if (class_item_list[0] == MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS.ICON_TYPE) { // класс иконки
      if (icon_type == undefined) icon_type = class_item_list[1];         // тип определяется по ПЕРВОМУ классу иконки
      classes_icon_list.push(class_item_list.slice(1));
    } else {
      classes_other_list.push(class_item_str);
    }
  }
  // if (classes_icon_list.length == 0) return undefined;                 // иконки в классах не найдены - пропусить для file, т.к. задан color
  let classes_other_str = classes_other_list.join(' ');                   // неиспользованные классы строкой
  let classes_icon_str  = classes_icon_list.map((val) => val.join('-')).join(' '); // 'mdi-flag mdi-spin' 'fs-spec0'


  // FONT: MDI
  if (icon_type == MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS.ICON_TYPE_MDI) {
    return L.divIcon({
      className: classes_other_str,
      iconSize:  null,
      color:     color,
      //icon:    icon,
      html:
        '<div class="marker-font">'+
          '<div class="marker-font-content" style="border-color: '+color+';">'+
            '<span class="v-icon mdi '+classes_icon_str+'" style="color: '+color+';">'+
          '</div>'+
          '<div class="marker-font-arrow" style="border-top-color: '+color+';"></div>'+
        '</div>',
    });
    // БЕЗ FRAME
    // '<div class="marker-font" style="color: '+color+';">'+
    //   '<span class="marker-font-mdi mdi mdi-map-marker style="color: '+color+';">'+
    // '</div>',
  }


  // FONT.FS
  if (icon_type == MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS.ICON_TYPE_FS) {
    return L.divIcon({
      className: classes_other_str,
      iconSize:  null,
      color:     color,
      //icon:      icon,
      html:
        '<div class="marker-font" style="color: '+color+';">'+
          '<div class="fs '+classes_icon_str+'" style="border-color: '+color+';">'+
          '</div>'+
        '</div>',
    });
  }


  // PULSE
  if (icon_type == MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS.ICON_TYPE_PULSE) {
    let size  = (classes_icon_list[0][1] ?? 12) * zoom|0;
    return L.icon.pulse({
      className: classes_other_str,
      iconSize:  [size, size],
      color:     color,
      fillColor: color,
    });
  }


  // FILE
  if (
    (icon_type == MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS.ICON_TYPE_FILE) ||   // или указан тип: ICON_TYPE_FILE
    ((classes_icon_str == '') &&
      (COLOR_EQU[color] || Object.values(COLOR_EQU).includes(color))         // или указан color из COLOR_EQU (key или val)
    )
  ) {
    if (icon_type != MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS.ICON_TYPE_FILE) { classes_icon_list = [[undefined, color]]; }
    let file   = classes_icon_list[0][1];
    if (COLOR_EQU[file]) { file = COLOR_EQU[file]; }
    let size_w = (classes_icon_list[0][2] ?? 25) * zoom|0; //(marker[MAP_ITEM.FC.STYLE.MARKER.SIZE_W.KEY] ?? 25) * zoom|0;
    let size_h = (classes_icon_list[0][3] ?? 41) * zoom|0; //(marker[MAP_ITEM.FC.STYLE.MARKER.SIZE_H.KEY] ?? 41) * zoom|0;
    return new L.Icon({
      className:   classes_other_str,
      shadowUrl:   icon_file_path('shadow-marker'),
      shadowSize:  [size_h, size_h],
      iconUrl:     icon_file_path(file),
      iconSize:    [size_w, size_h],
      iconAnchor:  [size_w/2|0, size_h],
      popupAnchor: [1, -34 * zoom|0],
    });


  }

  return;


}


// иконка группировки
// select не имеет смысла, т.к. могут группироваться маркеры с разными id, только часть из которых sel
export function icon_group_get(color, title, select=false) {
  return new L.DivIcon({
    html: '<div style="background-color:'+color+';"><span>' + title + '</span></div>',
    className: 'marker-cluster marker-cluster-small marker-cluster-bg-new'+((select)?(' '+MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS.SEL):''),
    iconSize: new L.Point(40, 40),
  });
}


// путь к файлу иконки
export function icon_file_path(name, ext='png') {
  // require('@/assets/img/markers/red.png');
  return process.env.BASE_URL+MAP_ITEM.FC.STYLE.MARKER.PATH+name+'.'+ext;
}


// цвет
export function icon_file_color2class(color) {
  if (COLOR_EQU[color]) { color = COLOR_EQU[color]; }
  return
    MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS.ICON_TYPE+
    MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS.ICON_SEPARATOR+
    MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS.ICON_TYPE_FILE+
    MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS.ICON_SEPARATOR+
    color;
}