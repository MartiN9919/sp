'use strict';

class Map_edit {
constructor({lf}) {
    this.PANEL_NAME     = 'panel_edit';
    this.lf             = lf;
    this.obj_panel      = new FORM_HIDE('#form_hide_tools', {
        objName:        this.PANEL_NAME,
        objTitle:       'Редактирование слоев',
        objWidth:       400,
        objPosition:    'right',
        objTimeVisible: 10,
        selAnchor:      '#panel_main',
    });

    this.refresh();
    this.obj_panel.show();
}

free() {
    this.obj_panel.hide();
    this.edit_off();

    if (this.obj_tree) {
        this.obj_tree.free();
        this.obj_tree = null;
        delete this.obj_tree;
    }

    this.obj_panel.free();
    this.obj_panel = null;
    delete this.obj_panel;
}


refresh() {
    this.obj_panel.loader(true);
    net_ajax({
        url:     AJ.SCRIPT_EXEC,
        data:    { script: AJ.SCRIPT_NAME.GEOMETRY_TREE, parent_id: 0, },
        success: function(data) {
            // // data = [[id, name, icon], ... ]
            // //     {'id': 1, 'category': 'item1/item2', 'name': 'test1', },
            // //     {'id': 2, 'category': 'item1/item2', 'name': 'test2', },
            // //     {'id': 3, 'category': 'item1/item3', 'name': 'test3', },
            // // ]

            // // нормализовать category: обрезать по сторонам пробелы, убрать последний слэш, разбить в список
            // for (let ind_data in data) {
            //     data[ind_data]['id']       = data[ind_data]['id'].toString();
            //     data[ind_data]['parent']   = data[ind_data]['category'].trim().replace(/\/$/, '');
            //     data[ind_data]['category'] = data[ind_data]['parent'].split('/');
            //     //data[ind_data]['category'].push(data[ind_data]['name'].trim());

            //     // добавить узлы-пути
            //     let item_id = '', item_parent = '', item_category = '';
            //     for (let ind_category in data[ind_data]['category']) {
            //         item_category = data[ind_data]['category'][ind_category];
            //         item_parent = item_id;
            //         item_id     = (item_id!='')?item_id+'/'+item_category:item_category;
            //         let rec     = data.filter(item => item['id']==item_id);
            //         if (rec.length == 0) {
            //             data.push({
            //                 'id':       item_id,
            //                 'category': data[ind_data]['category'].slice(0,-1),
            //                 'parent':   item_parent,
            //                 'name':     item_category,
            //             });
            //         }
            //     }
            //     //delete data[ind_data]['category'];
            // }


            // // сортировать по KEY_PARENT, KEY_NAME
            // data.sort(function (a, b) {
            //     let a_len = a['category'].length;
            //     let b_len = b['category'].length;
            //     if (a_len       > b_len)       { return  1; }
            //     if (a_len       < b_len)       { return -1; }
            //     if (a['parent'] > b['parent']) { return  1; }
            //     if (a['parent'] < b['parent']) { return -1; }
            //     if (a['name']   > b['name'])   { return  1; }
            //     if (a['name']   < b['name'])   { return -1; }
            //     return 0;
            // });


            // function data_to_tree(id_parent) {
            //     let ret = [];
            //     let data_parent = data.filter(function(item) { return (item['parent']==id_parent) } );
            //     for (let data_parent_ind in data_parent) {
            //         let data_parent_item = data_parent[data_parent_ind];
            //         let ret_item         = {
            //             id:       data_parent_item['id'].toString(),
            //             text:     data_parent_item['name'],
            //             children: data_to_tree(data_parent_item['id']),
            //             icon:     'fa fa-layer-group fa-md',
            //         };
            //         if (ret_item.children.length>0) {
            //             ret_item.icon   = 'fa fa-folder fa-md';
            //             ret_item.a_attr = { class: 'jstree-title', };
            //         }
            //         ret.push(ret_item);
            //     }
            //     return ret;
            // }

            // data
            // var tree = data_to_tree(0); //this.map_ini();

            // ВРЕМЕННО - ДЕМО
            var tree = [];
            for (let data_item of data) {
                let item = {
                    id:       data_item['id'].toString(),
                    text:     data_item['name'],
                    children: 0,
                    icon:     'fa '+data_item['icon']+' fa-md',
                };
                tree.push(item);
            }

            this.obj_tree = new Class_jstree_selected({
                sel_parent:  '#'+this.PANEL_NAME+' .panelScroll',
                cb_selected: this.selected.bind(this),
                delay:       SYS.DELAY_ACTION,
                struct_data: tree,
            });
            this.obj_panel.loader(false);
        }.bind(this),
    });
}


selected(nodes) {
    if (nodes.new=='') { this.edit_off(); return; }
    net_ajax({
        url:  AJ.SCRIPT_EXEC,
        data: {
            script: AJ.SCRIPT_NAME.GEOMETRY_GET,
            id:     nodes.new,
        },
        success: function(nodes, data) {  // [37, "location", "{"type": "GeometryCollection", "geometries": [{"ty…8.048096, 56.383502], [26.938477, 55.621793]]]}]}"]
            if (nodes.old!='' || data.length!=1) { this.edit_off(); }
            if (nodes.new!='') { this.edit_on(JSON.parse(data[0][2])); }
        }.bind(this, nodes),
        error: function(nodes) {
            alertify.error('Ошибка чтения '+nodes.new);
        }.bind(this, nodes),
    });
}

data_server_set(id, data) {
    net_ajax({
        url: AJ.SCRIPT_EXEC,
        data: {
            script:   AJ.SCRIPT_NAME.GEOMETRY_SET,
            data:     [ ['id', id], ['location', JSON.stringify(data)]],
        },
        success: function(id, ret) {
            if (ret[0]) alertify.success('Сохранено!')
            else        alertify.error  ('Ошибка сохранения (id '+id+'):'+ret[1]);
        }.bind(this, id),
        error: function(id) {
            alertify.error('Ошибка сохранения (id '+id+')');
        }.bind(this, id),
    });
}

edit_on(data) {
    this.leaflet_edit = new Class_leaflet_edit({
        map:          this.lf.map,
        data:         data,
        cb_data_save: function(data) {
            this.data_server_set(this.obj_tree.selected_id_old, data);
        }.bind(this),
        marker_red:   this.lf.markers[this.lf.leaflet_markers.MARKER_COLOR_RED],
    });
}

edit_off() {
    if (this.leaflet_edit) { this.leaflet_edit.free(); delete this.leaflet_edit; }
}



}
