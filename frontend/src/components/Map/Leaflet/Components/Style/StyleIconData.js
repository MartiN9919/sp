
import { MAP_ITEM } from '@/components/Map/Leaflet/Lib/Const';

// "icon": "test",     // "mdi-flag mdi-spin", "fs-spec0", "pulse" (size: 12), "#0f0", "gold", "file_name" (size_w: 25, size_h: 41)


// const DATA_ICON = {
//   DATA: {
//     [MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS.ICON_TYPE_MDI]: {
//       //type:     'icon_div',
//       iconSize: null,
//       //icon:     'mdi-flag',
//       html:
//         '<div class="marker-font">'+
//           '<div class="marker-font-content" style="border-color: {color};">'+
//             '<span class="v-icon mdi {icon}" style="color: {color};">'+
//           '</div>'+
//           '<div class="marker-font-arrow" style="border-top-color: {color};"></div>'+
//         '</div>',
//     },

//   },
// }

const COLOR_EQU = {
  '#000': 'black',
  '#f00': 'red',
  '#0f0': 'green',
  '#00f': 'blue',
};

// получить иконку
// используется только первый совпавший класс из списка допустимых
export function get_icon(classes_str='', color='blue', zoom=1) {
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
  if (classes_icon_list.length == 0) return undefined;                    // иконки в классах не найдены
  let classes_other_str = classes_other_list.join(' ');
  let classes_icon_str;
  let ret = undefined;
  switch (icon_type) {


    // FONT: MDI
    case MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS.ICON_TYPE_MDI:
      classes_icon_str  = classes_icon_list.map((val) => val.join('-')).join(' '); // 'mdi-flag mdi-spin'
      ret = L.divIcon({
        className: classes_other_str,                                     // неиспользованные классы
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
      break;
      // БЕЗ FRAME
      // '<div class="marker-font" style="color: '+color+';">'+
      //   '<span class="marker-font-mdi mdi mdi-map-marker style="color: '+color+';">'+
      // '</div>',


    // FONT.FS
    case MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS.ICON_TYPE_FS:
      classes_icon_str  = classes_icon_list.map((val) => val.join('-')).join(' '); // 'fs-spec0'
      ret = L.divIcon({
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
      break;


    // PULSE
    case MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS.ICON_TYPE_PULSE:
      let size  = (classes_icon_list[0][1] ?? 12) * zoom|0;
      ret = L.icon.pulse({
        className: classes_other_str,
        iconSize:  [size, size],
        color:     color,
        fillColor: color,
      });
      break;


    // FILE
    case MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS.ICON_TYPE_FILE:
      let file   = classes_icon_list[0][1];
      if (COLOR_EQU[file]) { file = COLOR_EQU[file]; }
      let size_w = (classes_icon_list[0][2] ?? 25) * zoom|0; //(marker[MAP_ITEM.FC.STYLE.MARKER.SIZE_W.KEY] ?? 25) * zoom|0;
      let size_h = (classes_icon_list[0][3] ?? 41) * zoom|0; //(marker[MAP_ITEM.FC.STYLE.MARKER.SIZE_H.KEY] ?? 41) * zoom|0;
      ret = new L.Icon({
        className:   classes_other_str,
        shadowUrl:   icon_file_path('shadow-marker'),
        shadowSize:  [size_h, size_h],
        iconUrl:     icon_file_path(file),
        iconSize:    [size_w, size_h],
        iconAnchor:  [size_w/2|0, size_h],
        popupAnchor: [1, -34 * zoom|0],
      });


  }

  return ret;


}


export function icon_file_path(name, ext='png') {
  // require('@/assets/img/markers/red.png');
  return process.env.BASE_URL+MAP_ITEM.FC.STYLE.MARKER.PATH+name+'.'+ext;
}
