/**
 * Normalize a GeoJSON feature into a FeatureCollection.
 *
 * @param {object} gj geojson data
 * @returns {object} normalized geojson data
 */
export function fc_normalize(gj) {
  const types = {
    Point: 'geometry',
    MultiPoint: 'geometry',
    LineString: 'geometry',
    MultiLineString: 'geometry',
    Polygon: 'geometry',
    MultiPolygon: 'geometry',
    GeometryCollection: 'geometry',
    Feature: 'feature',
    FeatureCollection: 'featurecollection'
  };

  if (!gj || !gj.type) return null;
  var type = types[gj.type];
  if (!type) return null;

  if (type === 'geometry') {
    return {
      type: 'FeatureCollection',
      features: [{
        type: 'Feature',
        properties: {},
        geometry: gj,
      }]
    };
  } else if (type === 'feature') {
    return {
      type: 'FeatureCollection',
      features: [gj],
    };
  } else if (type === 'featurecollection') {
    return gj;
  }
}


/**
 * Merge a series of GeoJSON objects into one FeatureCollection containing all
 * features in all files.  The objects can be any valid GeoJSON root object,
 * including FeatureCollection, Feature, and Geometry types.
 *
 * @param {Array<Object>} inputs a list of GeoJSON objects of any type
 * @return {Object} a geojson FeatureCollection.
 * @example
 * var geojsonMerge = require('@mapbox/geojson-merge');
 *
 * var mergedGeoJSON = geojsonMerge.merge([
 *   { type: 'Point', coordinates: [0, 1] },
 *   { type: 'Feature', geometry: { type: 'Point', coordinates: [0, 1] }, properties: {} }
 * ]);
 *
 * console.log(JSON.stringify(mergedGeoJSON));
 */
export function fc_merge (inputs) {
  let output = {
    type: 'FeatureCollection',
    features: []
  };
  for (let i = 0; i < inputs.length; i++) {
    let fc = fc_normalize(inputs[i]);
    for (var j = 0; j < fc.features.length; j++) {
      output.features.push(fc.features[j]);
    }
  }
  return output;
}



// читать мз FeatureCollection properties.key
export function fc_key(FC, key) {
  let ret = [];
  for (let i=0; i<FC.features.length; i++) {
    ret.push(FC.features[i].properties[key]);
  }
  return ret;
}


// удалить из FeatureCollection объекты типов types_del ['LineString', 'Point', ...]
export function fc_types_del(FC, types_del) {
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
export function scale_log(data) {
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
    let scale       = data_log.slice(ind_min_log, ind_max_log);   // ind_max_log+1
    for (let i=scale.length-2; i>=0; i--) {
        if (data.filter(v => ((v>=scale[i])&&(v<scale[i+1]))).length==0) { scale.splice(i, 1); }
    }
    return scale;
}

// массив промежуточных цветов из len элементов, включая начальный и конечный цвета
// color_array('FF9900', '66FF33', 4);
export function color_array(color_begin, color_end, len) {
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
