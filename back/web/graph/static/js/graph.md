



    // ГЛАВНОЕ МЕНЮ
    topmenu_item_ini('nav-graph', [
        //{id: 'graph-add',   icon: 'fa-plus',        title: 'Добавить элемент',  menu: [],},
        //{id: 'graph-other', icon: 'fa-info-circle', title: 'Разное',            action: function(){ alert('Добавить')}},
        //{},
        //{id: 'graph-set',   icon: 'fa-cog',         title: 'Настройки',         action: function(){ alert('Добавить5')}},
    ])
    //this.JQ_MNU_ADD = $('#graph-add > ul.submenu').last();
    this.JQ_MNU_ADD = $('#nav-graph > ul.submenu').last();
    this.NAV_INP    = 'nav_inp2';
    net_ajax({
        url:     AJ.SCRIPT_EXEC,
        data:    {script: AJ.SCRIPT_NAME.OBJ_LIST},
        success: function(data){
            for (let data_item of data) {
                // кроме rel-объекта
                if (data_item.name=='rel') continue;
                // добавить пункт меню
                this.JQ_MNU_ADD.append(
                    '<li id="'+this.NAV_INP+'_'+data_item.id+'" '+
                        'data-obj_id="'+         data_item.id+'" '+
                        'data-obj_name="'+       data_item.name+'" '+
                        'data-obj_title="'+      data_item.title+'" '+
                        'data-obj_name_single="'+data_item.title_single+'" '+
                        'data-obj_icon="'+       data_item.icon +'" '+
                        '>'+
                        '<i class="fa '+data_item.icon+' fa-md"></i>'+
                        data_item.title_single+
                    '</li>'
                );
                //$('#'+this.NAV_INP+'_'+data_item.id).on('click', this.nav_inp_click.bind(this));
            }
        }.bind(this),
        error: function(err){ alert('Ошибка: '+AJ.SCRIPT_EXEC+'.'+AJ.SCRIPT_NAME.OBJ_LIST); },
    });



// блок defs
//defsAdd("#panel_main");

var data_nodes =  [
    {"name": "Lillian", "obj": "F", mark: true},
    {"name": "Gordon", "obj": "M", mark: true},
    {"name": "Sylvester", "obj": "M", mark: false},
    {"name": "Mary", "obj": "F"},
    {"name": "Helen", "obj": "F"},
    {"name": "Jamie", "obj": "M"},
    {"name": "Jessie", "obj": "F"},
    {"name": "Ashton", "obj": "M"},
    {"name": "Duncan", "obj": "M"},
    {"name": "Evette", "obj": "F"},
    {"name": "Mauer", "obj": "M"},
    {"name": "Fray", "obj": "F"},
    {"name": "Duke", "obj": "M"},
    {"name": "Baron", "obj": "M"},
    {"name": "Infante", "obj": "M"},
    {"name": "Percy", "obj": "M"},
    {"name": "Cynthia", "obj": "F"},
    {"name": "Feyton", "obj": "M", mark: true},
    {"name": "Lesley", "obj": "F"},
    {"name": "Yvette", "obj": "F"},
    {"name": "Maria", "obj": "F"},
    {"name": "Lexy", "obj": "F"},
    {"name": "Peter", "obj": "M"},
    {"name": "Ashley", "obj": "F"},
    {"name": "Finkler", "obj": "M"},
    {"name": "Damo", "obj": "M"},
    {"name": "Imogen", "obj": "F"},
    ]

var data_links = [
    {"source": "Sylvester", "target": "Gordon", "type":"A" },
    {"source": "Sylvester", "target": "Lillian", "type":"A" },
    {"source": "Sylvester", "target": "Mary", "type":"A"},
    {"source": "Sylvester", "target": "Jamie", "type":"A"},
    {"source": "Sylvester", "target": "Jessie", "type":"A"},
    {"source": "Sylvester", "target": "Helen", "type":"A"},
    {"source": "Helen", "target": "Gordon", "type":"A"},
    {"source": "Mary", "target": "Lillian", "type":"A"},
    {"source": "Ashton", "target": "Mary", "type":"A"},
    {"source": "Duncan", "target": "Jamie", "type":"A"},
    {"source": "Gordon", "target": "Jessie", "type":"A"},
    {"source": "Sylvester", "target": "Fray", "type":"E"},
    {"source": "Fray", "target": "Mauer", "type":"A"},
    {"source": "Fray", "target": "Cynthia", "type":"A"},
    {"source": "Fray", "target": "Percy", "type":"A"},
    {"source": "Percy", "target": "Cynthia", "type":"A"},
    {"source": "Infante", "target": "Duke", "type":"A"},
    {"source": "Duke", "target": "Gordon", "type":"A"},
    {"source": "Duke", "target": "Sylvester", "type":"A"},
    {"source": "Baron", "target": "Duke", "type":"A"},
    {"source": "Baron", "target": "Sylvester", "type":"E"},
    {"source": "Evette", "target": "Sylvester", "type":"E"},
    {"source": "Cynthia", "target": "Sylvester", "type":"E"},
    {"source": "Cynthia", "target": "Jamie", "type":"E"},
    {"source": "Mauer", "target": "Jessie", "type":"E"},
    {"source": "Duke", "target": "Lexy", "type":"A"},
    {"source": "Feyton", "target": "Lexy", "type":"A"},
    {"source": "Maria", "target": "Feyton", "type":"A"},
    {"source": "Baron", "target": "Yvette", "type":"E"},
    {"source": "Evette", "target": "Maria", "type":"E"},
    {"source": "Cynthia", "target": "Yvette", "type":"E"},
    {"source": "Maria", "target": "Jamie", "type":"E"},
    {"source": "Maria", "target": "Lesley", "type":"E"},
    {"source": "Ashley", "target": "Damo", "type":"A"},
    {"source": "Damo", "target": "Lexy", "type":"A"},
    {"source": "Maria", "target": "Feyton", "type":"A"},
    {"source": "Finkler", "target": "Ashley", "type":"E"},
    {"source": "Sylvester", "target": "Maria", "type":"E"},
    {"source": "Peter", "target": "Finkler", "type":"E"},
    {"source": "Ashley", "target": "Gordon", "type":"E"},
    {"source": "Maria", "target": "Imogen", "type":"E"}

]

