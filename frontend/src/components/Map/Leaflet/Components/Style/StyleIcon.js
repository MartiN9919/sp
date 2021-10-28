import { MAP_CONST, MAP_ITEM } from '@/components/Map/Leaflet/Lib/Const';
import { get_icon_data } from '@/components/Map/Leaflet/Components/Style/StyleIconData';
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


export function marker_get(latlng, classes_str='', color='blue', zoom=1, param={}) {
  let icon = icon_get(classes_str, color, zoom);
  return icon_2_marker(latlng, icon, param);
}

export function icon_2_marker(latlng, icon, param={}) {
  let param_icon = (icon) ? { icon:icon, } : {};
  return L.marker(latlng, { ...param, ...param_icon, });
}




// получить иконку
export function icon_get(classes_str='', color='blue', zoom=1) {
  const separator  = MAP_CONST.CLASS.ICON.SEPARATOR;
  let classes_list = classes_str.trim().replace(/\s+/g, ' ').split(' ');  // убрать лишние пробелы
  classes_list = [...new Set(classes_list)];                              // исключить повторы
  if (color) color = color.toLowerCase();                                 // цвет к нижнему регистру

  // парсить классы
  let icon_type          = undefined;                                     // тип иконки
  let classes_icon_list  = [];                                            // классы,    связанные с иконками: [[mdi, 'flag'], ['mdi', 'spin'], ...]
  let classes_other_list = [];                                            // классы, не связанные с иконками: ['class1', ...]
  for(let class_ind=0; class_ind<classes_list.length; class_ind++) {      // классы иконки
    let class_item_str  = classes_list[class_ind];                        // название класса строкой
    let class_item_list = class_item_str.split(separator);                // название класса списком
    if (class_item_list[0] == MAP_CONST.CLASS.ICON.TYPE) {                // класс иконки
      if (icon_type == undefined) icon_type = class_item_list[1];         // тип определяется по ПЕРВОМУ классу иконки
      classes_icon_list.push(class_item_list.slice(1));
    } else {
      classes_other_list.push(class_item_str);
    }
  }
  // if (classes_icon_list.length == 0) return undefined;                 // иконки в классах не найдены - пропусить для file, т.к. задан color
  let classes_other_str = classes_other_list.join(' ');                   // неиспользованные классы строкой
  let classes_icon_str  = classes_icon_list.map((val) => val.join(separator)).join(' '); // 'mdi-flag mdi-spin' 'fs-spec0'




  // FONT: MDI
  if (icon_type == MAP_CONST.CLASS.ICON.MDI) {
    return new L.DivIcon({
      className: classes_other_str,
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


  // SVG
  if (icon_type == MAP_CONST.CLASS.ICON.SVG) {
    if (classes_icon_list.length<1) return;
    if (classes_icon_list[0].length<2) return;
    let data = get_icon_data(classes_icon_list[0][1], color, zoom);
    if (data == undefined) return;
    console.log(zoom, data.width, data.height, data.anchor_dx, data.anchor_dy)
    return new L.DivIcon({
      className:   classes_other_str,
      color:       color,
      iconSize:    [data.width,     data.height],
      iconAnchor:  [data.anchor_dx, data.anchor_dy],                         // точка привязки svg относительно верхнего левого угла
      //popupAnchor: [1,             -data.height*1.1|0],
      html:        data.svg,
    });
  }


  // FILE
  if (
    (icon_type == MAP_CONST.CLASS.ICON.FILE) ||                              // или указан тип FILE
    ((classes_icon_str == '') &&
      (COLOR_EQU[color] || Object.values(COLOR_EQU).includes(color))         // или указан color из COLOR_EQU (key или val)
    )
  ) {
    if (icon_type != MAP_CONST.CLASS.ICON.FILE) { classes_icon_list = [[undefined, color]]; }
    let file   = classes_icon_list[0][1];
    if (COLOR_EQU[file]) { file = COLOR_EQU[file]; }
    let size_w = (classes_icon_list[0][2] ?? 25) * zoom|0;
    let size_h = (classes_icon_list[0][3] ?? 41) * zoom|0;
    return new L.Icon({
      className:   classes_other_str,
      shadowUrl:   icon_file_path('shadow-marker'),
      shadowSize:  [size_h, size_h],
      iconUrl:     icon_file_path(file),
      iconSize:    [size_w,     size_h],
      iconAnchor:  [size_w/2|0, size_h],                                      // указатель: x-center, y-bottom
      popupAnchor: [1,         -size_h*1.1|0],
    });
  }


  // PULSE
  if (icon_type == MAP_CONST.CLASS.ICON.PULSE) {
    let size  = (classes_icon_list[0][1] ?? 12) * zoom|0;
    return L.icon.pulse({                                                     // или new L.Icon - в данном случае не работает
      className: classes_other_str,
      iconSize:  [size, size],
      color:     color,
      fillColor: color,
    });
  }


  // DEFAULT
  let size_w = 25 * zoom|0;
  let size_h = 41 * zoom|0;
  return new L.Icon({
      className:   classes_other_str,                                         // иначе сторонние классы не применятся
      shadowUrl:   icon_file_path('shadow-marker'),
      shadowSize:  [size_h, size_h],
      iconUrl:     icon_file_path('blue'),
      iconSize:    [size_w,     size_h],
      iconAnchor:  [size_w/2|0, size_h],                                      // указатель: x-center, y-bottom
      popupAnchor: [1,         -size_h*1.1|0],
    });
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


// цвет
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
export function icon_file_color2class(color) {
  if (color) color = color.toLowerCase();
  if (COLOR_EQU[color]) { color = COLOR_EQU[color]; }
  return
    MAP_CONST.CLASS.ICON.TYPE+
    MAP_CONST.CLASS.ICON.SEPARATOR+
    MAP_CONST.CLASS.ICON.FILE+
    MAP_CONST.CLASS.ICON.SEPARATOR+
    color;
}