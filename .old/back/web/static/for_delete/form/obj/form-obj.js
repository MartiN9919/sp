//======================================================================
//=====   КЛАСС: МОДАЛЬНАЯ ФОРМА - ВВОД ДАННЫх   =======================
//======================================================================

class Form_obj {
// static COOK_FORM_OBJ_SVAR  = 'form_obj_svar';
// static COOK_FORM_OBJ_STOOL = 'form_obj_stool';

constructor(options) {
    this.obj_name    = options.obj_name || "form-obj";      // создаваемый DOM-элемент: #obj_name
    this.obj_id      = options.obj_id;                      // id объекта
    this.OBJ         = {};                                  // указатели на инициализированные классы-объекты
    this.DATA        = {};                                  // указатели на данные: obj - об объекте (sys_obj), key - sys_key

    // получить информацию об объекте
    net_ajax({
        url:     AJ.SCRIPT_EXEC,
        data:    {script: AJ.SCRIPT_NAME.KEY_LIST, obj: parseInt(this.obj_id),},
        success: this.ini.bind(this),
        error:   function(err){ alert('Ошибка получения информации об объекте id='+this.obj_id); }.bind(this),
    });
}

ini(data) {
    this.DATA.obj  = data.obj;
    this.DATA.keys = data.keys;
    $('#'+this.id_window).html('');

    // главное окно класса
    this.id_window = this.id('');
    $('body').append('<section id="'+this.id_window+'" class="select_off" style="padding:5px;"></section>');
    $('#'+this.id_window).window({    //dialog
        title:       '<i class="fa '+this.DATA.obj.icon+' fa-md"></i>&nbsp;&nbsp;'+this.DATA.obj.title_single.toUpperCase(),
        modal:       true,
        minimizable: false,
        collapsible: false,
        width:       600,
        height:      400,
    });

    // блоки
    this.id_layout        = this.id('layout');
    this.id_layout_search = this.id('layout_search');
    this.id_layout_result = this.id('layout_result');
    this.id_layout_button = this.id('layout_button');
    this.id_btn_select    = this.id('btn_select');
    this.id_btn_create    = this.id('btn_create');
    this.id_btn_cancel    = this.id('btn_cancel');

    $('#'+this.id_window).append('<section id="'+this.id_layout+'"></section>');
    $('#'+this.id_layout)
        .layout({
            fit:      true,
        })
        .layout('add', {
            id:       this.id_layout_search,
            region:   'north',
            height:   '35px',
        })
        .layout('add', {
            id:       this.id_layout_result,
            region:   'center',
        })
        .layout('add', {
            id:       this.id_layout_button,
            //cls:      'select_off',
            region:   'south',
            height:   '35px',
            border:   false,
            style: {
                'text-align': 'right',
                padding:      '5px 0 0 0',
            },
        });
    $('#'+this.id_layout_button).append(
        '<a id="'+this.id_btn_select+'" style="margin-right:5px;" href="#"></a>'+
        '<a id="'+this.id_btn_create+'" style="margin-right:5px;" href="#"></a>'+
        '<a id="'+this.id_btn_cancel+'" href="#"></a>'
    );
    $('#'+this.id_btn_select)
        .linkbutton({
            id:       this.id_btn_select,
            iconCls:  'icon-ok',
            text:     'Выбрать',
            width:    150,
            //disabled: true,
        });
    $('#'+this.id_btn_create)
        .linkbutton({
            id:       this.id_btn_create,
            iconCls:  'icon-add',
            text:     'Создать',
            width:    150,
        });
    $('#'+this.id_btn_cancel).linkbutton({
            id:       this.id_btn_cancel,
            iconCls:  'icon-cancel',
            text:     'Отменить',
            width:    150,
        });

    $('#'+this.id_btn_select).linkbutton('disable');



    // this.OBJ.val = new FORM_OBJ_VAL({
    //     id_parent: this.id_layout_search,
    //     data:      this.DATA,
    // });

    // // this.OBJ.key  = new FORM_OBJ_KEY({
    // //     parent:   '#'+this.obj_name+' .panel_key',
    // //     obj_info: this.DATA.info,
    // // });

    // // this.OBJ.find = new FORM_OBJ_FIND({
    // //     parent:   '#'+this.obj_name+' .panel_find',
    // // });


    return;

    // $(this.obj_selector).treegrid({
    //     idField:        'id',
    //     treeField:      'key',
    //     animate:        true,
    //     fit:            true,   // автоширина
    //     fitColumns:     true,   // автоширина
    //     scrollbarSize:  0,
    //     nowrap:         true,   // в одну строку
    //     singleSelect:   true,
    //     width:          '100%',
    //     height:         '100%',
    //     onResizeColumn: this.on_resize_col.bind(this),
    //     columns:[[
    //         { field: 'key', title: 'Ключ',     width: '30%', },
    //         { field: 'val', title: 'Значение', width: '50%', },
    //         { field: 'dat', title: 'Дата',     width: '20%', resizable: false, fixed: true, }, //width: '20%', },   // , align: 'right'
    //     ]],
    //     data: {
    //         //total:tree_data.length,
    //         rows: FORM_TREE.tree_child(_tree_data, 0),
    //     },
    //     // loadFilter: function(rows) {
    //     // },
    // });




    // events
    this.on_resize(undefined);
    window.addEventListener('resize', this.on_resize.bind(this), false);

    this.DOM.form.classed("mShow", true);
}

// генератор id элементов класса
id(id='') { return this.obj_name+((id!='')?('_'+id):''); }

free = function() {
    if (this.OBJ.val ) this.OBJ.val. free();
    if (this.OBJ.key ) this.OBJ.key. free();
    if (this.OBJ.find) this.OBJ.find.free();

    window.removeEventListener('resize', this.on_resize, false);
    this.DOM  = undefined;
    this.OBJ  = undefined;
    this.DATA = undefined;
}



mdClear() {
    // valList([]);
    // valText("");
    // mdErr('');
}

// mdUndo() {
//     // valList(dataListSel);
//     // valText(dataText);
//     // mdErr('');
// }

// mdEdit() {
//     if (funEdit !== undefined) { funEdit(); btn_close_click(); }
// }

btn_close_click() {
    // скрыть
    this.DOM.form.classed("mShow", false);

    // // отключить события формы
    // if (isText) { DOM.input.on("input", null); }
    // d3.selectAll(".mForm .mFieldSwitch").on("change", null);
    // DOM.btnClear .on("click", null);
    // DOM.btnUndo  .on("click", null);
    // DOM.btnEdit  .on("click", null);
    // DOM.btn_ok    .on("click", null);
    // DOM.btn_cancel.on("click", null);
    // DOM.close    .on("click", null);

    // очистить DOM
    this.DOM.form.transition().delay(700).remove();
    this.DOM.overlay.transition().delay(700).remove();
}

btn_ok_click() {
    // if (funOk !== undefined) funOk(valList(), valText());
    // btn_close_click();
}

mdErr(sErr = '') {
    this.DOM.err.attr("display", (sErr != '') ? null : "none");
    this.DOM.err.text(sErr);
}



// ============================================================
// RESIZE
// ============================================================
on_resize(element) {
    this.DOM.JS_panel_main.style.height = (document.documentElement.clientHeight-220)+'px';
    if (this.OBJ.val) this.OBJ.val.on_resize(element);
}



// ============================================================
//  ЧТЕНИЕ-ЗАПИСЬ ДАННЫХ
// ============================================================
// valList(val = undefined) { // баг d3.selectAll("#id .class")
//     // if (val !== undefined) {
//     //     d3.selectAll(".mForm .mFieldSwitch").property("checked", function(d, i){ return (findInArr(val, dataListAll[i][AJ_NAME]) >= 0); });
//     // } else {
//     //     ret = [];
//     //     var arr = d3.selectAll(".mForm .mFieldSwitch");
//     //     for(var i=0; i<arr[0].length; i++) { if (arr[0][i].checked) ret.push(arr[0][i].value); };
//     //     return ret;
//     // }
// }

// valText(val = undefined) {
//     // if (val !== undefined) { if (isText) DOM.input.property("value", val); }
//     // else { return (isText) ? DOM.input.property("value").trim() : ""; }
// }

}