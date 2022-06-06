import _ from 'lodash'

const ObjectCtxMenu = [
  {
    icon: 'mdi-pencil',
    title: 'Изменить',
    subtitle: 'Редактировать данный объект',
    action: 'setChangeObject',
    disabled: false
  },
  {
    icon: 'mdi-delete',
    title: 'Удалить',
    subtitle: 'Удалить объект с графа',
    action: 'deleteObject',
    disabled: false
  },
  {
    icon: 'mdi-link-variant',
    title: 'Найти связи',
    subtitle: 'Поиск связей для данного объекта',
    action: 'setSearchRelation',
    disabled: false
  },
  {
    icon: 'mdi-map-plus',
    title: 'Вывести геометрию/точку на карту',
    subtitle: 'Вывести выбранную геометрию/точку на карту',
    action: 'addGeometryToGraph',
    disabled: true
  },
  {
    icon: 'mdi-cog-outline',
    title: 'Настройки',
    subtitle: 'Индивидуальные настройки объекта',
    menu: [
      {
        title: 'Подпись',
        model: 'objectTitle',
      },
      {
        title: 'Заголовок',
        model: 'objectTooltip'
      },
      {
        title: 'Дата внесения записи',
        model: 'objectCreateDate'
      },
      {
        title: 'Триггеры',
        model: 'objectTriggers'
      }
    ],
  }
]

const RelationCtxMenu = [
  {
    icon: 'mdi-link-variant-plus',
    title: 'Редактировать связь',
    subtitle: 'Добавить/Изменить данную связь',
    action: 'createRelation',
    disabled: false
  },
  {
    icon: 'mdi-cog-outline',
    title: 'Настройки',
    subtitle: 'Индивидуальные настройки связи',
    menu: [
      {
        title: 'Заголовок',
        model: 'relationTooltip'
      },
      {
        title: 'Дата создания связей',
        model: 'relationCreateDate'
      },
      {
        title: 'Документ породивший связь',
        model: 'relationDoc'
      }
    ],
  }
]

const SpaceCtxMenu = [
  {
    icon: 'mdi-link-variant',
    title: 'Связь',
    subtitle: 'Работа со связями объекта',
    menu: [
      {
        icon: 'mdi-link-variant-plus',
        title: 'Создать связь',
        subtitle: 'Связать выбранные объекты',
        action: 'createRelation',
        disabled: true
      },
      {
        icon: 'mdi-account-search-outline',
        title: 'Найти связи',
        subtitle: 'Найти минимальные связи между выбранными объектами',
        action: 'findRelations',
        disabled: true
      },
    ],
  },
  {
    icon: 'mdi-graphql',
    title: 'Переупорядочивание',
    subtitle: 'Расстановка объектов на графе',
    menu: [
      {
        icon: 'mdi-graph-outline',
        title: 'Переупорядочить граф',
        subtitle: 'Переупорядочить граф',
        action: 'reorderNodes',
        disabled: true
      },
      {
        icon: 'mdi-graph',
        title: 'Переупорядочить выбранные объекты',
        subtitle: 'Переупорядочить выбранные на графе объекты',
        action: 'reorderChoosingNodes',
        disabled: true
      }
    ],
  },
  {
    icon: 'mdi-archive-outline',
    title: 'Сохранить / Загрузить',
    subtitle: 'Операции над объектами',
    menu: [
      {
        icon: 'mdi-download',
        title: 'Загрузить граф',
        subtitle: 'Загрузить граф из файла',
        action: 'getGraphFromFile',
        disabled: true
      },
      {
        icon: 'mdi-upload',
        title: 'Сохранить граф',
        subtitle: 'Сохранить граф в файл',
        action: 'saveGraphInFile',
        disabled: true
      }
    ],
  },
    {
    icon: 'mdi-delete-variant',
    title: 'Удалить',
    subtitle: 'Удаление объектов с графа',
    menu: [
      {
        icon: 'mdi-delete-outline',
        title: 'Очистить граф',
        subtitle: 'Удалить все объекты с графа',
        action: 'clearGraph',
        disabled: true
      },
      {
        icon: 'mdi-delete',
        title: 'Удалить выбранные объекты',
        subtitle: 'Удалить с графа все выбранные объекты',
        action: 'deleteObjects',
        disabled: true
      }
    ],
  },

]

function getObjectCtxMenu(geometryToGraph) {
  let objectCtxMenu = _.cloneDeep(ObjectCtxMenu)
  objectCtxMenu[3].disabled = !geometryToGraph
  return objectCtxMenu
}

function getSpaceCtxMenu(save, reorder, createRelation, findRelation, choosingObjects) {
  let spaceCtxMenu = _.cloneDeep(SpaceCtxMenu)
  spaceCtxMenu[0].menu[0].disabled = !createRelation
  spaceCtxMenu[0].menu[1].disabled = !findRelation
  spaceCtxMenu[1].menu[0].disabled = !reorder
  spaceCtxMenu[1].menu[1].disabled = !choosingObjects
  spaceCtxMenu[2].menu[0].disabled = false
  spaceCtxMenu[2].menu[1].disabled = !save
  spaceCtxMenu[3].menu[0].disabled = !save
  spaceCtxMenu[3].menu[1].disabled = !choosingObjects
  return spaceCtxMenu
}

export default {getObjectCtxMenu, RelationCtxMenu, getSpaceCtxMenu}