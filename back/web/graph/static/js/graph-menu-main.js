class GRAPH_MENU_MAIN {

// ***********************************************
// INI
// ***********************************************
menu_main_ini = function(target){
    net_ajax({
        url:     AJ.SCRIPT_EXEC,
        data:    {script: AJ.SCRIPT_NAME.OBJ_LIST},
        success: function(data){
            this.main_menu_struct = [
                { title: 'Добавить объект',   icon: 'fa-plus',           submenu: [] },
                { title: 'Очистить холст',    icon: 'fa-trash',          action: this.node_delall_menu },
                { type:  'separator' },
                { title: 'Снять все отметки', icon: 'fa-check-circle',   action: this.node_mark_clearall_menu },
                { title: 'Открепить все',     icon: 'fa-thumbtack',      action: this.node_pin_clearall_menu },
                { type:  'separator' },
                { title: 'Сохранить как ...', icon: 'fa-save',           action: () => svg_save(this.SVG_JS) },
                { title: 'Копировать',        icon: 'fa-copy',           action: () => svg_copy(this.SVG_JS) },
                { title: 'Печать ...',        icon: 'fa-print',          action: () => svg_print(this.SVG_JS) },
                { type:  'separator' },
                { title: 'Справка',           icon: 'fa-info-circle',    action: this.menu_main_help },
                { title: 'Тест',              icon: 'fa-file-download',  action: this.node_test_action },
            ];
            for (let data_item of data) {
                if (data_item.name=='rel') continue;
                this.main_menu_struct[0]['submenu'].push(
                    {
                        id:     data_item.id,
                        title:  data_item.title_single.charAt(0).toUpperCase() + data_item.title_single.slice(1),
                        icon:   data_item.icon,
                        action: this.node_add_menu,
                        data:   data_item,
                    }
                );
            }
            target.on('contextmenu', d3.contextMenu(this.main_menu_struct, undefined, cb_create_before));
        }.bind(this),
        error: function(err){ alert('Ошибка: '+AJ.SCRIPT_EXEC+'.'+AJ.SCRIPT_NAME.OBJ_LIST); },
    });

    let cb_create_before = function(menu_struct, event, index){
        menu_struct[1].enabled = this.node_delall_enabled();
        menu_struct[3].enabled = this.node_mark_clearall_enabled();
        menu_struct[4].enabled = this.node_pin_clearall_enabled();
        menu_struct[6].enabled = menu_struct[1].enabled;
        menu_struct[7].enabled = (menu_struct[1].enabled && ((navigator.clipboard)?true:false));
        if (!(navigator.clipboard)) menu_struct[7].tip =
            'Для включения возможности копирования\n'+
            '1. в окне браузера наберите: chrome://flags\n'+
            '2. включите опцию: Insecure origins treated as secure\n'+
            '3. в поле под опцией укажите: '+window.location.protocol+'//'+window.location.host;
        menu_struct[8].enabled = menu_struct[1].enabled;
    }.bind(this);
};

// ***********************************************
// GRAPH: KEY
// ***********************************************
graph_key = function(){
    d3.select("body").on('keydown', function(e){
        if ((e.keyCode == 49)  && e.ctrlKey && e.shiftKey) { this.node_add_menu(this.main_menu_struct[0]['submenu'][0]); return; } // CTRL+SHIFT+1
        if ((e.keyCode == 50)  && e.ctrlKey && e.shiftKey) { this.node_add_menu(this.main_menu_struct[0]['submenu'][1]); return; } // CTRL+SHIFT+2
        if ((e.keyCode == 51)  && e.ctrlKey && e.shiftKey) { this.node_add_menu(this.main_menu_struct[0]['submenu'][2]); return; } // CTRL+SHIFT+3
        if ((e.keyCode == 52)  && e.ctrlKey && e.shiftKey) { this.node_add_menu(this.main_menu_struct[0]['submenu'][3]); return; } // CTRL+SHIFT+4
        if ((e.keyCode == 53)  && e.ctrlKey && e.shiftKey) { this.node_add_menu(this.main_menu_struct[0]['submenu'][4]); return; } // CTRL+SHIFT+5
        if ((e.keyCode == 54)  && e.ctrlKey && e.shiftKey) { this.node_add_menu(this.main_menu_struct[0]['submenu'][5]); return; } // CTRL+SHIFT+6
        if ((e.keyCode == 55)  && e.ctrlKey && e.shiftKey) { this.node_add_menu(this.main_menu_struct[0]['submenu'][6]); return; } // CTRL+SHIFT+7
        if ((e.keyCode == 56)  && e.ctrlKey && e.shiftKey) { this.node_add_menu(this.main_menu_struct[0]['submenu'][7]); return; } // CTRL+SHIFT+8
        if ((e.keyCode == 57)  && e.ctrlKey && e.shiftKey) { this.node_add_menu(this.main_menu_struct[0]['submenu'][8]); return; } // CTRL+SHIFT+9
        if ((e.keyCode == 112) && e.ctrlKey && e.shiftKey) { this.menu_main_help(); return; } // CTRL+F1
    }.bind(this));
};


menu_main_help = function(menu_item, data, sender, point){
    let tt = new FORM_INFO();
};






}
