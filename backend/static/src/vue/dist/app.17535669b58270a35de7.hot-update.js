webpackHotUpdate("app",{

/***/ "./src/store/modules/map/index_menu.js":
/*!*********************************************!*\
  !*** ./src/store/modules/map/index_menu.js ***!
  \*********************************************/
/*! exports provided: MAP_DATA_MENU_TILES */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"MAP_DATA_MENU_TILES\", function() { return MAP_DATA_MENU_TILES; });\n/* harmony import */ var leaflet__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! leaflet */ \"./node_modules/leaflet/dist/leaflet-src.js\");\n/* harmony import */ var leaflet__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(leaflet__WEBPACK_IMPORTED_MODULE_0__);\n\nvar MAP_DATA_MENU_TILES = [{\n  title: 'OSM',\n  subtitle: 'Схема (Интернет)',\n  icon: 'mdi-map-outline',\n  url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',\n  attr: '',\n  tms: false,\n  crs: leaflet__WEBPACK_IMPORTED_MODULE_0__[\"L\"].CRS.EPSG3857\n}, {\n  title: 'OSM',\n  subtitle: 'Схема (Локальная сеть)',\n  icon: 'mdi-map-outline',\n  url: 'http://200.200.200.231/osm/{z}/{x}/{y}.png',\n  attr: '',\n  tms: false\n}, // {\n//   title:    'OSM',\n//   subtitle: 'Схема (Локальная сеть)',\n//   url:      'http://192.168.56.1:8080/osm/{z}/{x}/{y}.png',\n//   icon:     'mdi-map-outline',\n//   attr:     '',\n//   tms:      false,\n//   enabled:  false,\n// },\n{\n  title: 'Yandex',\n  subtitle: 'Интернет',\n  url: 'https://core-sat.maps.yandex.net/tiles?l=sat&v=3.786.0&x={x}&y={y}&z={z}&scale=2&lang=ru_UA',\n  icon: 'mdi-map-outline',\n  attr: '',\n  tms: false,\n  crs: leaflet__WEBPACK_IMPORTED_MODULE_0__[\"L\"].CRS.EPSG3395,\n  enabled: false\n}, {\n  title: 'ESRI',\n  subtitle: 'Спутник (Интернет)',\n  icon: 'mdi-map-outline',\n  url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',\n  attr: '',\n  tms: false\n}, {\n  title: 'ОТМ',\n  subtitle: 'Схема (Интернет)',\n  url: 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',\n  icon: 'mdi-map-outline',\n  attr: '',\n  tms: false\n}, {\n  title: 'Stamen',\n  subtitle: 'Черно-белая (Интернет)',\n  icon: 'mdi-map-outline',\n  url: 'http://{s}.tile.stamen.com/toner/{z}/{x}/{y}.png',\n  attr: '',\n  tms: false\n}, {\n  title: 'Yandex',\n  subtitle: 'Спутник (Локальная сеть)',\n  url: 'http://200.200.200.232/{z}/{x}/{-y}.jpg',\n  icon: 'mdi-map-outline',\n  attr: '',\n  tms: false,\n  enabled: false\n}];//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiLi9zcmMvc3RvcmUvbW9kdWxlcy9tYXAvaW5kZXhfbWVudS5qcy5qcyIsInNvdXJjZXMiOlsid2VicGFjazovLy8uL3NyYy9zdG9yZS9tb2R1bGVzL21hcC9pbmRleF9tZW51LmpzPzUwNTYiXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IHsgTCwgfSBmcm9tIFwibGVhZmxldFwiO1xuXG5leHBvcnQgY29uc3QgTUFQX0RBVEFfTUVOVV9USUxFUyA9IFtcbiAge1xuICAgIHRpdGxlOiAgICAnT1NNJyxcbiAgICBzdWJ0aXRsZTogJ9Ch0YXQtdC80LAgKNCY0L3RgtC10YDQvdC10YIpJyxcbiAgICBpY29uOiAgICAgJ21kaS1tYXAtb3V0bGluZScsXG4gICAgdXJsOiAgICAgICdodHRwczovL3tzfS50aWxlLm9wZW5zdHJlZXRtYXAub3JnL3t6fS97eH0ve3l9LnBuZycsXG4gICAgYXR0cjogICAgICcnLFxuICAgIHRtczogICAgICBmYWxzZSxcbiAgICBjcnM6ICAgICAgTC5DUlMuRVBTRzM4NTcsXG4gIH0sXG4gIHtcbiAgICB0aXRsZTogICAgJ09TTScsXG4gICAgc3VidGl0bGU6ICfQodGF0LXQvNCwICjQm9C+0LrQsNC70YzQvdCw0Y8g0YHQtdGC0YwpJyxcbiAgICBpY29uOiAgICAgJ21kaS1tYXAtb3V0bGluZScsXG4gICAgdXJsOiAgICAgICdodHRwOi8vMjAwLjIwMC4yMDAuMjMxL29zbS97en0ve3h9L3t5fS5wbmcnLFxuICAgIGF0dHI6ICAgICAnJyxcbiAgICB0bXM6ICAgICAgZmFsc2UsXG4gIH0sXG5cbiAgLy8ge1xuICAvLyAgIHRpdGxlOiAgICAnT1NNJyxcbiAgLy8gICBzdWJ0aXRsZTogJ9Ch0YXQtdC80LAgKNCb0L7QutCw0LvRjNC90LDRjyDRgdC10YLRjCknLFxuICAvLyAgIHVybDogICAgICAnaHR0cDovLzE5Mi4xNjguNTYuMTo4MDgwL29zbS97en0ve3h9L3t5fS5wbmcnLFxuICAvLyAgIGljb246ICAgICAnbWRpLW1hcC1vdXRsaW5lJyxcbiAgLy8gICBhdHRyOiAgICAgJycsXG4gIC8vICAgdG1zOiAgICAgIGZhbHNlLFxuICAvLyAgIGVuYWJsZWQ6ICBmYWxzZSxcbiAgLy8gfSxcblxuICB7XG4gICAgdGl0bGU6ICAgICdZYW5kZXgnLFxuICAgIHN1YnRpdGxlOiAn0JjQvdGC0LXRgNC90LXRgicsXG4gICAgdXJsOiAgICAgICdodHRwczovL2NvcmUtc2F0Lm1hcHMueWFuZGV4Lm5ldC90aWxlcz9sPXNhdCZ2PTMuNzg2LjAmeD17eH0meT17eX0mej17en0mc2NhbGU9MiZsYW5nPXJ1X1VBJyxcbiAgICBpY29uOiAgICAgJ21kaS1tYXAtb3V0bGluZScsXG4gICAgYXR0cjogICAgICcnLFxuICAgIHRtczogICAgICBmYWxzZSxcbiAgICBjcnM6ICAgICAgTC5DUlMuRVBTRzMzOTUsXG4gICAgZW5hYmxlZDogIGZhbHNlLFxuICB9LFxuXG4gIHtcbiAgICB0aXRsZTogICAgJ0VTUkknLFxuICAgIHN1YnRpdGxlOiAn0KHQv9GD0YLQvdC40LogKNCY0L3RgtC10YDQvdC10YIpJyxcbiAgICBpY29uOiAgICAgJ21kaS1tYXAtb3V0bGluZScsXG4gICAgdXJsOiAgICAgICdodHRwczovL3NlcnZlci5hcmNnaXNvbmxpbmUuY29tL0FyY0dJUy9yZXN0L3NlcnZpY2VzL1dvcmxkX0ltYWdlcnkvTWFwU2VydmVyL3RpbGUve3p9L3t5fS97eH0nLFxuICAgIGF0dHI6ICAgICAnJyxcbiAgICB0bXM6ICAgICAgZmFsc2UsXG4gIH0sXG4gIHtcbiAgICB0aXRsZTogICAgJ9Ce0KLQnCcsXG4gICAgc3VidGl0bGU6ICfQodGF0LXQvNCwICjQmNC90YLQtdGA0L3QtdGCKScsXG4gICAgdXJsOiAgICAgICdodHRwczovL3tzfS50aWxlLm9wZW50b3BvbWFwLm9yZy97en0ve3h9L3t5fS5wbmcnLFxuICAgIGljb246ICAgICAnbWRpLW1hcC1vdXRsaW5lJyxcbiAgICBhdHRyOiAgICAgJycsXG4gICAgdG1zOiAgICAgIGZhbHNlLFxuICB9LFxuICB7XG4gICAgdGl0bGU6ICAgICdTdGFtZW4nLFxuICAgIHN1YnRpdGxlOiAn0KfQtdGA0L3Qvi3QsdC10LvQsNGPICjQmNC90YLQtdGA0L3QtdGCKScsXG4gICAgaWNvbjogICAgICdtZGktbWFwLW91dGxpbmUnLFxuICAgIHVybDogICAgICAnaHR0cDovL3tzfS50aWxlLnN0YW1lbi5jb20vdG9uZXIve3p9L3t4fS97eX0ucG5nJyxcbiAgICBhdHRyOiAgICAgJycsXG4gICAgdG1zOiAgICAgIGZhbHNlLFxuICB9LFxuICB7XG4gICAgdGl0bGU6ICAgICdZYW5kZXgnLFxuICAgIHN1YnRpdGxlOiAn0KHQv9GD0YLQvdC40LogKNCb0L7QutCw0LvRjNC90LDRjyDRgdC10YLRjCknLFxuICAgIHVybDogICAgICAnaHR0cDovLzIwMC4yMDAuMjAwLjIzMi97en0ve3h9L3steX0uanBnJyxcbiAgICBpY29uOiAgICAgJ21kaS1tYXAtb3V0bGluZScsXG4gICAgYXR0cjogICAgICcnLFxuICAgIHRtczogICAgICBmYWxzZSxcbiAgICBlbmFibGVkOiAgZmFsc2UsXG4gIH0sXG5dO1xuIl0sIm1hcHBpbmdzIjoiQUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBRUE7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQVBBO0FBVUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBTkE7QUFVQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBUkE7QUFZQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFOQTtBQVNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQU5BO0FBU0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBTkE7QUFTQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQVBBIiwic291cmNlUm9vdCI6IiJ9\n//# sourceURL=webpack-internal:///./src/store/modules/map/index_menu.js\n");

/***/ })

})