import { MAP_ITEM } from '@/components/Map/Leaflet/Lib/Const';
import { dict_get } from '@/components/Map/Leaflet/Lib/Lib';

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
      type: MAP_ITEM.FC.TYPE.VAL,
      features: [{
        type: 'Feature',
        properties: {},
        geometry: gj,
      }]
    };
  } else if (type === 'feature') {
    return {
      type: MAP_ITEM.FC.TYPE.VAL,
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
    type: MAP_ITEM.FC.TYPE.VAL,
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



// читать из FeatureCollection: список features[i].properties.key
export function fc_properties_keys_get(FC, key) {
  let ret = [];
  for (let i=0; i<FC.features.length; i++) {
    let val = FC.features[i].properties[key];
    if (val != undefined) ret.push(val);
  }
  return ret;
}


// удалить из FeatureCollection: объекты типов types_del ['LineString', 'Point', ...]
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


// читать из Feature: список feature.properties.class
export function get_feature_class(feature) {
  let ret = dict_get(feature, [MAP_ITEM.FC.FEATURES.PROPERTIES.KEY, MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS.KEY], '');
  return ret.trim().replace(/\s+/g, ' ');
}


// читать из Feature: список feature.geometry.coordinates
// invert  - поменять местами x и y
export function get_feature_coordinates(feature, invert=false) {
  let ret = {
    [MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE.POINT]: [],
    [MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE.LINE]: [],
    [MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE.POLYGON]: [],
  }

  //=========================================================
  // разбор одной записи
  //=========================================================
  function parse_item(item_geometry) {
    let item_type        = item_geometry[MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE.KEY];
    let item_coordinates = item_geometry[MAP_ITEM.FC.FEATURES.GEOMETRY.COORDINATES.KEY] ?? {};

    if (invert) {
      switch (item_type) {
        case MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE.POINT:                                  // для точек [x,y]
          item_coordinates = [item_coordinates[1], item_coordinates[0]];
          break;
        case MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE.LINE:                                   // для линий [[x,y],...]
          item_coordinates = item_coordinates.map((val) => { return [val[1], val[0]] });
          break;
        case MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE.POLYGON:                                // для полигонов [[[x,y],...],...]
          if (invert) {
            for(let i=0; i<item_coordinates.length;i++) {
              item_coordinates[i] = item_coordinates[i].map((val) => { return [val[1], val[0]] });
            }
          }
          break;
      }
    }

    ret[item_type].push(item_coordinates);
  }
  //=========================================================


  let geometry      = feature[MAP_ITEM.FC.FEATURES.GEOMETRY.KEY];
  let geometry_type = geometry[MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE.KEY];

  // GeometryCollection: вложенные геометрии
  if (geometry_type == MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE.GC) {
    for(let i=0; i<geometry[MAP_ITEM.FC.FEATURES.GEOMETRY.GEOMETRIES.KEY].length; i++) {
      parse_item(geometry[MAP_ITEM.FC.FEATURES.GEOMETRY.GEOMETRIES.KEY][i]);
    }
  }

  // Point, LineString, Polygon
  else { parse_item(geometry); }

  return ret;
}
