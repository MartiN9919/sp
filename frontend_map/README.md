# frontend_map

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

npm install @mdi/font -D


удалить vue-resize-split-pane": "^0.1.5
удалить SelectorInput в EditorNavObj в главном проекте

в store/addition.js:
    удалить import store from "@/store"
    изменить genVarNameForLocalstorage return "local_user"

в store/index.js:
    const store = new Vuex.Store({ modules: {map}, ...
    export default store

в store/modules/map/index.js:
    удалить import axios from "@/plugins/axiosSettings"
    удалить MAP_ACT_INI
    задать state.tiles