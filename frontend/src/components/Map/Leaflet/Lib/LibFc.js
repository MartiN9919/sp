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

    // fix bug missing properties when cut features
    let gj_copy = JSON.parse(JSON.stringify(gj));
    if (gj_copy.features) {
      gj_copy.features.forEach(function(item) {
        if (!item.properties) item.properties = {}
      });
    }

    return gj_copy;
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



// читать из FeatureCollection все features[i].properties.key
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


// задан ли FC
export function fc_exist(FC) {
  return ((FC) && (FC.features) && (FC.features.length > 0));
}
