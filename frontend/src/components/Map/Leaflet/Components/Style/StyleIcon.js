import { Icon } from 'leaflet';
import { MAP_CONST, MAP_ITEM } from '@/components/Map/Leaflet/Lib/Const';
import { get_style_data_icon } from '@/components/Map/Leaflet/Components/Style/StyleData';



// устранение бага с путями
export function icon_ini() {
  delete Icon.Default.prototype._getIconUrl;
  Icon.Default.mergeOptions({
    iconRetinaUrl: icon_file_path('blue-2x'),
    iconUrl:       icon_file_path('blue'),
    shadowUrl:     icon_file_path('shadow-marker'),
  });
}


export function marker_get(latlng, icon_color=undefined, icon_properties={}, zoom_map=undefined, marker_param={}) {
  let icon = icon_get(icon_color, icon_properties, zoom_map);
  return icon_2_marker(latlng, icon, marker_param);
}

export function icon_2_marker(latlng, icon, param={}) {
  let param_icon = (icon) ? { icon:icon, } : {};
  return L.marker(latlng, { ...param, ...param_icon, });
}




/* получить иконку
 * icon_properties - из fc.features[].properties
 * class    = '', тип иконки определяется по ПЕРВОМУ классу иконки
 * text     = undefined
 * zoom     = undefined (автоматическое определение), false, 1.2
 */
