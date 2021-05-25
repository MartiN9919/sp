'use strict';

/*
 ОТОБРАЖЕНИЕ FEATURECOLLECTION В ВИДЕ ЦВЕТНЫХ ОБЛАСТЕЙ
 также может отображать линии и маркеры, но без цвета (их наличие не желательно)
 https://leafletjs.com/examples/choropleth/example.html
*/

class Class_leaflet_view_colors {
constructor({
    obj_id        = '',             // идентификатор объекта
    map,                            // ссылка на карту
    ajax_url      = '',             // URL ajax-запроса для получения данных (geojson FeatureCollection)
    ajax_param    = {},             // параметры ajax-запроса
    only_polygon  = true,           //*удалять линии и маркеры
    cb_data       = undefined,      //*переопределяемая callback-функция: огбработки данных ajax-запроса
    cb_color      = undefined,      //*переопределяемая callback-функция: определения цвета области в зависимости от value
    cb_style      = undefined,      //*переопределяемая callback-функция: определения стиля области
    color_begin   = '00FF00',       //*цвет: начальный
    color_end     = 'FF0000',       //*цвет: конечный
    color_inverce = false,          //*цвет: обратный порядок
    title         = undefined,      //*информатор: текст заголовока
    show_legend   = true,           //*легенда: видимость
    show_hint     = true,           //*подсказки: ключ FeatureCollection.Feature.Properties name+value
}) {
    var that                        = this;
    this.obj_id                     = obj_id;
    this.map                        = map;
    this.layer_object               = undefined;
    this.only_polygon               = only_polygon;
    this.cb_data                    = cb_data;
    this.cb_color                   = (cb_color)?cb_color:this.cb_color_default;
    this.cb_style                   = (cb_style)?cb_style:this.cb_style_default;
    this.color_begin                = (color_inverce)?color_end:color_begin;
    this.color_end                  = (color_inverce)?color_begin:color_end;
    this.title                      = title;
    this.show_hint                  = show_hint;

    this.scale_value                = [];
    this.scale_color                = [];

    // // === информатор
    // if (info_show) {
    //     this.control_info           = L.control({position: 'topright'});
    //     this.control_info.onAdd     = function (map) {
    //         this.div_info = L.DomUtil.create('div', 'info leaflet-bar');
    //         this.update();
    //         return this.div_info;
    //     };
    //     this.control_info.update    = function (properties) {
    //         this.div_info.style.display = ((that.info_title)||(properties))?'block':'none';
    //         this.div_info.innerHTML     =
    //             (that.info_title ? ('<h4>'+that.info_title+'</h4>') : '')+
    //             (properties      ? ('<b>'+properties.name+'</b><span>'+properties.value+'</span>') : '');
    //     };
    //     this.control_info.addTo(map);
    // }

    // === заголовок
    if (title) {
        this.control_title          = L.control({position: 'topright'});
        this.control_title.onAdd    = function (map) {
            this.div_info           = L.DomUtil.create('div', 'info leaflet-bar');
            this.div_info.innerHTML     = '<h4>'+that.title+'</h4>';
            this.div_info.style.display = 'block';
            return this.div_info;
        };
        this.control_title.addTo(map);
    }

    // === легенда
    if (show_legend) {
        this.control_legend         = L.control({position: 'bottomright'});
        this.control_legend.onAdd   = function (map) {
            this.div_legend = L.DomUtil.create('div', 'info leaflet-bar legend');
            return this.div_legend;
        };
        this.control_legend.update = function () {
            let labels=[], from, to;
            for (let i=0; i<that.scale_value.length; i++) {
                from = that.scale_value[i];
                to   = that.scale_value[i+1];
                labels.push('<i style="background:'+that.cb_color(that.scale_value, from+0.00000001)+'"></i> '+from+((to!=undefined)?'&ndash;'+to:'+'));
            }
            this.div_legend.innerHTML = labels.join('<br>');
        };
        this.control_legend.addTo(map);
    }

    // === ajax
    net_ajax({
        url:     ajax_url,
        success: this.data_get.bind(this),
        data:    ajax_param,
    });
}

free() {
    if (this.layer_object)   { this.layer_object.remove();   delete(this.layer_object);   }
    if (this.control_title)  { this.control_title.remove();  delete(this.control_title);  }
    if (this.control_legend) { this.control_legend.remove(); delete(this.control_legend); }
}


// data - geojson FeatureCollection
data_get(data) {
    if (this.cb_data) data = this.cb_data(data);
    if (!data) return;

    // исключить ненужные геометрии
    if (this.only_polygon) fc_types_del(data, ['LineString', 'Point']);

    // properties к стандартным наименованиям
    fc_rename(data, KEY.TEST_GEO_COLOR, FC_PROPERTIES.COLOR);

    this.scale_value  = scale_log(fc_key(data, FC_PROPERTIES.COLOR));
    this.scale_color  = color_array(this.color_begin, this.color_end, this.scale_value.length);

    if (this.control_legend) this.control_legend.update();
    this.layer_object = L.geoJson(data, {
        style:         this.cb_style.bind(this),
        onEachFeature: this.onEachFeature.bind(this),
    }).addTo(this.map);
}

cb_color_default(scale_value, value) {
    let ret = this.scale_color[scale_value.length-1];
    for (let i=0; i<this.scale_value.length-1; i++) {
        if (value >= this.scale_value[i] && value < this.scale_value[i+1]) {
            ret = this.scale_color[i];
            break;
        }
    }
    return '#'+ret;
}
cb_style_default(feature) {
    return {
        weight:     2,
        opacity:    1,
        color:      'white',
        dashArray:  '3',
        fillOpacity: 0.4,
        fillColor:   this.cb_color(this.scale_value, feature.properties[FC_PROPERTIES.COLOR][FC_PROPERTIES.IND.VAL]),
    };
}
onEachFeature(feature, layer) {
    layer.on({
        mouseover: this.on_mouse_over.bind(this),
        mouseout:  this.on_mouse_out .bind(this),
        click:     this.on_click     .bind(this),
    });

    if (this.show_hint) {
        let prop     = feature.properties;
        if (FC_PROPERTIES.NAME in prop && FC_PROPERTIES.COLOR in prop) {
            let is_point = (feature.geometry.type=='Point');
            layer.bindTooltip('<b>'+prop[FC_PROPERTIES.NAME][FC_PROPERTIES.IND.VAL]+'</b></br><span>'+prop[FC_PROPERTIES.COLOR][FC_PROPERTIES.IND.VAL]+'</span>', {
                permanent: false,
                sticky:    false,
                direction: is_point?'right':'center',
                opacity:   0.8,
                offset:    is_point?L.point(20, 0):L.point(0, 0),
            });
        }
    }

}
on_mouse_over(e) {
    var layer = e.target;
    layer.setStyle({
        weight:      5,
        color:       '#888',
        dashArray:   '',
        fillOpacity: 0.7,
    });
    layer.bringToFront(); //if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) { layer.bringToFront(); }
    //if (this.control_info) this.control_info.update(layer.feature.properties);
}
on_mouse_out(e) {
    this.layer_object.resetStyle(e.target);
    //if (this.control_info) this.control_info.update();
}
on_click(e) {
    this.map.fitBounds(e.target.getBounds());
}


}