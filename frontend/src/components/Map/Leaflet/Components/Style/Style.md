# Decorators

## pattern
- создает дополнительные слои на основании patterns
- формируется динамически
- формируется с учетом color для конкретной фигуры или группы фигур (GeometryCollection)
- формируется только для линий и полигонов (не для маркеров)

## style и defs
- формируются динамически
- формируются для всего набора данных
- формируются с учетом текущего color
- обращение конкретной фигуры к ним осуществляется путем указания соответствующего класса
- для уникальности к имени класса дописывается постфикс (индекс в state.selectedTemplate.activeAnalysts)

## icon
- icon-svg- ...
- icon-file- ...
- icon-mdi- ...  [icon-mdi-spin]
- icon-fc- ...
- icon-pulse

  тип определяется по ПЕРВОМУ классу иконки
  первый класс определяет тип, остальные - дополнительные параметры
  'icon-mdi-flag icon-mdi-spin' => [['mdi', 'flag'], ['mdi', 'spin']]
  'icon-fs-spec0'
  'icon-pulse-30'
  'icon-file-gold-25-41'
  'icon-file-#00f'



  PROPERTIES: {
    CLASS:   'class',                 // key: класс для стилизации
    TEXT:    'text',                  // надпись на маркере, пока что только для svg-маркеров
    ZOOM:    'zoom',                  // масштабирование маркера: ['auto'], false, Numeric, пока что только для svg-маркеров
    HINT:    'hint',                  // всплывающая подсказка, НЕТ РЕАКТИВНОСТИ?
  },





 icon_get('icon-mdi-flag sss icon-mdi-spin tst')
 icon_get(className, color, 2);
 icon_get('', 'green'); icon_get('', '#00f');  COLOR_EQU
 icon_get();
