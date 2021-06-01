webpackHotUpdate("app",{

/***/ "./src/store/modules/map/index_menu.js":
/*!*********************************************!*\
  !*** ./src/store/modules/map/index_menu.js ***!
  \*********************************************/
/*! exports provided: MAP_DATA_MENU_TILES */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"MAP_DATA_MENU_TILES\", function() { return MAP_DATA_MENU_TILES; });\n/* harmony import */ var proj4leaflet__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! proj4leaflet */ \"./node_modules/proj4leaflet/src/proj4leaflet.js\");\n/* harmony import */ var proj4leaflet__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(proj4leaflet__WEBPACK_IMPORTED_MODULE_0__);\n\nvar MAP_DATA_MENU_TILES = [{\n  title: 'OSM',\n  subtitle: 'Схема (Интернет)',\n  icon: 'mdi-map-outline',\n  url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',\n  attr: '',\n  tms: false //crs:      CRS.EPSG3857,\n\n}, {\n  title: 'OSM',\n  subtitle: 'Схема (Локальная сеть)',\n  icon: 'mdi-map-outline',\n  url: 'http://200.200.200.231/osm/{z}/{x}/{y}.png',\n  attr: '',\n  tms: false\n}, // {\n//   title:    'OSM',\n//   subtitle: 'Схема (Локальная сеть)',\n//   url:      'http://192.168.56.1:8080/osm/{z}/{x}/{y}.png',\n//   icon:     'mdi-map-outline',\n//   attr:     '',\n//   tms:      false,\n//   enabled:  false,\n// },\n{\n  title: 'Yandex',\n  subtitle: 'Интернет',\n  url: 'https://core-sat.maps.yandex.net/tiles?l=sat&v=3.786.0&x={x}&y={y}&z={z}&scale=2&lang=ru_UA',\n  icon: 'mdi-map-outline',\n  attr: '',\n  tms: false,\n  crs: L.CRS.EPSG3395,\n  enabled: false\n}, {\n  title: 'ESRI',\n  subtitle: 'Спутник (Интернет)',\n  icon: 'mdi-map-outline',\n  url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',\n  attr: '',\n  tms: false\n}, {\n  title: 'ОТМ',\n  subtitle: 'Схема (Интернет)',\n  url: 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',\n  icon: 'mdi-map-outline',\n  attr: '',\n  tms: false\n}, {\n  title: 'Stamen',\n  subtitle: 'Черно-белая (Интернет)',\n  icon: 'mdi-map-outline',\n  url: 'http://{s}.tile.stamen.com/toner/{z}/{x}/{y}.png',\n  attr: '',\n  tms: false\n}, {\n  title: 'Yandex',\n  subtitle: 'Спутник (Локальная сеть)',\n  url: 'http://200.200.200.232/{z}/{x}/{-y}.jpg',\n  icon: 'mdi-map-outline',\n  attr: '',\n  tms: true,\n  crs: L.CRS.EPSG3395,\n  enabled: false\n}];//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiLi9zcmMvc3RvcmUvbW9kdWxlcy9tYXAvaW5kZXhfbWVudS5qcy5qcyIsInNvdXJjZXMiOlsid2VicGFjazovLy8uL3NyYy9zdG9yZS9tb2R1bGVzL21hcC9pbmRleF9tZW51LmpzPzUwNTYiXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IHsgQ1JTLCB9IGZyb20gJ3Byb2o0bGVhZmxldCc7XG5cblxuZXhwb3J0IGNvbnN0IE1BUF9EQVRBX01FTlVfVElMRVMgPSBbXG4gIHtcbiAgICB0aXRsZTogICAgJ09TTScsXG4gICAgc3VidGl0bGU6ICfQodGF0LXQvNCwICjQmNC90YLQtdGA0L3QtdGCKScsXG4gICAgaWNvbjogICAgICdtZGktbWFwLW91dGxpbmUnLFxuICAgIHVybDogICAgICAnaHR0cHM6Ly97c30udGlsZS5vcGVuc3RyZWV0bWFwLm9yZy97en0ve3h9L3t5fS5wbmcnLFxuICAgIGF0dHI6ICAgICAnJyxcbiAgICB0bXM6ICAgICAgZmFsc2UsXG4gICAgLy9jcnM6ICAgICAgQ1JTLkVQU0czODU3LFxuICB9LFxuICB7XG4gICAgdGl0bGU6ICAgICdPU00nLFxuICAgIHN1YnRpdGxlOiAn0KHRhdC10LzQsCAo0JvQvtC60LDQu9GM0L3QsNGPINGB0LXRgtGMKScsXG4gICAgaWNvbjogICAgICdtZGktbWFwLW91dGxpbmUnLFxuICAgIHVybDogICAgICAnaHR0cDovLzIwMC4yMDAuMjAwLjIzMS9vc20ve3p9L3t4fS97eX0ucG5nJyxcbiAgICBhdHRyOiAgICAgJycsXG4gICAgdG1zOiAgICAgIGZhbHNlLFxuICB9LFxuXG4gIC8vIHtcbiAgLy8gICB0aXRsZTogICAgJ09TTScsXG4gIC8vICAgc3VidGl0bGU6ICfQodGF0LXQvNCwICjQm9C+0LrQsNC70YzQvdCw0Y8g0YHQtdGC0YwpJyxcbiAgLy8gICB1cmw6ICAgICAgJ2h0dHA6Ly8xOTIuMTY4LjU2LjE6ODA4MC9vc20ve3p9L3t4fS97eX0ucG5nJyxcbiAgLy8gICBpY29uOiAgICAgJ21kaS1tYXAtb3V0bGluZScsXG4gIC8vICAgYXR0cjogICAgICcnLFxuICAvLyAgIHRtczogICAgICBmYWxzZSxcbiAgLy8gICBlbmFibGVkOiAgZmFsc2UsXG4gIC8vIH0sXG5cbiAge1xuICAgIHRpdGxlOiAgICAnWWFuZGV4JyxcbiAgICBzdWJ0aXRsZTogJ9CY0L3RgtC10YDQvdC10YInLFxuICAgIHVybDogICAgICAnaHR0cHM6Ly9jb3JlLXNhdC5tYXBzLnlhbmRleC5uZXQvdGlsZXM/bD1zYXQmdj0zLjc4Ni4wJng9e3h9Jnk9e3l9Jno9e3p9JnNjYWxlPTImbGFuZz1ydV9VQScsXG4gICAgaWNvbjogICAgICdtZGktbWFwLW91dGxpbmUnLFxuICAgIGF0dHI6ICAgICAnJyxcbiAgICB0bXM6ICAgICAgZmFsc2UsXG4gICAgY3JzOiAgICAgIEwuQ1JTLkVQU0czMzk1LFxuICAgIGVuYWJsZWQ6ICBmYWxzZSxcbiAgfSxcblxuICB7XG4gICAgdGl0bGU6ICAgICdFU1JJJyxcbiAgICBzdWJ0aXRsZTogJ9Ch0L/Rg9GC0L3QuNC6ICjQmNC90YLQtdGA0L3QtdGCKScsXG4gICAgaWNvbjogICAgICdtZGktbWFwLW91dGxpbmUnLFxuICAgIHVybDogICAgICAnaHR0cHM6Ly9zZXJ2ZXIuYXJjZ2lzb25saW5lLmNvbS9BcmNHSVMvcmVzdC9zZXJ2aWNlcy9Xb3JsZF9JbWFnZXJ5L01hcFNlcnZlci90aWxlL3t6fS97eX0ve3h9JyxcbiAgICBhdHRyOiAgICAgJycsXG4gICAgdG1zOiAgICAgIGZhbHNlLFxuICB9LFxuICB7XG4gICAgdGl0bGU6ICAgICfQntCi0JwnLFxuICAgIHN1YnRpdGxlOiAn0KHRhdC10LzQsCAo0JjQvdGC0LXRgNC90LXRgiknLFxuICAgIHVybDogICAgICAnaHR0cHM6Ly97c30udGlsZS5vcGVudG9wb21hcC5vcmcve3p9L3t4fS97eX0ucG5nJyxcbiAgICBpY29uOiAgICAgJ21kaS1tYXAtb3V0bGluZScsXG4gICAgYXR0cjogICAgICcnLFxuICAgIHRtczogICAgICBmYWxzZSxcbiAgfSxcbiAge1xuICAgIHRpdGxlOiAgICAnU3RhbWVuJyxcbiAgICBzdWJ0aXRsZTogJ9Cn0LXRgNC90L4t0LHQtdC70LDRjyAo0JjQvdGC0LXRgNC90LXRgiknLFxuICAgIGljb246ICAgICAnbWRpLW1hcC1vdXRsaW5lJyxcbiAgICB1cmw6ICAgICAgJ2h0dHA6Ly97c30udGlsZS5zdGFtZW4uY29tL3RvbmVyL3t6fS97eH0ve3l9LnBuZycsXG4gICAgYXR0cjogICAgICcnLFxuICAgIHRtczogICAgICBmYWxzZSxcbiAgfSxcbiAge1xuICAgIHRpdGxlOiAgICAnWWFuZGV4JyxcbiAgICBzdWJ0aXRsZTogJ9Ch0L/Rg9GC0L3QuNC6ICjQm9C+0LrQsNC70YzQvdCw0Y8g0YHQtdGC0YwpJyxcbiAgICB1cmw6ICAgICAgJ2h0dHA6Ly8yMDAuMjAwLjIwMC4yMzIve3p9L3t4fS97LXl9LmpwZycsXG4gICAgaWNvbjogICAgICdtZGktbWFwLW91dGxpbmUnLFxuICAgIGF0dHI6ICAgICAnJyxcbiAgICB0bXM6ICAgICAgdHJ1ZSxcbiAgICBjcnM6ICAgICAgTC5DUlMuRVBTRzMzOTUsXG4gICAgZW5hYmxlZDogIGZhbHNlLFxuICB9LFxuXTtcbiJdLCJtYXBwaW5ncyI6IkFBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUdBO0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFQQTtBQVVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQU5BO0FBVUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQVJBO0FBWUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBTkE7QUFTQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFOQTtBQVNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQU5BO0FBU0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQVJBIiwic291cmNlUm9vdCI6IiJ9\n//# sourceURL=webpack-internal:///./src/store/modules/map/index_menu.js\n");

/***/ })

})