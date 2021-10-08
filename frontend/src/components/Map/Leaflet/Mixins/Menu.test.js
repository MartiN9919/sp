import { MAP_ITEM } from '@/components/Map/Leaflet/Lib/ConstOld';
// import { MAP_STYLE } from '@/components/Map/Leaflet/Lib/Const';
// var STYLE = MAP_STYLE;

export const MAP_TEST_ITEM_1 = {
  //"id": 5,
  "name": "Test 1",
  "hint": "Это тест 1",
  // "line":   MAP_ITEM.LINE.ANT,

  "fc": {
    //"color": "green",     //rgba(255, 190, 218, 0.5)
    "style": {
      "color":  "green",    // rgba(255, 190, 218, 0.5)
      "marker": {
        "icon": "gold",     // "mdi-flag mdi-spin", "fs-spec0", "pulse" (size: 12), "#0f0", "gold", "file_name" (size_w: 25, size_h: 41)
        //"zoom": 1,
      },
      "line": {
        "type": "ant",
      },
    //"line":   MAP_ITEM.LINE.ANT,
    },


    "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "properties": {
          "hint": "Подсказка 1",
        },
        "geometry": {
          "type": "Polygon",
          "coordinates": [
            [
              [23.503812450763203,53.969066992023016],
              [23.767941692759162,53.305836099082995],
              [24.917680746153298,53.435614938642495],
              [23.503812450763203,53.969066992023016],
            ]
          ]
        },
      },
      {
        "type": "Feature",
        "properties": {
          "hint": "Подсказка 2",
          "date": "2021-01-05 09:00",
        },
        "geometry": {
          "type": "Polygon",
          "coordinates": [
            [
              [24.917680746153298,54.83722712988182],
              [24.49951171875,54.31011433916155],
              [23.840332031250004,54.87660665410869],
              [24.917680746153298,54.83722712988182],
            ]
          ]
        },
      },
      {
        "type": "Feature",
        "properties": {
          "hint": "Подсказка 3-1",
          "date": "2021-01-04",
        },
        "geometry": {
          "type": "LineString",
          "coordinates": [
            [32.02514648437501,54.7943516039205],
            [27.608642578125004,53.904338156274704],
            [23.70849609375,52.0862573323384],
          ]
        },
      },
      {
        "type": "Feature",
        "properties": {
          "hint": "Подсказка 3-2",
          "date": "2021-01-04",
        },
        "geometry": {
          "type": "LineString",
          "coordinates": [
            [22.939453125,54.09806018306312],
            [23.829345703125004,53.69020141273198],
            [27.605584208817955,53.88673288280922],
          ]
        },
      },
      {
        "type": "Feature",
        "properties": {
          "hint": "Подсказка 4",
          "date": "2021-01-03",
        },
        "geometry": {
          "type": "Point",
          "coordinates": [23.928222656250004,53.028000167735165]
        },
      },
      {
        "type": "Feature",
        "properties": {
          "hint": "Подсказка 5",
          "date": "2021-01-02",
        },
        "geometry": {
          "type": "Point",
          "coordinates": [23.532714843750004,53.94315470224928]
        },
      },
      {
        "type": "Feature",
        "properties": {
          "hint": "Test",
          "date": "2021-01-01",
        },
        "geometry": {
          "type": "Point",
          "coordinates": [25.7080078125,54.16243396806781]
        },
      },
      // {
      //   "type": "Feature",
      //   "properties": {},
      //   "geometry": {
      //     "type": "Point",
      //     "coordinates": [-0.52509765625,48.104642388766935]
      //   }
      // },
    ],
  }
};


export const MAP_TEST_ITEM_2 = {
  //"id": 6,
  "name": "Test 2",
  "hint": "Это тест 2",
  "color": "#923",
  // "marker": MAP_ITEM.MARKER.PULSE,
  "fc": {
    //"color": "#923",
    "marker": MAP_ITEM.MARKER.PULSE,
    "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "properties": {
          "hint": "Привет",
        },
        "geometry": {
          "type": "Polygon",
          "coordinates": [
            [
              [31.014404296875004,52.429222277955134],
              [29.267578125000004,52.03897658307622],
              [30.563964843750004,51.26191485308451],
              [31.014404296875004,52.429222277955134],
            ]
          ]
        }
      },
      {
        "type": "Feature",
        "properties": {
          "hint": "Подсказка 555",
          "date": "2020-12-31 05:00",
        },
        "geometry": {
          "type": "LineString",
          "coordinates": [
            [27.535667644760217,53.882154002633904],
            [30.984884804942663,52.41945363472706],
            [30.51100587077343,50.414116379832485],
          ]
        },
      },
      {
        "type": "Feature",
        "properties": {},
        "geometry": {
          "type": "Point",
          "coordinates": [30.541992187500004,50.41551870402678]
        }
      },
      {
        "type": "Feature",
        "properties": {},
        "geometry": {
          "type": "Point",
          "coordinates": [31.24901404693862,51.4907087536248]
        }
      },
      {
        "type": "Feature",
        "properties": {},
        "geometry": {
          "type": "Point",
          "coordinates": [29.637048820051557,51.06794583616016]
        }
      },
      {
        "type": "Feature",
        "properties": {
          "hint": "Подсказка 5",
          "date": "2021-01-06 19:00",
        },
        "geometry": {
          "type": "Point",
          "coordinates": [30.21580260030736,51.284672727278426]
        },
      },

    ],
  }
};



