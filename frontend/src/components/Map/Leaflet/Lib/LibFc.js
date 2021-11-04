import { MAP_CONST, MAP_ITEM } from '@/components/Map/Leaflet/Lib/Const';
import { dict_get, str_cut }   from '@/components/Map/Leaflet/Lib/Lib';



/**
 * Установить hint
 * only_parent = true - устанавливать для вложенных слоев (GeometryCollection)
 */
export function set_feature_hint(layer, fc_properties, only_parent=false) {
  let text = fc_properties[MAP_ITEM.FC.FEATURES.PROPERTIES.TEXT] ?? '';
  let date = fc_properties[MAP_ITEM.FC.FEATURES.PROPERTIES.DATE] ?? '';
  let hint = fc_properties[MAP_ITEM.FC.FEATURES.PROPERTIES.HINT] ?? '';
  let val  =
    ((text != '') ? ('<span style="font-weight: bold;background: #eee;width: 100%;display: inline-block;">'+str_cut(text, 100)+'</span><br>') : '')+
    ((date != '') ? (date+'<br>') : '')+
    str_cut(hint, 100).replace(/\n/, '<br>');
  if (val == '') return;

  function set_hint(layer_item) {
    layer_item.bindTooltip('<div style="white-space: nowrap;">' + val + '</div>', {permanent: false, sticky: true, });
  }
  if ((only_parent==false) && (layer.hasOwnProperty('_layers'))) {
    for(let tempLayer in layer._layers) { set_hint(layer._layers[tempLayer]); }
  }
  else {
    set_hint(layer);
  };
}




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
  } else if (type.toLowerCase() === 'featurecollection') {

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
    features: [],
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
  if (FC.type.toLowerCase() !== 'featurecollection') return;

  for(let i=FC.features.length-1; i>=0; i--) {
    if (types_del.indexOf(FC.features[i].geometry.type)>-1) {
      FC.features.splice(i, 1);
    }
  }
}


// задан ли FC
export function fc_exist(FC) {
  return ((FC) && (FC.features) && (FC.features.length > 0));
}


// читать из Feature: список feature.properties.class
export function get_feature_class(feature) {
  let ret = dict_get(feature, ['properties', MAP_ITEM.FC.FEATURES.PROPERTIES.CLASS], '');
  return ret.trim().replace(/\s+/g, ' ');
}


// читать из Feature: список feature.geometry.coordinates
// invert  - поменять местами x и y
export function get_feature_coordinates(feature, invert=false) {
  let ret = {
    [MAP_CONST.TYPE_GEOMETRY.POINT]: [],
    [MAP_CONST.TYPE_GEOMETRY.LINE]: [],
    [MAP_CONST.TYPE_GEOMETRY.POLYGON]: [],
  }

  //=========================================================
  // разбор одной записи
  //=========================================================
  function parse_item(item_geometry) {
    let item_type        = item_geometry[MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE];
    let item_coordinates = item_geometry[MAP_ITEM.FC.FEATURES.GEOMETRY.COORDINATES] ?? {};

    if (invert) {
      switch (item_type) {
        case MAP_CONST.TYPE_GEOMETRY.POINT:                                             // для точек [x,y]
          item_coordinates = [item_coordinates[1], item_coordinates[0]];
          break;
        case MAP_CONST.TYPE_GEOMETRY.LINE:                                              // для линий [[x,y],...]
          item_coordinates = item_coordinates.map((val) => { return [val[1], val[0]] });
          break;
        case MAP_CONST.TYPE_GEOMETRY.POLYGON:                                           // для полигонов [[[x,y],...],...]
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


  let geometry      = feature.geometry;
  let geometry_type = geometry[MAP_ITEM.FC.FEATURES.GEOMETRY.TYPE];

  // GeometryCollection: вложенные геометрии
  if (geometry_type == MAP_CONST.TYPE_GEOMETRY.GC) {
    for(let i=0; i<geometry[MAP_ITEM.FC.FEATURES.GEOMETRY.GEOMETRIES].length; i++) {
      parse_item(geometry[MAP_ITEM.FC.FEATURES.GEOMETRY.GEOMETRIES][i]);
    }
  }

  // Point, LineString, Polygon
  else { parse_item(geometry); }

  return ret;
}
