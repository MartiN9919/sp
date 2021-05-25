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
d3.contextMenu = function (menu_struct, menu_data, cb_create_before, cb_create_after, cb_close) {
    let p = d3.selectAll('.d3MenuContext').data([1]);
    p.enter().append('ul').attr('class', 'd3MenuContext');
    p.exit().remove();

    // событие contextmenu
    return function(event, index) {
        // видны во ВСЕХ экземплярах, но допустимо, так как два меню не могут быть ОДНОВРЕМЕННО активированы
        ul_self    = this;
        ul_changed = false;
        menu_timer = undefined;

        // область данных если не задана, то создается как свойство объекта
        if ((menu_data===undefined) && (this.__data__===undefined)) this.__data__ = {};

        // cb_create_before
        if (cb_create_before) cb_create_before(menu_struct, event, index);

        // меню: создать
        itemsCreate(this, d3.selectAll('.d3MenuContext'), menu_struct);

        // меню: показать
        d3.select('.d3MenuContext')
            .style('left', (event.pageX - 2)  + 'px')
            .style('top',  (event.pageY - 22) + 'px')    // -2
            .style('display', 'block')

            // =====================================================
            // MENU.ON_MOUSELEAVE
            // =====================================================
            .on('mouseleave', function(event, data) {
                if (menu_timer) { menu_timer = timerAbort(menu_timer); }

                var d3_menu = d3.select(this);
                var data    = ((menu_data !== undefined) ? menu_data : ((ul_self)?ul_self.__data__:undefined));
                if (d3_menu.classed('d3MenuContext') && !(d3_menu.classed('d3MenuContextSubmenu'))) {
                    if (cb_close) cb_close(ul_changed, data);
                    ul_changed = false;
                    d3_menu.style('display', 'none').style('top', null).style('left', null).selectAll("li").remove();
                }
            });

        // отключить старое меню
        event.preventDefault();

        // остановить дальнейшую передачу события
        event.stopPropagation();

        // cb_create_after
        if (menu_timer) { menu_timer = runDelay(menu_timer, 100, cb_create_after); }
    };



    // self - элемент, на который повешено .on('contextmenu', d3.contextMenu ...)
    function itemsCreate(self, d3_menu_all, menu_struct) {
        d3_menu_all.html('');

        // удаление невидимых пунктов
        var menuVisible = [];
        menu_struct.forEach(function(d) { if (d['visible'] !== false) menuVisible.push(d); });

        d3_menu_all.selectAll('li').data(menuVisible).enter()
            .append('li')
            .attr('id', function(d) { return (d.id !== undefined) ? String(d.id) : null; })


            // =====================================================
            // ITEM.ON_CREATE
            // =====================================================
            .html(function(d) {
                var data = (menu_data !== undefined) ? menu_data : self.__data__, ret = '';
                if (d.visible === false) return ret;

                switch(d.type) {
                // cепаратор
                case 'separator': break;

                // radio: data[d.var] = d.val
                case 'radio':
                    if (d.var !== undefined) {
                        ret = '<label>'+
                                  '<input '+
                                      'type="radio" '+
                                      'name="'+d.var+'"'+
                                      ((data[d.var]     === d.val  ) ? ' checked'  : '')+
                                      ((d.enabled       === false  ) ? ' disabled' : '')+
                                  '>'+
                                  '<span>'+d.title+'</span>'+
                              '</label>';
                    }
                    break;

                // checkbox: data[d.var] = d.valOn | d.valOff [true | false]
                case 'checkbox':
                    if (d.valOn  === undefined) d.valOn  = true;
                    if (d.valOff === undefined) d.valOff = false;
                    if (d.var    !== undefined) {
                        ret = '<label>'+
                                  '<input '+
                                      'type="checkbox" '+
                                      'name="'+d.var+'"'+
                                      ((data[d.var] === d.valOn) ? ' checked'  : '')+
                                      ((d.enabled   === false  ) ? ' disabled' : '')+
                                  '>'+
                                  '<span>'+d.title+'</span>'+
                              '</label>';
                    }
                    break;

                // text
                case 'text':
                    if (d.var !== undefined) {
                        ret = '<i class="fa fa-md'+((d.icon !== undefined) ? (' '+d.icon) : '')+'"></i>'+
                              '<label>'+
                                  ((d.title !== undefined) ? ('<span>'+d.title+'</span>') : ('<span style="width: 0;"></span>'))+
                                  '<input '+
                                      'type="text" '+
                                      'name="'+d.var+'"'+
                                      'value="'+((data[d.var] !== undefined) ? data[d.var] : '')+'" '+
                                      ((d.tip           !== undefined) ? ('placeholder="'+d.tip+'" ') : '')+
                                      ((d.enabled       === false    ) ? 'disabled ' : '')+
                                  '>'+
                              '</label>';
                    }
                    break;

                // select
                case 'select':
                    if (d.var !== undefined) {
                        d.val.forEach(function(item) {
                            ret += '<option '+((data[d.var] === item[0]) ? 'selected ' : '')+'value="'+item[0]+'">'+item[1]+'</option>';
                        });
                        ret = '<i class="fa fa-md'+((d.icon !== undefined) ? (' '+d.icon) : '')+'"></i>'+
                              '<label>'+
                                  ((d.title !== undefined) ? ('<span>'+d.title+'</span>') : ('<span style="width: 0;"></span>'))+
                                  '<select '+
                                      'name="'+d.var+'"'+
                                      ((d.enabled === false) ? 'disabled ' : '')+
                                  '>'+
                                  ret+
                                  '</select>'+
                              '</label>';
                    }
                    break;

                // стандартный пункт меню
                default:
                    if ((d.action === undefined) && (d.submenu === undefined)) d.enabled = false;
                    ret = '<i class="fa fa-md'+((d.icon !== undefined) ? (' '+d.icon) : '')+'"></i>'+
                          '<label>'+d.title+'</label>';
                }
                return ret;
            })


            // =====================================================
            // ITEM.ON_CLICK
            // =====================================================
            // self - элемент, на который повешено .on('contextmenu', d3.contextMenu ...)
            // this = li
            // menu_item === this.__data__
            // =====================================================
            .on('click', function(event, menu_item) {
                // нет реакции
                if ((menu_item.submenu !== undefined) || (menu_item.enabled === false)) return;

                // action только для стандартного пункта, т.к. changed не вызывается
                if ((menu_item.action) && (menu_item.type === undefined)) {
                    var data = (menu_data !== undefined) ? menu_data : self.__data__;
                    if (menu_item.action(menu_item, data, self, d3.pointer(event, self)) !== false) {
                        d3.select('.d3MenuContext').style('display', 'none');
                    }
                }

                // отключить иные события
                event.stopPropagation();
            })

            // должно быть после создания элементов
            .classed('d3MenuContextItemDisabled',  function(d) { return (d.enabled === false); })
            .classed('d3MenuContextItemSeparator', function(d) { return (d.type    == 'separator'); })
            .attr('type',  function(d) { return ((d.type !== undefined) ? d.type : ((d.submenu !== undefined) ? 'submenu' : '')); })
            .attr('title', function(d) { return ((d.tip  !== undefined) ? d.tip  : ''); })



            // =====================================================
            // ITEM.ON_CHANGE
            // =====================================================
            // this = li
            // menu_item === this.__data__
            // =====================================================
            .on('change', function(event, menu_item) {
                // измененить данные
                var data = (menu_data !== undefined) ? menu_data : self.__data__;
                switch(menu_item.type) {
                    case 'radio':
                        data[menu_item.var] = menu_item.val;
                        ul_changed = true;
                        break;
                    case 'checkbox':
                        data[menu_item.var] = ((this.childNodes[0].childNodes[0].checked) ? menu_item.valOn : menu_item.valOff );  // d3.select(this)[0][0].children[0].children[0].checked
                        ul_changed = true;
                        break;
                    case 'text':
                        data[menu_item.var] = this.childNodes[1].childNodes[1].value;     // d3.select(this)[0][0].children[1].children[1].value
                        ul_changed = true;
                        break;
                    case 'select':
                        data[menu_item.var] = this.childNodes[1].childNodes[1].value;
                        ul_changed = true;
                        break;
                }
                if (menu_item.action) {
                    if (menu_item.action(menu_item, data, self) !== false) {
                        d3.select('.d3MenuContext').style('display', 'none');
                    }
                }

                // отключить иные события
                event.stopPropagation();
            })




            // =====================================================
            // ITEM.ON_MOUSEENTER
            // =====================================================
            .on('mouseenter', function(event, menu_item) {
                // показать субменю
                if ((menu_item.submenu === undefined) || (menu_item.enabled === false)) return;

                // удалить субменю
                d3.select(this).selectAll("ul").remove();

                // создать субменю
                var listSub = d3.select(this).append("ul").classed('d3MenuContext d3MenuContextSubmenu', true);
                itemsCreate(self, listSub, menu_item.submenu);

                // позиционировать субменю
                listSub.style('top',  (this.offsetTop   - 20)+'px');
                listSub.style('left', (this.offsetWidth - 0 )+'px');

                // отключить старое меню
                event.preventDefault();
            })


            // =====================================================
            // ITEM.ON_MOUSELEAVE
            // =====================================================
            .on('mouseleave', function(event, menu_item) {
                if (menu_item.submenu !== undefined) {
                    d3.select(this.parentNode).selectAll("ul").remove();
                }
            });
    }


};
