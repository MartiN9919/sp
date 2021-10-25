
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


// получить иконку
// используется только первый совпавший класс из списка допустимых
export function data_icon(classes_str, color="blue", zoom=1) {
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

  let ret = undefined;
  switch (icon_type) {

    // FONT: MDI
    case MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS.ICON_TYPE_MDI:
      let classes_icon_str  = classes_icon_list.map((val) => val.join('-')).join(' '); // 'mdi-flag mdi-spin'
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

  }

  return ret;


}



    // icon_type  = class_item_list.slice(0,2).join('-');                    // первых два элемента - тип иконки
    // icon_param = class_item_list.slice(2);                                // остальное: параметры иконки (зависят от типа иконки)
    // break
