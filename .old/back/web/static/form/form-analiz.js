
// КЛАСС: МОДАЛЬНАЯ ФОРМА - ВЫБОР ЭЛЕМЕНТА
// IN:    obj_id - id объекта
// OUT:   {id: , text: }
//        id выбранного элемента (0 создать новый элемент, -1 отмена)

class FORM_ANALIZ {

constructor(options) {
    this.DELAY              = 1000;                                 // задержка поиска, мс

    this.RET                = {};                                   // аргумент cb_action
    this.RET_ID             = 'id';
    this.RET_TEXT           = 'text';
    this.RET[this.RET_ID  ] = -1;
    this.RET[this.RET_TEXT] = undefined;

    this.obj_name           = 'ddd';                // создаваемый DOM-элемент: #obj_name
    // this.obj_name           = options.obj_data.name;                // создаваемый DOM-элемент: #obj_name
    // this.obj_id             = options.obj_data.id;                  // объект: id
    // this.obj_icon           = options.obj_data.icon;                // объект: иконка
    // this.obj_title          = options.obj_data.title_single;        // объект: наименование
    // this.cb_action          = options.cb_action;                    // callback: выбранный id [N, -1 отмена, 0 новый]

    this.id_window          = this.html_id('');
    this.id_layout          = this.html_id('layout');
    this.id_layout_north    = this.html_id('layout_north');
    this.id_layout_center   = this.html_id('layout_center');
    this.id_layout_south    = this.html_id('layout_south');

    this.id_textbox         = this.html_id('north_textbox');
    this.id_datagrid        = this.html_id('center_datagrid');
    this.id_button_select   = this.html_id('button_select');
    this.id_button_create   = this.html_id('button_create');
    this.id_button_cancel   = this.html_id('button_cancel');


    // ***********************************************
    // ОКНО
    // ***********************************************
    this.html_set();
    return;
    $('#'+this.id_window).window({
        title:       '&nbsp;<i class="fa '+this.obj_icon+' fa-md"></i>&nbsp;&nbsp;'+this.obj_title.toUpperCase()+':&nbsp;&nbsp;выбрать элемент',
        modal:       true,
        maximizable: false,
        minimizable: false,
        collapsible: false,
        width:       '40%',
        height:      '80%',
        minWidth:    700,
        minHeight:   500,
        maxWidth:    '90%',
        maxHeight:   '90%',
        cls:         'select_off',
        onClose: function(){
            this.textbox_timer_off();
            this.cb_action(this.RET);
        }.bind(this),
    });
    this.jq_window = $('#'+this.id_window);

    // инициализация
    this.jq_window.attr('tabIndex','-1').css('outline-style','none').bind('keydown',function(e){    // tabIndex - возможность фокуса, outline-style - скрытие фокуса
        if (e.keyCode == 13){ this.jq_button_select.trigger('click'); } // ENTER
        if (e.keyCode == 27){ this.jq_window.window('close'); } // ESC
    }.bind(this));



    // ***********************************************
    // РАЗМЕТКА ОКНА
    // ***********************************************
    this.jq_window.append('<section id="'+this.id_layout+'"></section>');
    $('#'+this.id_layout)
        .layout({
            fit:      true,
        })
        .layout('add', {
            id:       this.id_layout_north,
            region:   'north',
            height:   '35px',
            border:   false,
            style: {
                'text-align': 'right',
                padding:      '0 0 5px 0',
            },
        })
        .layout('add', {
            id:       this.id_layout_center,
            region:   'center',
            border:   false,
        })
        .layout('add', {
            id:       this.id_layout_south,
            region:   'south',
            height:   '35px',
            border:   false,
            style: {
                'text-align': 'right',
                padding:      '5px 0 0 0',
            },
        });
    //this.jq_layout_north = $('#'+this.id_layout_north);
    this.jq_layout_center = $('#'+this.id_layout_center);
    this.jq_layout_south  = $('#'+this.id_layout_south);



    // ***********************************************
    // LAYOUT NORTH: TEXTBOX
    // ***********************************************
    $('#'+this.id_layout_north).append('<div id="'+this.id_textbox+'" style=""></div>');
    $('#'+this.id_textbox).textbox({
        //label:         'Найти:',
        //labelPosition: 'before',
        //labelAlign:    'left',
        prompt:        'Текст для идентифицикации объекта',
        width:         '100%',
        height:        '100%',
        icons:[{
            iconCls: 'icon-clear',
            handler: function(e){
                $(e.data.target).textbox('clear').textbox('textbox').focus();
                this.jq_textbox.textbox('getIcon',0).css('visibility','hidden');    // searchbox
                this.jq_textbox.textbox('textbox').trigger('input', '');            // this.textbox_input(undefined, '');
            }.bind(this),
        }],
    });
    this.jq_textbox = $('#'+this.id_textbox);

    // инициализация
    this.jq_textbox.textbox('textbox').focus();
    this.jq_textbox.textbox('textbox').bind('input', this.textbox_input);           // events set: input
    this.jq_textbox.textbox('textbox').trigger('input', '');                        // events fire: input



    // ***********************************************
    // LAYOUT CENTER: DATAGRID
    // ***********************************************
    $('#'+this.id_layout_center).append('<table id="'+this.id_datagrid+'"></table>');
    $('#'+this.id_datagrid).datagrid({
        //id:             'zzzzz',
        idField:        'id',
        showHeader:     false,
        // title:       'Найдено',
        // iconCls:     'icon-search',
        emptyMsg:       'Объекты отсутствуют',
        loadMsg:        'Загрузка ...',
        width:          '100%',
        height:         '100%',

        fit:            true,
        scrollbarSize:  0,

        lines:          true,
        nowrap:         true,
        singleSelect:   true,
        columns: [[
             { field: 'id',    hidden: true, },
             { field: 'title', width: '100%', },
        ]],
        onSelect: function(index,row){
            this.jq_button_select.linkbutton('enable');
        }.bind(this),
        onUnselect: function(index,row){
            this.jq_button_select.linkbutton('disable');
        }.bind(this),
        onDblClickRow: function(index,row){
            this.window_close(row.id);
        }.bind(this),
        loader: function(param, success, error){
            // this.jq_button_select.linkbutton('disable');
            var val = this.jq_textbox.val().trim();
            if (val=='') { success([]); return; }
            net_ajax({
                url:      AJ.EL_FIND,
                data:     {obj_id: this.obj_id, search: this.jq_textbox.textbox('getValue') },
                success:  function(data){
                     success(data);
                },
                error: function(){
                    error();
                },
            });
        }.bind(this),
        // onLoadSuccess:function(data){
        // }.bind(this),
        // onLoadError: function(XMLHttpRequest, textStatus, errorThrown){
        // }.bind(this),
    });
    this.jq_datagrid = $('#'+this.id_datagrid);



    // ***********************************************
    // LAYOUT SOUTH: BUTTON
    // ***********************************************
    $('#'+this.id_layout_south).append(
        '<a id="'+this.id_button_create+'" style="float:left;margin-right:5px;" href="#"></a>'+
        '<a id="'+this.id_button_select+'" style="margin-right:5px;" href="#"></a>'+
        '<a id="'+this.id_button_cancel+'" href="#"></a>'
    );
    $('#'+this.id_button_create).linkbutton({
        iconCls:  'icon-add',
        text:     'Создать',
        width:    150,
        onClick:  function(){
            this.window_close(0, this.jq_textbox.textbox('getValue').trim());
        }.bind(this),
    });
    $('#'+this.id_button_select).linkbutton({
        iconCls:  'icon-ok',
        text:     'Выбрать',
        width:    150,
        disabled: true,
        onClick:  function(){
            let row = this.jq_datagrid.datagrid('getSelected');
            if (row) { this.window_close(row.id); }
            else     { this.window_close(-1);     }
        }.bind(this),
    });
    $('#'+this.id_button_cancel).linkbutton({
        iconCls:  'icon-cancel',
        text:     'Отменить',
        width:    150,
        onClick:  function(){
            this.window_close(-1);
        }.bind(this),
    });
    this.jq_button_create = $('#'+this.id_button_create);
    this.jq_button_select = $('#'+this.id_button_select);
    this.jq_button_cancel = $('#'+this.id_button_cancel);
}



// ***********************************************
// ПСЕВДОДЕСТРУКТОР - вызывать принудительно
// ***********************************************
free = function(){
    this.textbox_timer_off();
    $('#'+this.obj_name+' *').unbind();
    this.html_clear();
}



// ***********************************************
// WINDOW
// ***********************************************
window_close = function(id, text=undefined){
    this.RET[this.RET_ID  ] = id;
    this.RET[this.RET_TEXT] = text;
    this.jq_window.window('close');
}.bind(this);



// ***********************************************
// TEXTBOX
// ***********************************************
// timer запустить
textbox_timer_off = function(){
    clearTimeout(this.event_timer);
    this.event_timer=undefined;
}.bind(this);

// timer остановить
textbox_timer_on = function(){
    this.textbox_timer_off();
    this.event_timer = setTimeout(function (){
        this.textbox_timer_off();
        this.jq_datagrid.datagrid('reload');
    }.bind(this), this.DELAY);
}.bind(this);

// обработка измененеия поля ввода: input
textbox_input = function(e, val_force){
    if (this.jq_button_select) this.jq_button_select.linkbutton('disable');     // недоступность кнопки выбора
    this.datagrid_unselect();                                                   // убрать выделение в datagrid
    var val = (val_force!==undefined)?val_force:$(e.target).val();              // читать содержимое поля ввода; $('#'+e.target.id).val();
    this.jq_textbox.textbox('setValue', val);                                   // зафиксировать изменения
    this.textbox_icon_clear(val);                                               // видимость иконки "очистить"
    this.textbox_timer_on();                                                    // таймер обновления
}.bind(this);

// видимость иконки "очистить"
textbox_icon_clear = function(val) {
    if (this.jq_textbox){
        let icon = this.jq_textbox.textbox('getIcon',0);
        if (val.trim()) { icon.css('visibility','visible'); } else { icon.css('visibility','hidden'); };    // icon.show() / hide() - глюки resize
    }
}.bind(this);



// ***********************************************
// DATAGRID
// ***********************************************
// убрать выделение
datagrid_unselect = function(){
    if (this.jq_datagrid){
        this.jq_datagrid.datagrid('unselectAll');
        this.jq_datagrid.datagrid('loadData', []);
    }
}.bind(this);



// ***********************************************
// HTML
// ***********************************************
html_id(id=''){ return this.obj_name+((id!='')?('_'+id):''); }
html_set(){
    this.html_clear();
    $('body').append('<div id="'+this.id_window+'"></div>');

    //onclick="open1('../../easyui/demo/window/inlinewindow.html',this)"
    $('#'+this.id_window).panel('refresh', '{% static "form/form-analiz.html" %}');

    //$('.easyui-window').window();
}
html_clear(){
    if (this.jq_window) {
        this.jq_window.parent().next('.window-shadow').remove();
        this.jq_window.parent().next('.window-mask').remove();
        this.jq_window.parent().remove();
    }
};


}
