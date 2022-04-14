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

в components/LeafletEditor.vue:
    добавить
      <DialogMenuPos
        ref="key_dialog"
        @ok="menu_pos_save_ok"
      />

в store/addition.js:
    удалить import store from "@/store"
    изменить genVarNameForLocalstorage return JSON.stringify({identifier: "local_user", key: this._key})

в store/index.js:
    const store = new Vuex.Store({ modules: {map}, ...
    export default store

в store/modules/map/index.js:
    удалить import axios from "@/plugins/axiosSettings"
    удалить MAP_ACT_INI
    задать state.tiles

в store/modules/siteControl/notifications.js:
    удалить import axios from "@/plugins/axiosSettings"
    удалить setNotificationInterval
    удалить stopNotificationInterval
    удалить getNotifications
    удалить axis в setReadNotification

