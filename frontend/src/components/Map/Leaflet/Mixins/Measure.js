export default {
  methods: {
    measure_options() {
      let COLOR = '#494';          // цвет маркеров и линий
      return {
        position:                'topleft',
        unit:                    'metres',
        measureControlClasses:   ['select_off'],
        clearMeasurementsOnStop: true,
        measureControlTitleOn:   'Рулетка: включить',
        measureControlTitleOff:  'Рулетка: выключить',
        tooltipTextDelete:       'Нажмите  SHIFT и кликните мышкой для <b>удаления точки</b>',
        tooltipTextResume:       '<br>Нажмите CTRL и кликните мышкой для <b>продолжения линии</b>',
        tooltipTextAdd:          'Нажмите CTRL и кликните мышкой для <b>добавления точки</b>',
        tooltipTextFinish:       '',
        tooltipTextMove:         '',
        backgroundColor:         '#dfd',
        tempLine:                { color: COLOR, weight: 2, },
        fixedLine:               { color: COLOR, weight: 2, },
        startCircle:             { color: COLOR, weight: 1, fillColor: '#0f0', fillOpacity: 1, radius: 5, },
        intermedCircle:          { color: COLOR, weight: 1, fillColor: '#ff0', fillOpacity: 1, radius: 5, },
        currentCircle:           { color: COLOR, weight: 1, fillColor: '#f0f', fillOpacity: 1, radius: 5, },
        endCircle:               { color: COLOR, weight: 1, fillColor: '#f00', fillOpacity: 1, radius: 5, },
      }
    },
  },

};
