/*
    Map_organizer               <--     Class_leaflet
        FORM_HIDE                      Class_leaflet_edit
        Class_jstree_checked            Class_leaflet_markers
        Map_edit
        Class_jstree_selected
*/


'use strict';

class Map_organizer extends Class_leaflet {
constructor(id_parent) {
    super(id_parent);

    const PANEL_NAME    = 'panel_managing';
    const GROUP_MODE    = 'mode';
    const ARR_DELAY     = 4000;                  // время видимости стрелки-подсказки

    this.map_objects    = [];


    this.ID_MODE_VIEW   = GROUP_MODE+'.view';
    this.ID_MODE_ANALIZ = GROUP_MODE+'.analiz';
    this.ID_MODE_MON    = GROUP_MODE+'.mon';
    this.ID_MODE_EDIT   = GROUP_MODE+'.edit';
    this.ID_MODE_MEDIA  = GROUP_MODE+'.media';
    const GROUP_MAP     = 'control_map';
    this.ITEM_MAP_SCHEMA_LOCAL_OSM       = GROUP_MAP+'.schema_local_osm';
    this.ITEM_MAP_SCHEMA_INTERNET_OSM    = GROUP_MAP+'.schema_internet_osm';
    this.ITEM_MAP_SCHEMA_INTERNET_MAP    = GROUP_MAP+'.schema_internet_map';
    this.ITEM_MAP_SCHEMA_INTERNET_STAMEN = GROUP_MAP+'.schema_internet_stamen';

    this.obj_panel = new FORM_HIDE('#form_hide_setting', {
        objName:     PANEL_NAME,
        objTitle:    'Панель управления',
        objWidth:    450,
        objPosition: 'left',
        selAnchor:   '#panel_main',
        arrText:     'Панель управления',
        arrDelay:    ARR_DELAY,
    });


    this.obj_tree = new Class_jstree_checked({
        sel_parent:       '#'+PANEL_NAME+' .panelScroll',
        callback_checked: this.map_refresh.bind(this),
        delay:            SYS.DELAY_ACTION,
        radio_groups:     [GROUP_MODE, GROUP_MAP, ],
        struct_data:      this.ini(),
    });

    this.obj_panel.show();

    this.layer_tile_set('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');


    this.obj_tree = new Class_jstree_checked({
        sel_parent: '#' + PANEL_NAME + ' .panelScroll',
        callback_checked: this.map_refresh.bind(this),
        radio_groups:     [GROUP_MODE, GROUP_MAP, ],
        struct_data: this.struct_menu_tree(),

    });
}



struct_menu_tree() {
    net_ajax({
        url:     AJ.SCRIPT_LIST,
        data:    {
            id: 1,
        },
        success: function(data){
            console.log(data)
            return data;
        }.bind(this),
    });
    // return [{
    // "id": 1,
    // "text": "Node 1",
    // "state": "closed",
    // }]
}

free() {
    this.obj_panel.hide();
    this.obj_panel.free();
    this.obj_panel = null;
    delete this.obj_panel;
}


ini() {
    let add_level_bind = add_level.bind(this);
    function add_level(id_parent) {
        let atd_children = [];
        for (let item of atd) {
            if (item[0] != id_parent) continue;
            atd_children.push({ id: item[1], text: item[3], icon: 'fa fa-cube fa-md', state: { }, 'children': add_level_bind(item[1]), });
        }
        return atd_children;
    }

    return [
    //*********************************************************************************************
    {
        id:       this.GROUP_MODE,
        text:     'Режим',                                      // '&nbsp;<i class=""></i>&nbsp;&nbsp;Режим'
        icon:     'fa fa-folder fa-md',                    // false
        a_attr:   { class: 'jstree-title no_checkbox', },
        state:    { checkbox_disabled: true, opened: true, },   // disabled: true,
        children: [
            { id: this.ID_MODE_VIEW,   text: 'Просмотр',       icon: 'fa fa-eye fa-md', state: { checked: true, selected: true }, },
            //{ id: this.ID_MODE_ANALIZ, text: 'Анализ',         icon: 'fa fa-chart-pie fa-md', state: { disabled: true, checkbox_disabled : true, }, },
            //{ id: this.ID_MODE_MON,    text: 'Мониторинг',     icon: 'fa fa-map fa-md', state: { disabled: true, checkbox_disabled : true, }, },
            { id: this.ID_MODE_EDIT,   text: 'Редактирование слоев', icon: 'fa fa-edit fa-md', state: { }, },
            { id: this.ID_MODE_MEDIA,  text: 'Работа с медиа',       icon: 'fa fa-camera fa-md', state: { }, },
        ],
    },

    //*********************************************************************************************
    {
        id:       'rr2',
        text:     'Объекты',                                    // '&nbsp;<i class="fa fa-layer-group fa-md"></i>&nbsp;&nbsp;Объекты',
        icon:     'fa fa-folder fa-md',
        a_attr:   { class: 'jstree-title no_checkbox', },
        state:    { checkbox_disabled: true, opened: true, },
        children: [
            {
                text:     'Происшествия',
                icon:     'fa fa-exclamation-triangle fa-md',
                a_attr:   { class: 'jstree-title no_checkbox', },
                state:    { checkbox_disabled: true, opened: true, },
                children: [
                    { id: 'inc.1', text: 'Наркотики', icon: 'fa fa-syringe fa-md',     state: { }, },
                    { id: 'inc.2', text: 'ТМЦ',       icon: 'fa fa-dollar-sign fa-md', state: { checked: true, selected: true }, },
                    { id: 'inc.3', text: 'Оружие',    icon: 'fa fa-bomb fa-md',        state: { checked: true, selected: true }, },
                    { id: 'inc.4', text: 'Мигранты',  icon: 'fa fa-running fa-md',     state: { checked: true, selected: true }, },
                ],
            },
            { text:   'Инженерные заграждения', icon: 'fa fa-hammer fa-md', state: { }, },
            { id: '3.4', text:   '33', icon: 'fa fa-question fa-md', },
            { id: '3.5', text:   '44', icon: 'fa fa-question fa-md', },
        ],
    },

    //*********************************************************************************************
    {
        id:       'atd',
        text:     'Административное деление',
        icon:     'fa fa-cube fa-md',
        state:    { checkbox_disabled : true, },
        a_attr:   { class: 'jstree-title no_checkbox', },
        children: add_level_bind('atd'),
    },

    //*********************************************************************************************
    {
        id:       'test.0',
        text:     'Тест',
        icon:     'fa fa-folder fa-md',
        state:    { checkbox_disabled: true, },
        a_attr:   { class: 'jstree-title no_checkbox ', },
        children: [
            { id: 'test.1',  text: 'obj_view_base',        icon: 'fa fa-cube fa-md', },
            { id: 'test.2',  text: 'Маркеры: png',         icon: 'fa fa-cube fa-md', }, //state : { disabled: true, checkbox_disabled : true, }, },
            { id: 'test.3',  text: 'Маркеры: pulse',       icon: 'fa fa-cube fa-md', },
            { id: 'test.4',  text: 'Маркеры: div',         icon: 'fa fa-cube fa-md', },
            { id: 'test.5',  text: 'Маркеры: color',       icon: 'fa fa-cube fa-md', },
            { id: 'test.6',  text: 'Маркеры: awesome',     icon: 'fa fa-cube fa-md', },
            { id: 'test.7',  text: 'Контрабанда сигарет',  icon: 'fa fa-cube fa-md', },
            { id: 'test.8',  text: 'Незаконная миграция',  icon: 'fa fa-cube fa-md', },
            { id: 'test.9',  text: 'Контрабанда алкоголя', icon: 'fa fa-cube fa-md', },
            { id: 'test.10', text: 'Минск',                icon: 'fa fa-cube fa-md', },
        ],
    },

    //*********************************************************************************************
    {
        id:       'control',
        text:     'Элементы',
        icon:     'fa fa-folder fa-md',
        a_attr:   { class: 'no_checkbox jstree-title', },
        state:    { checkbox_disabled: true, },
        children: [
            {
                id:         this.GROUP_MAP,
                text:       'Подложка',
                icon:       'fa fa-globe fa-md',
                a_attr:     { class: 'jstree-title no_checkbox', },
                state:      { checkbox_disabled : true, },
                children:   [
                    { id: this.ITEM_MAP_SCHEMA_LOCAL_OSM,       text: 'Схема - локальный сервер OSM', icon: 'fa fa-map fa-md', state: { }, },
                    { id: this.ITEM_MAP_SCHEMA_INTERNET_OSM,    text: 'Схема - интернет OSM',         icon: 'fa fa-map fa-md', state: { selected: true }, },
                    { id: this.ITEM_MAP_SCHEMA_INTERNET_MAP,    text: 'Схема - интернет MAP',         icon: 'fa fa-map fa-md', state: { }, },
                    { id: this.ITEM_MAP_SCHEMA_INTERNET_STAMEN, text: 'Схема - интернет stamen',      icon: 'fa fa-map fa-md', state: { }, },
                    //{ id: this.GROUP_MAP+'.satellite',       text: 'Спутник', icon: 'fa fa-satellite fa-md', state: { disabled: true, checkbox_disabled : true, visible: false, }, },
                ],
            },
            { id: 'control.scale', text: 'Масштаб', icon: 'fa fa-ruler fa-md', state: { checked: true, selected: true }, },
        ],
    },
    ];
}


map_refresh(data) {
    for (let item of data.del) {
        switch(item) {
        case this.ID_MODE_EDIT:  this.object_del(this.obj_edit ); break;
        case this.ID_MODE_MEDIA: this.object_del(this.obj_media); break;
        case 'control.scale':    this.element_del('scale'); break;
        default:                 this.object_layer_del(item);
        }
    };

    for (let item of data.add) {
        switch(item) {
        case this.ID_MODE_EDIT:                    this.obj_edit  = new Map_edit ({lf: this}); break;
        case this.ID_MODE_MEDIA:                   this.obj_media = new Map_media({lf: this}); break;

        case this.ITEM_MAP_SCHEMA_LOCAL_OSM:       this.layer_tile_set('http://192.168.56.1:8080/osm/{z}/{x}/{y}.png', {maxZoom: 18}, ); break;
        case this.ITEM_MAP_SCHEMA_INTERNET_OSM:    this.layer_tile_set('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'); break;
        case this.ITEM_MAP_SCHEMA_INTERNET_MAP:    this.layer_tile_set('https://api.mapbox.com/v4/mapbox.light/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoicmVhZGNvZGVsZWFybiIsImEiOiJjaWx6eGd6ZGgwOGt0dTlrcjRqbDI0cjIyIn0.TZnkCyunFnYBYzi6D7AepA'); break;
        case this.ITEM_MAP_SCHEMA_INTERNET_STAMEN: this.layer_tile_set('http://{s}.tile.stamen.com/toner/{z}/{x}/{y}.png'); break;

        case 'test.1':
            this.map_objects.push(
                new Class_leaflet_view_base({
                    obj_id:       item,
                    map:          this.map,
                    ajax_url:     AJ.POLYGON_GET_OSM,
                    ajax_param:   { 'polygon_name_list': ['Витебская область', 'Брестская область', 'Мядельский район'] },
                    title:        'Полигоны из ajax geojson',
                    hint:         'name',
                })
            );
            break;

        case 'test.2':
            this.map_objects.push(
                new Class_leaflet_view_base({
                    obj_id:       item,
                    map:          this.map,
                    ajax_url:     AJ.SCRIPT_EXEC,
                    ajax_param:   { script: AJ.SCRIPT_NAME.REL_TO_GEO, obj_name: 'point', keys_rel: ['ngg_smoke',], keys_obj: ['address'], where_dop: ['dat is null']}, // AJ.SCRIPT_NAME.TEST
                    marker_icon:  this.markers[this.leaflet_markers.MARKER_PNG],
                    title:        'Маркеры PNG',
                    hint:         'address',
                })
            );
            break;


        case 'test.3':
            this.map_objects.push(
                new Class_leaflet_view_base({
                    obj_id:       item,
                    map:          this.map,
                    ajax_url:     AJ.SCRIPT_EXEC,
                    ajax_param:   { script: AJ.SCRIPT_NAME.REL_TO_GEO, obj_name: 'point', keys_rel: ['ngg_migrate',], keys_obj: ['address']},
                    marker_icon:  this.markers[this.leaflet_markers.MARKER_PULSE_GREEN],
                    marker_group: L.MarkerClusterGroup,
                    title:        'Маркеры PULSE (группировка)',
                    hint:         'address',
                })
            );
            break;

        case 'test.4':
            this.map_objects.push(
                new Class_leaflet_view_base({
                    obj_id:       item,
                    map:          this.map,
                    ajax_url:     AJ.SCRIPT_EXEC,
                    ajax_param:   { script: AJ.SCRIPT_NAME.REL_TO_GEO, obj_name: 'point', keys_rel: ['ngg_tmc',], keys_obj: ['address']},
                    marker_icon:  this.markers[this.leaflet_markers.MARKER_DIV_125],
                    title:        'Маркеры DIV',
                    hint:         'address',
                })
            );
            break;

        case 'test.5':
            this.map_objects.push(
                new Class_leaflet_view_base({
                    obj_id:       item,
                    map:          this.map,
                    ajax_url:     AJ.SCRIPT_EXEC,
                    ajax_param:   { script: AJ.SCRIPT_NAME.REL_TO_GEO, obj_name: 'point', keys_rel: ['ngg_opg',], keys_obj: ['address']},
                    marker_icon:  this.markers[this.leaflet_markers.MARKER_COLOR_GREEN],
                    title:        'Маркеры COLOR',
                    hint:         'address',
                })
            );
            break;

        case 'test.6':
            this.map_objects.push(
                new Class_leaflet_view_base({
                    obj_id:       item,
                    map:          this.map,
                    ajax_url:     AJ.SCRIPT_EXEC,
                    ajax_param:   { script: AJ.SCRIPT_NAME.REL_TO_GEO, obj_name: 'point', keys_rel: ['ngg_npr',], keys_obj: ['address']},
                    marker_icon:  this.markers[this.leaflet_markers.MARKER_AWESOME_TEST],
                    title:        'Маркеры AWESOME',
                    hint:         'address',
                })
            );
            break;

        case 'test.7':
            this.map_objects.push(
                this.obj_view_color = new Class_leaflet_view_colors({
                    obj_id:     item,
                    map:        this.map,
                    ajax_url:   AJ.SCRIPT_EXEC,
                    ajax_param: { script: AJ.SCRIPT_NAME.REL_TO_GEO, obj_name: 'geometry', keys_rel: ['arial_1'], keys_obj: ['name', 'test_geo_color']},
                    title:      'КОНТРАБАНДА СИГАРЕТ',
                })
            );
            break;

        case 'test.8':
            this.map_objects.push(
                new Class_leaflet_view_colors({
                    obj_id:      item,
                    map:         this.map,
                    ajax_url:    AJ.SCRIPT_EXEC,
                    ajax_param:  { script: AJ.SCRIPT_NAME.REL_TO_GEO, obj_name: 'geometry', keys_rel: ['arial_2'], keys_obj: ['name', 'test_geo_color'], },
                    title:       'НЕЗАКОННАЯ МИГРАЦИЯ',
                    show_hint:   false,
                })
            );
            break;

        case 'test.9':
            this.map_objects.push(
                new Class_leaflet_view_colors({
                    obj_id:      item,
                    map:         this.map,
                    ajax_url:    AJ.SCRIPT_EXEC,
                    ajax_param:  { script: AJ.SCRIPT_NAME.REL_TO_GEO, obj_name: 'geometry', keys_rel: ['arial_3'], keys_obj: ['name', 'test_geo_color'], },
                    title:       'КОНТРАБАНДА АЛКОГОЛЯ',
                })
            );
            break;

        case 'control.scale': this.control_scale_add(); break;

        default:
            for (let item_atd of atd) {
                if (item_atd[1]==item) {
                    this.map_objects.push(
                        new Class_leaflet_view_base({
                            obj_id:     item_atd[1],
                            map:        this.map,
                            ajax_url:   AJ.POLYGON_GET_OSM,
                            ajax_param: { 'polygon_name_list': [item_atd[2],] },
                            hint:       'name',
                        })
                    );
                }
            }
        }
    };

}



// удалить произвольный объект
object_del(obj) {
    if (obj) {
        if (obj.free) obj.free();
        //delete obj;
        obj = null;
    }
}

// удалить объект-слой
object_layer_del(obj_id) {
    for (let ind=0; ind<this.map_objects.length; ind++) {
        if (obj_id==this.map_objects[ind].obj_id) {
            if (this.map_objects[ind].free) this.map_objects[ind].free();
            delete this.map_objects[ind];
            this.map_objects.splice([ind], 1);
            break;
        }
    }
}


}
