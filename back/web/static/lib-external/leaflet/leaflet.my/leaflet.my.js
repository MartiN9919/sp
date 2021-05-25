'use strict';

class Class_leaflet {
constructor(id_parent) {
    var that = this;
    this.id_parent          = id_parent;
    this.map                = L.map(id_parent, {zoomControl: false, editable: true}).setView([53.783, 27.974], 7);
    this.elements           = {};
    this.markers            = {};
    this.ELEMENT_LAYER_DATA = 'layer_data';
    this.leaflet_markers    = new Class_leaflet_markers(this);


    // event: on_click
    this.map.on('click', function(e) {
        var coord = e.latlng;
        var lat = coord.lat;
        var lng = coord.lng;
        console.log("You clicked the map at latitude: " + lat + " and longitude: " + lng);
    });

    // event: on_resize
    this.resize_bind       = this.resize.bind(this);
    this.resize_timer_bind = this.resize_timer.bind(this);
    this.resize_timer(undefined);
    window.addEventListener('resize', this.resize_timer_bind, false);
}


//* SCALE
control_scale_add(position='bottomright') { this.elements['scale'] = L.control.scale({metric: true, imperial: false, position: position, }).addTo(this.map); }


//* TILE
layer_tile_set(url) {
    if ('tile' in this.elements) this.element_del('tile');
    this.elements['tile'] = new L.TileLayer(url, {attribution: '&copy; Госпогранкомитет РБ'});
    this.map.addLayer(this.elements['tile']);
}


//* DEL (LAYER, CONTROL)
element_del(element_name) {
    if (element_name in this.elements) { this.elements[element_name].remove(); delete(this.elements[element_name]); }
    else console.error('Не верное название элемента:', element_name);
    //this.map.removeLayer(this.elements[element_name]);
}


//* ENENT RESIZE
resize_timer(element) { setTimeout(this.resize_bind, 100); }
resize(element)       { this.map.invalidateSize(); }


};



/*
 *  DATA
 */
// данные на карту
// data_set(data) { this.layer_polygon_add('edit', data); }
// data_set(data, editing = true) {
//     this.data = data;
//     if (editing) {
//         this.edit_control_on(this.data);
//         return;
//     }

//     // не понимает geojsonFeature, а только geometrycollection
//     // this.elements[this.ELEMENT_LAYER_DATA] = L.GeoJSON.geometryToLayer(this.data);
//     // this.elements[this.ELEMENT_LAYER_DATA].addTo(this.map);

//     // this.elements[this.ELEMENT_LAYER_DATA] = L.geoJSON().addTo(this.map);
//     // this.elements[this.ELEMENT_LAYER_DATA].addData(this.data);

//     try {
//         this.elements[this.ELEMENT_LAYER_DATA] = (this.data.type=='FeatureCollection')?L.geoJSON(this.data):L.GeoJSON.geometryToLayer(this.data);
//         this.elements[this.ELEMENT_LAYER_DATA].addTo(this.map);
//     } catch {
//         alertify.error('Ошибка в данных!');
//     }
// }
// данные с карты
// data_get() {
//     return this.elements[this.ELEMENT_LAYER_DATA].toGeoJSON();
// }
// удалить слой данных и сами данные
// data_clear() {
//     if (this.elements[this.ELEMENT_LAYER_DATA])
//         this.elements[this.ELEMENT_LAYER_DATA].clearLayers();
//         delete this.elements[this.ELEMENT_LAYER_DATA];
//     if (this.data) delete this.data;
//}

// // вставка картинки
// var imageUrl = '/static/img/bg/bg-home.jpg';
// var imageBounds = [[17.342761, 78.552432], [16.396553, 80.727725]];
// var overlay = L.imageOverlay(imageUrl, imageBounds);
// overlay.addTo(this.map);



/*
 * ============================
 * ВНЕ КЛАССА
 * ============================
 */
// переименовать FeatureCollection properties.key_from -> properties.key_to
function fc_rename(FC, key_from, key_to) {
    for (let i=0; i<FC.features.length; i++) {
        if (FC.features[i].properties[key_from]) {
            FC.features[i].properties[key_to] = FC.features[i].properties[key_from];
            delete FC.features[i].properties[key_from];
        }
    }
    return FC;
}



