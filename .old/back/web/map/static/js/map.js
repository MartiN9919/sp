'use strict';

$(document).ready(function(){
    // чтобы скрыть не отформатированный html
    $('body').css('display', 'block').trigger('resize');

    // выбор меню выделить
    $('#nav-map').splitbutton('disable');

    // разворачивать панель при наведении указателя
    // let p_expand = $('#layout').layout('panel','expandWest');
    // p_expand.on('mouseover',function(){
    //     p_expand.trigger('click');
    // });

    let obj_map = new Map_organizer('layout-center');


    // $('#script-list').tree({
    //     url: 'tree_data.json',
    // // loadFilter: function(data){
    // //     if (data.d){
    // //         return data.d;
    // //     } else {
    // //         return data;
    // //     }
    // // }
    // });

});


