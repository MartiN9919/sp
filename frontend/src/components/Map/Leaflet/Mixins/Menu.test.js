import { TEST as DATA_FORCE      } from '@/components/Map/Leaflet/Components/Style/StyleDataForce';
import { TEST as DATA_CHECKPOINT } from '@/components/Map/Leaflet/Components/Style/StyleDataCheckpoint';
import { TEST as DATA_ENGENEER   } from '@/components/Map/Leaflet/Components/Style/StyleDataEngeneer';
import { TEST as DATA_LAYOUT     } from '@/components/Map/Leaflet/Components/Style/StyleDataLayout';
import { TEST as DATA_TEXT       } from '@/components/Map/Leaflet/Components/Style/StyleDataText';
import { TEST as DATA_COMMON     } from '@/components/Map/Leaflet/Components/Style/StyleDataCommon';
import { TEST as DATA_TEST       } from '@/components/Map/Leaflet/Components/Style/StyleDataTest';


export const MAP_TEST_ITEM_1 = {
  //"id": 5,
  "name":  "Test 1",
  //"hint":  "Это тест 1",
  "color": "#F00",
  "fc":    {
    "type": "FeatureCollection",
    "features": [
      ...DATA_FORCE,
      ...DATA_CHECKPOINT,
      ...DATA_ENGENEER,
      ...DATA_LAYOUT,
      ...DATA_TEXT,
      ...DATA_COMMON,
      ...DATA_TEST,
    ],
  }
};


export const MAP_TEST_ITEM_2 = {
  //"id": 6,
  "name":  "Test 2",
  //"hint":  "Это тест 2",
  "color": "green",  // "#923"
  "fc": {
    "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "properties": {
          "class": "mark hatch-diagonal-1",
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
          "class": "line_border_2 hidden",
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
        "properties": {
          "hint": "Контроль 5",
          "date": "2021-01-02",
        },
        "geometry": {
          "type": "Point",
          "coordinates": [27.5,54.0],
        },
      },

      {
        "type": "Feature",
        "properties": {
          "class": "icon-pulse-14",
        },
        "geometry": {
          "type": "Point",
          "coordinates": [30.541992187500004,50.41551870402678]
        }
      },
      // {
      //   "type": "Feature",
      //   "properties": {
      //     "class": "icon-fs-spec0",
      //   },
      //   "geometry": {
      //     "type": "Point",
      //     "coordinates": [31.24901404693862,51.4907087536248]
      //   }
      // },
      // {
      //   "type": "Feature",
      //   "properties": {
      //     "class": "icon-file-gold",
      //   },
      //   "geometry": {
      //     "type": "Point",
      //     "coordinates": [29.637048820051557,51.06794583616016]
      //   }
      // },
      // {
      //   "type": "Feature",
      //   "properties": {
      //     "class": "icon-file-test-25-41",
      //     "hint": "Подсказка 5",
      //     "date": "2021-01-06 19:00",
      //   },
      //   "geometry": {
      //     "type": "Point",
      //     "coordinates": [30.21580260030736,51.284672727278426]
      //   },
      // },

      // {
      //   "type": "Feature",
      //   "properties": {
      //     "class": "icon-file-#0f0",
      //     "hint": "Подсказка 6",
      //     "date": "2021-01-09 12:00",
      //   },
      //   "geometry": {
      //     "type": "Point",
      //     "coordinates": [32.21580260030736,50.284672727278426]
      //   },
      // },

    ],
  }
};


export const MAP_TEST_ITEM_3 = {
  "name": "Test 3",
  //"hint": "Это тест 3",
  "color": "#493",
  "fc": {
    "style": {
      "coloring": "green_max",
    },
    "type": "FeatureCollection",
    "features": [
      //должно удалиться
      {
        "type": "Feature",
        "properties": {
          "class": "icon-mdi-flag sss icon-mdi-spin tst",
          "hint": "Подсказка 4",
          "date": "2021-01-03",
        },
        "geometry": {
          "type": "Point",
          "coordinates": [13.928222656250004,53.028000167735165]
        },
      },
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
      //должно удалиться
      {
        "type": "Feature",
        "properties": {
          "class": "icon-mdi-flag sss icon-mdi-spin tst",
          "hint": "Подсказка 4",
          "date": "2021-01-03",
        },
        "geometry": {
          "type": "Point",
          "coordinates": [13.928222656250004,53.028000167735165]
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
