//======================================================================
//=====   КЛАСС: МЕНЮ   ================================================
//======================================================================
// menu_struct      - структура меню, []
//     action:        click или сhange для input
//     type='':       eсли action.return = false - меню не закроется
//     type='':       eсли action === undefined  - пункт меню недоступен
//     input-объекты: click меню не закрывает
//     input-объекты: eсли var === undefined  - пункт меню не отображается
//     не располагать в субменю поле select внизу: после выбора курсор оказывается вне hover и меню закрывается
// menu_data        - сохранение данных input, select, check, radio-объектов, если не задано, то используется/создается __data__ click-объекта
// cb_create_before - callback до создания меню
// cb_create_after  - callback после создания меню в АСИНХРОННОМ РЕЖИМЕ
// cb_close         - callback перед закрытием меню
//======================================================================


    .on('contextmenu', d3.contextMenu(nodeMenu));

    nodeMenu = [
        {
            title: 'Подробно',
            icon:  'fa-file-text-o',
            action: function(self, d, i) {
                alert(d.unit_name);
            }
        },
        {
            title: 'Item #2',
            icon:  'fa-television',
            enabled: false,
            visible: false,
            id: 'mmm',
            action: function(self, d, i) {
                    console.log(i);
            }
        },
        {
            title: 'Item #3',
            submenu: [
                { title: '555', icon:  'fa-television' },
                { title: '777',
                  enabled: false,
                  submenu: [
                            {'title': '!!!!'},
                            {'title': 'wwww'}
                            ]
                },
                { type:  'separator' },
                {
                    type:  'checkbox',
                    title: 'Выбор checkbox #5 ferer er er e r e re rere rer',
                    var:   'ww5',
                    valOn:  true,
                    valOff: false,
                },
            ],
            //action: function(self, d, i) {
            //        console.log(i);
            //}
        },
        {
            title: 'Item #4',
            submenu: [
                { title: '5558', icon:  'fa-television' },
                { title: '7778' },
                { type:  'separator' },
                {
                    type:  'checkbox',
                    title: 'Выбор checkbox #8',
                    var:   'ww8',
                    valOn:  true,
                    valOff: false,
                },
            ],
            //action: function(self, d, i) {
            //        console.log(i);
            //}
        },
        {
            title: 'Item #5',
            submenu: [
                { title: '555', icon:  'fa-television' },
                { title: '777',
                  submenu: [
                            {'title': '!!!!'},
                            {'title': 'wwww'},
                            {
                            type:  'select',
                            icon:  'fa-television',
                            val:   [['red',    'красный8'],
                                    ['yellow', 'желтый8'],
                                    ['green',  'зеленый8'],
                                    ],
                            tip:   'помогите ...',
                            var:   'varSelect8',
                            },
                            ],
                },
                { type:  'separator' },
                {
                    type:  'checkbox',
                    title: 'Выбор checkbox #5 ferer er er e r e re rere rer',
                    var:   'ww5',
                    valOn:  true,
                    valOff: false,
                },
            ],
            //action: function(self, d, i) {
            //        console.log(i);
            //}
        },
        {   type:  'separator' },
        {
            type:  'select',
            title: 'Блок Select',
            icon:  'fa-television',
            val:   [['red',    'красный'],
                    ['yellow', 'желтый'],
                    ['green',  'зеленый'],
                   ],
            var:   'varSelect',
            tip:   'подказка',
        },
        {
            type:  'select',
            icon:  'fa-television',
            val:   [['red',    'красный2'],
                    ['yellow', 'желтый2'],
                    ['green',  'зеленый2'],
                   ],
            var:   'varSelect2',
        },
        {
            type:  'text',
            title: 'Ввод текста',
            icon:  'fa-television',
            var:   'varText',
            enabled: false,
        },
        {
            type:  'text',
            title: 'Ввод текста 2',
            var:   'varText2',
            tip:   'Подсказка !!!',
        },
        {
            type:  'text',
            icon:  'fa-television',
            var:   'varText3',
            tip:   'Подсказка 3',
        },
        {   type:  'separator' },
        {
            type:  'radio',
            title: 'Выбор radio #1',
            var:   'varRadio',
            val:   'tt1',
        },
        {
            type:  'radio',
            title: 'Выбор radio #2',
            var:   'varRadio',
            val:   'tt2',
        },
        {   type:  'separator' },
        {
            type:  'checkbox',
            title: 'Выбор checkbox #1',
            var:   'ww2',
            valOn:  true,
            valOff: false,
        },
        {
            type:  'checkbox',
            title: 'Выбор checkbox #2',
            var:   'ww3',
            valOn: 'Yes',
            valOff: 'No',
        },
    ];

