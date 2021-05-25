//**********************************************************************
//*****   ИНИЦИАЛИЗАЦИЯ   **********************************************
//**********************************************************************

// выбор меню выделить
topmenu_select('navMap');

DOM = {};

resize(undefined);
window.addEventListener('resize', resize, false);


let obj_map    = new Map_organizer('map');


// ============================================================
// RESIZE
// ============================================================
function resize(element) {
    var JS_body = document.querySelector('body');
    var JS_map  = document.querySelector('#panel_main');
    JS_body.style.height = (document.documentElement.clientHeight - 1)+'px';
    JS_map.style.height  = (document.documentElement.clientHeight - JS_map.offsetTop - 1)+'px';
}
