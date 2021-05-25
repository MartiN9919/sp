'use strict';

class Class_leaflet_view_base {
constructor({
    obj_id        = '',             // идентификатор объекта
    map,                            // ссылка на карту
    ajax_url      = '',             // URL ajax-запроса для получения данных (geojson FeatureCollection)
    ajax_param    = {},             // параметры ajax-запроса
    cb_data       = undefined,      //*переопределяемая callback-функция: огбработки данных ajax-запроса
    cb_style      = undefined,      //*переопределяемая callback-функция: определения стиля области
    cb_marker     = undefined,      //*переопределяемая callback-функция: выбор маркера
    marker_icon   = undefined,      //*маркер по умолчанию
    marker_item   = undefined,      //*класс-маркер [L.Marker]
    marker_group  = undefined,      //*класс-группа
    title         = undefined,      //*информатор: текст заголовока
    hint          = undefined,      //*подсказки: ключ FeatureCollection.Feature.Properties  например: address
}) {
    var that                        = this;
    this.obj_id                     = obj_id;
    this.map                        = map;
    this.layer_object               = undefined;
    this.cb_data                    = cb_data;
    this.cb_style                   = (cb_style )?cb_style :this.cb_style_default .bind(this);
    this.cb_marker                  = (cb_marker)?cb_marker:this.cb_marker_default.bind(this);
    this.marker_icon                = marker_icon;
    this.marker_item                = (marker_item)?marker_item:L.Marker;
    this.marker_group               = marker_group;
    this.title                      = title;
    this.hint                       = hint;

    this.scale_value                = [];
    this.scale_color                = [];

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

    // === ajax
    net_ajax({
        url:     ajax_url,
        data:    ajax_param,
        success: this.data_get.bind(this),
    });
}

free() {
    if (this.layer_object)   { this.layer_object .remove();   delete(this.layer_object ); }
    if (this.control_title)  { this.control_title.remove();   delete(this.control_title); }
}

// data - geojson FeatureCollection
data_get(data) {
    if (this.cb_data) { data = this.cb_data(data); }
    if (!data) return;

    this.group  = (this.marker_group)?new this.marker_group():undefined;
    this.layers = L.geoJson(data, {
        style:         this.cb_style,
        pointToLayer:  this.cb_marker,
        onEachFeature: this.onEachFeature.bind(this),
    });
    this.layer_object = (this.group)?this.group.addTo(this.map):this.layers.addTo(this.map);
}

cb_style_default(feature) {
    return {
        weight:      2,
        fillOpacity: 0.1,
        fillColor:   '#aaf',
    };
}

onEachFeature(feature, layer) {
    if (this.group) { layer.addTo(this.group); }
    if (this.hint) {
        let prop = feature.properties;
        if (this.hint in prop) {
            let is_point = (feature.geometry.type=='Point');
            layer.bindTooltip(prop[this.hint][0], {
                permanent: false,
                sticky:    false,
                direction: is_point?'right':'center',
                opacity:   0.8,
                offset:    is_point?L.point(20, 0):L.point(0, 0),
            });
        }
    }
}

cb_marker_default(feature, latlng) {
    return new this.marker_item(latlng, {icon: this.marker_icon });
}

}