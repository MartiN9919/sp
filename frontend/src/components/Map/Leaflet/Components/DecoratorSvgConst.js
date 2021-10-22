const CONST_SVG = {
  KEY_STYLE: 'style',
  KEY_DEFS:  'defs',
  DATA: {
    // скрыто
    'hidden': {
      style: 'opacity: 0;',
    },


    // штриховка: диагональные штрихи тонкие
    'hatch-diagonal-1': {
      style: 'fill: url(#{id});',
      defs: `
          <pattern id="{id}" patternUnits="userSpaceOnUse" width="4" height="4">
            <path d="M-1,1 l2,-2 M0,4 l4,-4 M3,5 l2,-2" style="stroke:{color}; stroke-width:1;" />
          </pattern>
        `,
    },


    // стрелка: <=>
    'arrow-double-end': {
      style: 'marker-end: url(#{id});',
      defs: `
        <marker id="{id}" fill="{color}" orient="auto" markerUnits='userSpaceOnUse' markerWidth='101' markerHeight='33' refX='0' refY='16.5' opacity='.5'>
          <path d='M1,17 L21,1 L21,33 Z'/>
          <path d='M101,17 L82,1 L82,33 Z'/>
          <rect x="20" y="6" width="64" height="5" />
          <rect x="20" y="23" width="64" height="5" />
        </marker>
      `,
    },




    //
    // РАЗНОЕ ДЛЯ ПРИМЕРОВ
    //

    // черта: тройная
    'dash-3': {
      style: 'marker-pattern: "40 url(#{id}_2) 40 url(#{id}_1)"',
      defs: `
        <marker id="{id}_2" orient="auto" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="12" refX="0" refY="0" viewBox="-4 -6 8 12">
          <rect x="-3" y="-5" width="2" height="10"/>
          <rect x="1" y="-5" width="2" height="10"/>
        </marker>
        <marker id="{id}_1" orient="auto" markerUnits="userSpaceOnUse" markerWidth="4" markerHeight="12" refX="0" refY="0" viewBox="-2 -6 4 12">
          <rect x="-1" y="-5" width="2" height="10"/>
        </marker>
      `,
    },


    // тест
    'fill-test': {
      style: 'fill: url(#{id});',
      defs: `
          <pattern id="{id}" fill="{color}" x="0" y="0" width="25" height="25" patternUnits="userSpaceOnUse">
            <circle cx="10" cy="10" r="10"/>
          </pattern>
        `,
    },

  },
}



// список классов в словарь строк style, defs
// return {style: '...', defs: '...'}
export function const_svg(classes_str, color="gray") {
  let ret = {style: '', defs: ''};
  let classes_list = classes_str.trim().replace(/\s+/g, ' ').split(' ');  // убрать лишние пробелы
  classes_list = [...new Set(classes_list)];                              // исключить повторы

  // перебрать классы
  classes_list.forEach(function(class_item, class_ind) {
    // для класса: стиль и defs
    let data = CONST_SVG.DATA[class_item];
    if (data === undefined) return;
    let data_style = data[CONST_SVG.KEY_STYLE];
    let data_defs  = data[CONST_SVG.KEY_DEFS ];

    // уникальный id
    let id = 'svg_'+(new Date().getTime())+'_'+class_ind;

    // заменить переменные
    if (data_style) {
      data_style = data_style.replace(/{id}/g, id).replace(/{color}/g, color);
      ret.style += '.'+class_item+' { '+data_style+' }\n';
    }

    if (data_defs) {
      data_defs = data_defs.replace(/{id}/g, id).replace(/{color}/g, color);
      ret.defs += data_defs+'\n';
    }
  });

  return ret;
}