export function icon_get(icon_color=undefined, icon_properties={}, zoom_map=undefined) {
  // классы, тип иконки
  const classes_str  = icon_properties.class ?? '';                             // классы строкой
  let   classes_list = classes_str.trim().replace(/\s+/g, ' ').split(' ');      // классы списком
  classes_list = [...new Set(classes_list)];                                    // исключить повторы
  let icon_type          = undefined;                                           // тип иконки
  let classes_icon_list  = [];                                                  // классы,    связанные с иконками: [[mdi, 'flag'], ['mdi', 'spin'], ...]
  let classes_other_list = [];                                                  // классы, не связанные с иконками: ['class1', ...]
  for(let class_ind=0; class_ind<classes_list.length; class_ind++) {            // классы иконки
    let class_item_str  = classes_list[class_ind];                              // название класса строкой
    let class_item_list = class_item_str.split(MAP_CONST.CLASS.ICON.SEPARATOR); // название класса списком
    if (class_item_list[0] == MAP_CONST.CLASS.ICON.TYPE) {                      // класс иконки
      if (icon_type == undefined) icon_type = class_item_list[1];               // тип иконки определяется по ПЕРВОМУ классу иконки
      classes_icon_list.push(class_item_list.slice(1));
    } else {
      classes_other_list.push(class_item_str);
    }
  }
  if (icon_type == undefined) {                                                 // тип иконки не задан: стандартная иконка SVG
    icon_type = MAP_CONST.CLASS.ICON.SVG;
    classes_icon_list.push([MAP_CONST.CLASS.ICON.SVG,MAP_CONST.CLASS.ICON.SVG_STANDART]);
  }
  const classes_other_str = classes_other_list.join(' ');                       // неиспользованные классы строкой
  const classes_icon_str  = classes_icon_list.map((val) => val.join(MAP_CONST.CLASS.ICON.SEPARATOR)).join(' '); // 'mdi-flag mdi-spin' 'fs-spec0'

  // остальные опции
  const text   = icon_properties[MAP_ITEM.FC.FEATURES.PROPERTIES.TEXT];         // иконка: надпись
  const rotate = icon_properties[MAP_ITEM.FC.FEATURES.PROPERTIES.ROTATE];       // иконка: поворот
  const color  =                                                                // иконка: цвет, приоритет fc.prop.color перед цветом скрипта
    ( icon_properties[MAP_ITEM.FC.FEATURES.PROPERTIES.COLOR] != undefined) ?
      icon_properties[MAP_ITEM.FC.FEATURES.PROPERTIES.COLOR] :
    ((icon_color ?? MAP_CONST.COLOR.DEFAULT_STYLE_ICON).toLowerCase());
  const zoom   =                                                                // иконка: масштаб
    (icon_properties[MAP_ITEM.FC.FEATURES.PROPERTIES.ZOOM] != undefined) ?
      ((icon_properties[MAP_ITEM.FC.FEATURES.PROPERTIES.ZOOM] !== false) ? icon_properties[MAP_ITEM.FC.FEATURES.PROPERTIES.ZOOM] : 1):
      ((zoom_map < MAP_CONST.CLASS.ICON.SVG_ZOOM_START) ? Math.pow(2.0, zoom_map-MAP_CONST.CLASS.ICON.SVG_ZOOM_START) : 1);


  // FILE
  if (icon_type == MAP_CONST.CLASS.ICON.FILE) {
    let file   =  classes_icon_list[0][1];
    let size_w = (classes_icon_list[0][2] ?? 25) * zoom|0;
    let size_h = (classes_icon_list[0][3] ?? 41) * zoom|0;
    return new L.Icon({
      className:   classes_other_str,                                           // иначе сторонние классы не применятся
      shadowUrl:   icon_file_path('shadow-marker'),
      shadowSize:  [size_h, size_h],
      iconUrl:     icon_file_path(file),
      iconSize:    [size_w,     size_h],
      iconAnchor:  [size_w/2|0, size_h],                                        // указатель: x-center, y-bottom
      popupAnchor: [1,         -size_h*1.1],
    });
  }


  // FONT: MDI
  if (icon_type == MAP_CONST.CLASS.ICON.MDI) {
    return new L.DivIcon({
      className: classes_other_str,                                             // иначе сторонние классы не применятся
      iconSize:  null,
      color:     color,
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
  if (icon_type == MAP_CONST.CLASS.ICON.FS) {
    return new L.DivIcon({
      className: classes_other_str,
      iconSize:  null,
      color:     color,
      html:
        '<div class="marker-font" style="color: '+color+';">'+
          '<div class="fs '+classes_icon_str+'" style="border-color: '+color+';">'+
          '</div>'+
        '</div>',
    });
  }


  // PULSE
  if (icon_type == MAP_CONST.CLASS.ICON.PULSE) {
    let size  = (classes_icon_list[0][1] ?? 12) * zoom|0;
    return L.icon.pulse({                                                         // или new L.Icon - в данном случае не работает
      className: classes_other_str,
      iconSize:  [size, size],
      color:     color,
      fillColor: color,
    });
  }


  // SVG (DEFAULT)
  if (icon_type == MAP_CONST.CLASS.ICON.SVG) {
    if (classes_icon_list.length<1) return;
    if (classes_icon_list[0].length<2) return;
    let data = get_style_data_icon({
      class_item: classes_icon_list[0][1],
      color:      color,
      zoom:       zoom,
      rotate:     rotate,
      text:       text,
    });

    if (data == undefined) return;
    // let shadow =  (icon_properties[MAP_ITEM.FC.FEATURES.PROPERTIES.SHADOW] !== false);
    let class_top    =  (icon_properties[MAP_ITEM.FC.FEATURES.PROPERTIES.TOP   ] ===  true) ? ' svg-top' : '';
    let class_shadow =  (icon_properties[MAP_ITEM.FC.FEATURES.PROPERTIES.SHADOW] ==  'red') ? ' svg-shadow-red' :
                       ((icon_properties[MAP_ITEM.FC.FEATURES.PROPERTIES.SHADOW] !== false) ? ' svg-shadow'     : '');
    return new L.DivIcon({
      className:   classes_other_str+class_shadow+class_top,
      iconSize:    [data.width,     data.height],
      iconAnchor:  [data.anchor_dx, data.anchor_dy],                            // точка привязки svg относительно верхнего левого угла
      popupAnchor: [1,             -data.height*1.1],
      html:        data.svg,
    });
  }
}


// иконка группировки
// select не имеет смысла, т.к. могут группироваться маркеры с разными id, только часть из которых sel
export function icon_group_get(color, title, select=false) {
  return new L.DivIcon({
    html: '<div style="background-color:'+color+';"><span>' + title + '</span></div>',
    className: 'marker-cluster marker-cluster-small marker-cluster-bg-new'+((select)?(' '+MAP_CONST.CLASS.SEL):''),
    iconSize: new L.Point(40, 40),
  });
}


// путь к файлу иконки
export function icon_file_path(name, ext='png') {
  // require('@/assets/img/markers/red.png');
  return process.env.BASE_URL+MAP_CONST.CLASS.ICON.PATH+name+'.'+ext;
}
