// ЗАВИСИМОСТИ: alerts

// ВКЛЮЧЕНИЕ / ОТКЛЮЧЕНИЕ УВЕДОМЛЕНИЙ
const NAV_ALERTS = 'nav_alerts';
function cookie_get_alerts() {
    let val = getCook(NAV_ALERTS, true)
    return ((val == 'true') || (val == true));
}
function nav_alerts(show, menu_action=true) {
    setCook(NAV_ALERTS, show, 3600*24*30);

    // Пункты меню: отображение
    document.getElementById('nav_alerts_on' ).style.display = show?'none':'';
    document.getElementById('nav_alerts_off').style.display = show?'':'none';

    // Режим
    alerts.monitor(show);

    // Информатор
    if (menu_action) alertify.success('Уведомления '+(show?'ВКЛЮЧЕНЫ':'ОТКЛЮЧЕНЫ'));
}

// // ВИДИМОСТЬ ГЛАВНОГО МЕНЮ
// const NAV_FIXPOS = 'nav_fixpos';
// function cookie_get_fixpos() {
//     let val = getCook(NAV_FIXPOS, true)
//     return ((val == 'true') || (val == true));
// }
// function nav_fixpos(show, menu_action=true) {
//     setCook(NAV_FIXPOS, show);

//     // Пункты меню: отображение
//     document.getElementById('nav_fixpos_on' ).style.display = show?'none':'';
//     document.getElementById('nav_fixpos_off').style.display = show?'':'none';

//     // Режим
//     $('.body-layout').layout((show)?'expand':'collapse', 'north');

//     // Информатор
//     if (menu_action) alertify.success('Главное меню: '+(show?'ЗАКРЕПИТЬ':'СКРЫВАТЬ'));
// };


$(document).ready(function(){
    nav_alerts(cookie_get_alerts(), false);
    // av_fixpos(cookie_get_fixpos(), false);
    // let p_expand = $('.body-layout').layout('panel','expandNorth');
    // p_expand.on('mouseover',function(){
    //     p_expand.trigger('click');
    // });
});