export const MAP_TEST_ITEM_3 = {
  "name": "Test 3",
  "hint": "Это тест 3",
  "color": "#443",
  "polygon": MAP_ITEM.POLYGON.GREEN_MIN,
  "fc": {
  //  "color": "#443",
    "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "properties": {
          "hint": "Color 1 = 10",
          "value": 10,
        },
        "geometry": {
          "type": "Polygon",
          "coordinates": [
            [
              [30.212402343750004,55.19141243527065],
              [30.443115234375004,54.50832650029076],
              [31.014404296875004,54.718275018302315],
              [30.212402343750004,55.19141243527065],
            ]
          ]
        }
      },
      {
        "type": "Feature",
        "properties": {
          "hint": "Color 2 = 20",
          "value": 20,
          "date": "2021-01-08 11:00",
        },
        "geometry": {
          "type": "Polygon",
          "coordinates": [
            [
              [31.453857421875004,55.19141243527065],
              [31.783447265625004,54.38695529486881],
              [31.190185546875004,55.247815044675555],
              [31.453857421875004,55.19141243527065],
            ]
          ]
        },
      },
      {
        "type": "Feature",
        "properties": {
          "hint": "Color 3 = 30",
          "value": 30,
          "date": "2021-01-04 12:00",
        },
        "geometry": {
          "type": "Polygon",
          "coordinates": [
            [
              [30.531005859375004,56.33481154165235],
              [29.553222656250004,55.72092280778698],
              [31.453857421875004,55.73948169869349],
              [31.508789062500004,56.065902963300424],
              [30.531005859375004,56.33481154165235],
            ]
          ]
        },
      },
      {
        "type": "Feature",
        "properties": {
          "hint": "Количество задержаний = 100",
          "value": 100,
        },
        "geometry": {
          "type": "Polygon",
          "coordinates": [
            [
              [30.926513671875,54.17529672404642],
              [30.805664062500004,52.98833725339543],
              [32.62939453125001,54.438102809740165],
              [30.926513671875,54.17529672404642],
            ]
          ]
        },
      },
    ],
  }
};


export const MAP_TEST_EDIT_1 = {
  mode_marker:  true,
  //mode_line:    true,
  mode_polygon: true,
  data: {
    "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "properties": {
          "hint": "Edit 1",
        },
        "geometry": {
          "type": "Polygon",
          "coordinates": [
            [
              [30.212402343750004,55.19141243527065],
              [30.443115234375004,54.50832650029076],
              [31.014404296875004,54.718275018302315],
              [30.212402343750004,55.19141243527065],
            ]
          ]
        }
      },
      {
        "type": "Feature",
        "properties": {
          "hint": "Edit 2",
        },
        "geometry": {
          "type": "Point",
          "coordinates": [24.071044921875004,55.86914706303444]
        },
      },
    ],
  },
};


export const MAP_TEST_EDIT_2 = {
  data: {
    "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "properties": {
          "hint": "Edit 1",
        },
        "geometry": {
          "type": "Polygon",
          "coordinates": [
            [
              [26.378173828125004,56.41390137600676],
              [26.520996093750004,55.86914706303444],
              [27.652587890625004,56.49889156789072],
              [26.378173828125004,56.41390137600676],
            ]
          ]
        }
      },
      {
        "type": "Feature",
        "properties": {
          "hint": "Edit 2",
        },
        "geometry": {
          "type": "Point",
          "coordinates": [30.541992187500004,56.353077613860826]
        },
      },
      {
        "type": "Feature",
        "properties": {
          "hint": "Подсказка 555",
          "date": "2020-12-31 05:00",
        },
        "geometry": {
          "type": "LineString",
          "coordinates": [
            [26.16943359375,56.69847410813164],
            [29.168701171875004,57.24339368551158],
            [31.201171875000004,57.01083265740579],
          ]
        },
      },
    ],
  },
};
