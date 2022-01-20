const ObjectCtxMenuSearchRelation = {
  icon: 'mdi-link-variant',
  title: 'Поиск связей',
  subtitle: 'Поиск связей для данного объекта',
  action: 'setSearchRelation'
}
const ObjectCtxMenuChangeObject = {
  icon: 'mdi-pencil',
  title: 'Изменить',
  subtitle: 'Редактировать данный объект',
  action: 'setChangeObject'
}
const ObjectCtxMenuDelete = {
  icon: 'mdi-delete',
  title: 'Удалить',
  subtitle: 'Удалить объект с графа',
  action: 'deleteObject'
}
const ObjectCtxMenuSettings = {
  icon: 'mdi-cog-outline',
  title: 'Настройки',
  subtitle: 'Индивидуальные настройки объекта',
  menu: [
    {
      title: 'Отображение',
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
      ]
    },
  ],
}

const ObjectCtxMenuGeometryToMap = {
  icon: 'mdi-map-plus',
  title: 'Вывести геометрию/точку на граф',
  subtitle: 'Вывести выбранную геометрию/точку на граф',
  action: 'addGeometryToGraph'
}

const RelationCtxMenu = [
  {
    icon: 'mdi-link-variant-plus',
    title: 'Редактировать связь',
    subtitle: 'Добавить/Изменить данную связь',
    action: 'createRelation'
  },
  {
    icon: 'mdi-cog-outline',
    title: 'Настройки',
    subtitle: 'Индивидуальные настройки связи',
    menu: [
      {
        title: 'Отображение',
        menu: [
          {
            title: 'Заголовок',
            model: 'relationTooltip'
          },
          {
            title: 'Дата создания связей',
            model: 'relationCreateDate'
          },
        ]
      },
    ],
  }
]

const SpaceCtxMenuSpaceBase = {
  icon: 'mdi-download',
  title: 'Загрузить граф',
  subtitle: 'Загрузить граф из файла',
  action: 'getGraphFromFile'
}


const SpaceCtxMenuSave = {
  icon: 'mdi-upload',
  title: 'Сохранить граф',
  subtitle: 'Сохранить граф в файл',
  action: 'saveGraphInFile'
}

const SpaceCtxMenuReorder = {
  icon: 'mdi-graphql',
  title: 'Переупорядочить граф',
  subtitle: 'Переупорядочить граф',
  action: 'reorderGraph'
}

const SpaceCtxMenuReorderChoosingObjects = {
  icon: 'mdi-graphql',
  title: 'Переупорядочить выбранные объекты',
  subtitle: 'Переупорядочить выбранные на графе объекты',
  action: 'reorderChoosingObjects'
}

const SpaceCtxMenuCreateRelation = {
  icon: 'mdi-link-variant-plus',
  title: 'Создать связь',
  subtitle: 'Связать выбранные объекты',
  action: 'createRelation'
}

const SpaceCtxMenuFindRelation = {
  icon: 'mdi-link-variant',
  title: 'Найти связи',
  subtitle: 'Найти все связи между выбранными объектами',
  action: 'findRelations'
}

const SpaceCtxMenuDeleteChoosing = {
  icon: 'mdi-delete',
  title: 'Удалить выбранные объекты',
  subtitle: 'Удалить с графа все выбранные объекты',
  action: 'deleteObjects'
}

function getObjectCtxMenu(geometryToGraph) {
  let objectCtxMenu = [
    ObjectCtxMenuSearchRelation,
    ObjectCtxMenuChangeObject,
    ObjectCtxMenuDelete,
    ObjectCtxMenuSettings
  ]
  if(geometryToGraph) {
    objectCtxMenu.unshift(ObjectCtxMenuGeometryToMap)
  }
  return objectCtxMenu
}

function getSpaceCtxMenu(save, reorder, createRelation, findRelation, choosingObjects) {
  let spaceCtxMenu = [SpaceCtxMenuSpaceBase]
  if(save) {
    spaceCtxMenu.unshift(SpaceCtxMenuSave)
  }
  if(reorder) {
    spaceCtxMenu.unshift(SpaceCtxMenuReorder)
  }
  if(choosingObjects) {
    spaceCtxMenu.unshift(SpaceCtxMenuReorderChoosingObjects)
  }
  if(createRelation) {
    spaceCtxMenu.unshift(SpaceCtxMenuCreateRelation)
  }
  if(findRelation) {
    spaceCtxMenu.unshift(SpaceCtxMenuFindRelation)
  }
  if(choosingObjects) {
    spaceCtxMenu.push(SpaceCtxMenuDeleteChoosing)
  }
  return spaceCtxMenu
}

export default {getObjectCtxMenu, RelationCtxMenu, getSpaceCtxMenu}