// читать мз FeatureCollection properties.key
function fc_key(FC, key) {
    let ret = [];
    for (let i=0; i<FC.features.length; i++) {
        ret.push(FC.features[i].properties[key][FC_PROPERTIES.IND.VAL]);
    }
    return ret;
}


// удалить из FeatureCollection объекты типов types_del []
function fc_types_del(FC, types_del) {
    for (let key in FC) {
        // недопустимые типы удалить
        if (key=='type') {
            if (types_del.indexOf(FC[key])>-1) return false;
        }
        // рекурсия
        if (typeof(FC[key])==='object') {
            if (!fc_types_del(FC[key], types_del)) delete(FC[key]);
        }
    }
    return true;
}


// ЛОГАРИФМИЧЕСКАЯ ШКАЛА ДЛЯ data
function scale_log(data) {
    const data_log = [
       -100000000000, -200000000000, -500000000000,
       -10000000000,  -20000000000,  -50000000000,
       -1000000000,   -2000000000,   -5000000000,
       -100000000,    -200000000,    -500000000,
       -10000000,     -20000000,     -50000000,
       -1000000,      -2000000,      -5000000,
       -100000,       -200000,       -500000,
       -10000,        -20000,        -50000,
       -1000,         -2000,         -5000,
       -100,          -200,          -500,
       -10,           -20,           -50,
       -1,            -2,            -5,
       -0.1,          -0.2,          -0.5,
       -0.01,         -0.02,         -0.05,
       -0.001,        -0.002,        -0.005,
       -0.0001,       -0.0002,       -0.0005,
       -0.00001,      -0.00002,      -0.00005,
       -0.000001,     -0.000002,     -0.000005,
       -0.0000001,    -0.0000002,    -0.0000005,
        0,
        0.0000001,     0.0000002,     0.0000005,
        0.000001,      0.000002,      0.000005,
        0.00001,       0.00002,       0.00005,
        0.0001,        0.0002,        0.0005,
        0.001,         0.002,         0.005,
        0.01,          0.02,          0.05,
        0.1,           0.2,           0.5,
        1,             2,             5,
        10,            20,            50,
        100,           200,           500,
        1000,          2000,          5000,
        10000,         20000,         50000,
        100000,        200000,        500000,
        1000000,       2000000,       5000000,
        10000000,      20000000,      50000000,
        100000000,     200000000,     500000000,
        1000000000,    2000000000,    5000000000,
        10000000000,   20000000000,   50000000000,
        100000000000,  200000000000,  500000000000,
        1000000000000, 2000000000000, 5000000000000,
    ];
    let val_min     = Math.min(... data);
    let val_max     = Math.max(... data);
    let val_min_log = Math.max(... data_log.filter(v => v <= val_min));
    let val_max_log = Math.min(... data_log.filter(v => v >  val_max));
    if (!isFinite(val_min_log)) val_min_log = data_log[0];
    if (!isFinite(val_max_log)) val_max_log = data_log[data_log.length-1];
    let ind_min_log = data_log.indexOf(val_min_log);
    let ind_max_log = data_log.indexOf(val_max_log);
    let scale       = data_log.slice(ind_min_log, ind_max_log);
    for (let i=scale.length-2; i>=0; i--) {
        if (data.filter(v => ((v>=scale[i])&&(v<scale[i+1]))).length==0) { scale.splice(i, 1); }
    }
    return scale;
}

// массив промежуточных цветов из len элементов, включая начальный и конечный цвета
// color_array('FF9900', '66FF33', 4);
function color_array(color_begin, color_end, len) {
    let ret = [color_begin];
    for (let i=1; i<=len-2; i++) {
        ret.push(color_mid(color_begin, color_end, 1.0*i/(len-1)));
    }
    ret.push(color_end);
    return ret;
}
function color_mid(color_begin, color_end, k) {
    function color_mid_dig(color_begin, color_end, k) { return ('0'+Math.round(parseInt(color_begin,16)*(1-k)+parseInt(color_end,16)*k).toString(16)).slice(-2); }
    let ret = '';
    for (let i=0; i<3; i++) { ret += color_mid_dig(color_begin.substr(i*2,2), color_end.substr(i*2,2), k); }
    return ret;
}
