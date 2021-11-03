import { STYLE_DATA_POST_TEST       } from '@/components/Map/Leaflet/Components/Style/StyleDataPost';
import { STYLE_DATA_CHECKPOINT_TEST } from '@/components/Map/Leaflet/Components/Style/StyleDataCheckpoint';
import { STYLE_DATA_ENGENEER_TEST   } from '@/components/Map/Leaflet/Components/Style/StyleDataEngeneer';
//import { STYLE_DATA_TEXT_TEST       } from '@/components/Map/Leaflet/Components/Style/StyleDataText';


export const MAP_TEST_ITEM_1 = {
  //"id": 5,
  "name":  "Test 1",
  "hint":  "Это тест 1",
  "color": "#F00",

  "fc": {
    // "style": {
    //   "marker": {
    //     "icon": "test",     // "mdi-flag mdi-spin", "fs-spec0", "pulse" (size: 12), "#0f0", "gold", "file_name" (size_w: 25, size_h: 41)
    //     "zoom": 2,
    //   },
    //   "line": {
    //     "class": "test_mark_auto arrow-double-end",
    //   },


    "type": "FeatureCollection",
    "features": [
      ...STYLE_DATA_POST_TEST,
      ...STYLE_DATA_CHECKPOINT_TEST,
      ...STYLE_DATA_ENGENEER_TEST,
      {
        "type": "Feature",
        "properties": {
          "class": "line-engeneer_zagr_ograd line-text_lr_100 hatch-diagonal-1",  // test_mark_auto
          "hint": "line-engeneer_zagr_ograd line-text_lr_100 hatch-diagonal-1",
          "text": "STOP",
        },
        "geometry": {
          "type": "Polygon",
          "coordinates": [
            [
              [25.0,55.5],
              [27.5,56.25],
              [31.0,55.5],
              [25.0,55.5],
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
              [30.0,54.5],
              [32.0,53.5],
              [30.0,52.5],
              [30.0,54.5],
            ]
          ]
        },
      },
      {
        "type": "Feature",
        "properties": {
          "class": "arrow-double-end line-engeneer_zagr_signal line-text_rl_fill_100 ant",
          "hint": "arrow-double-end line-engeneer_zagr_signal line-text_rl_fill_100 ant",
          "date": "2021-01-04",
          "text": "C-120",
        },
        "geometry": {
          "type": "LineString",
          "coordinates": [
            [32.0,56.5],
            [27.5,57.5],
            [24.0,56.5],
          ]
        },
      },
      {
        "type": "Feature",
        "properties": {
          "class": "arrow-double-end line-engeneer_zagr_signal line-text_lr_300 ant",
          "hint": "arrow-double-end line-engeneer_zagr_signal line-text_lr_300 ant",
          "date": "2021-01-04",
          "text": "C-120",
        },
        "geometry": {
          "type": "LineString",
          "coordinates": [
            [24.0,56.0],
            [27.5,57.0],
            [32.0,56.0],
          ]
        },
      },
      {
        "type": "Feature",
        "properties": {
          "class": "line_border_1 hidden",
          "hint": "line_border_1 hidden",
          "date": "2021-01-04",
        },
        "geometry": {
          "type": "LineString",
          "coordinates": [
            [24.0,55.5],
            [27.5,56.5],
            [32.0,55.5],
          ]
        },
      },
      {
        "type": "Feature",
        "properties": {
          "class": "line-engeneer_zagr_invisible hidden",
          "hint": "line-engeneer_zagr_invisible hidden",
          "date": "2021-05-04",
        },
        "geometry": {
          "type": "LineString",
          "coordinates": [
            [24.0,57.0],
            [27.5,58.0],
            [32.0,57.0],
          ]
        },
      },
      {
        "type": "Feature",
        "properties": {
          "class": "line-engeneer_zagr_ograd",
          "hint": "line-engeneer_zagr_ograd",
          "date": "2021-05-04",
          "color": "#888",
        },
        "geometry": {
          "type": "LineString",
          "coordinates": [
            [24.0,57.5],
            [27.5,58.5],
            [32.0,57.5],
          ]
        },
      },






      {
        "type": "Feature",
        "properties": {
          "class": "icon-svg-standart",
          "hint": "icon-svg-standart",
          "date": "2021-01-02",
          "zoom": false,
        },
        "geometry": {
          "type": "Point",
          "coordinates": [24.0,54.5]
        },
      },
      {
        "type": "Feature",
        "properties": {
          "class": "icon-svg-standart",
          "hint": "icon-svg-standart",
          "date": "2021-01-02",
        },
        "geometry": {
          "type": "Point",
          "coordinates": [24.5,54.5]
        },
      },
      {
        "type": "Feature",
        "properties": {
          "class": "icon-svg-point_detention_inside",
          "text": '"detention"',
          "hint": "icon-svg-point_detention_inside\ntest\nasdf asd fa sdf a sd fa sd f asd f as df a sd fa sd f asd f asd fa sd fa sdf asd",
          "date": "2021-04-01",
          "zoom": false,
        },
        "geometry": {
          "type": "Point",
          "coordinates": [25.0,54.5]
        },
      },


      {
        "type": "Feature",
        "properties": {
          "class": "icon-mdi-flag sss icon-mdi-spin tst",
          "hint": "Demo",
          "date": "2021-01-03",
          //"zoom": false,
        },
        "geometry": {
          "type": "Point",
          "coordinates": [45,53.0]
        },
      },
    ],
  }
};


export const MAP_TEST_ITEM_2 = {
  //"id": 6,
  "name":  "Test 2",
  "hint":  "Это тест 2",
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
          "coordinates": [24.5,53.25]
        },
      },

      // {
      //   "type": "Feature",
      //   "properties": {
      //     "class": "icon-pulse-14",
      //   },
      //   "geometry": {
      //     "type": "Point",
      //     "coordinates": [30.541992187500004,50.41551870402678]
      //   }
      // },
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
  "hint": "Это тест 3",
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
