import UserSetting from "@/store/addition"

class SearchSettings {
  constructor() {
    this.searchDeep = {
      title: 'Глубина поиска',
      subTitle: 'Глубина, на которую будет осуществляться поиск',
      state: new UserSetting('searchDeep', ''),
      props: {mask: '#'}
    }
    this.searchCount = {
      title: 'Максимальное количество объектов',
      subTitle: 'Максимальное количество объектов, которые вернет поиск',
      state: new UserSetting('searchCount', ''),
      props: {mask: '###'}
    }
    this.searchShort = {
      title: 'Короткие пути',
      subTitle: 'Выводить только кротчайшие пути между объектами',
      state: new UserSetting('searchShort', false)
    }
  }
}

class GlobalSettings {
  constructor() {
    this.linkHighlighting = {
      title: 'Подсветка связей',
      subTitle: 'Подсвечивать объекты и связи при наведении',
      state: new UserSetting('linkHighlighting', true)
    }
    this.showGlobalTitle = {
      title: 'Подписи объектов',
      subTitle: 'Подпись под объектами на графе',
      state: new UserSetting('showGlobalTitle', true)
    }
    this.showGlobalTooltipObject = {
      title: 'Заголовки объектов',
      subTitle: 'Отображение заголовка над объектами',
      state: new UserSetting('showGlobalTooltipObject', true)
    }
    this.showGlobalTriggers = {
      title: 'Уведомления о триггерах',
      subTitle: 'Управление отображением значка уведомления о срабатывании триггеров',
      state: new UserSetting('showGlobalTriggers', true)
    }
    this.showGlobalDateObject = {
      title: 'Время записи объекта',
      subTitle: 'Управление отображением даты классификатора',
      state: new UserSetting('showGlobalDateObject', true)
    }
    this.showGlobalTooltipRelation = {
      title: 'Заголовки связей',
      subTitle: 'Отображение заголовка над связями',
      state: new UserSetting('showGlobalTooltipRelation', true)
    }
    this.showGlobalDateRelation = {
      title: 'Время записи связи',
      subTitle: 'Управление отображением даты связи',
      state: new UserSetting('showGlobalDateRelation', true)
    }
    this.showGlobalDocRelation = {
      title: 'Документ установивший связь',
      subTitle: 'Управление отображением названия документа на основании которого была создана связь',
      state: new UserSetting('showGlobalDocRelation', true)
    }
  }
}

export default {
  state: {
    classifiersSettings: new UserSetting('classifiersSettings', []),
    globalDisplaySettings: new GlobalSettings(),
    searchSettings: new SearchSettings()
  },
  getters: {
    classifiersSettings: state => state.classifiersSettings.value,
    globalDisplaySettings: state => state.globalDisplaySettings,
    globalDisplaySettingValue: state => identifier => state.globalDisplaySettings[identifier].state.value,
    searchSettings: state => state.searchSettings,
    searchSettingsValue: state => identifier => state.searchSettings[identifier].state.value
  },
  mutations: {
    changeGlobalSettingState: (state, {id, value}) => state.globalDisplaySettings[id].state.value = value,
    changeSearchSettingsState: (state, {id, value}) => state.searchSettings[id].state.value = value,
    setClassifiersSettings: (state, classifierId) => state.classifiersSettings.switch(classifierId)
  },
  actions: {
    changeGlobalSettingState({ commit }, payload) { commit('changeGlobalSettingState', payload) },
    changeSearchSettingsState({ commit }, payload) { commit('changeSearchSettingsState', payload) },
    setClassifiersSettings({ getters, commit }, id) { commit('setClassifiersSettings', id) }
  }
}