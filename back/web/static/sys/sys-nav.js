// ЧИСТЫЙ JAVA SCRIPT
// ЗАВИСИМОСТИ: alerts

// ЛОГОТИП
let logo       = document.querySelector('li.item_logo span');
logo.innerText = logo.innerText.toUpperCase();

logo.onmouseover = function(event) {
    document.querySelector('li.item_logo span').classList.add('blink_on');
    setTimeout(function() {
        document.querySelector('li.item_logo span').classList.remove('blink_on')}, 500);
};
delete logo;

// ПРИЗНАК СУБМЕНЮ
document.querySelectorAll('#menu_main li').forEach(function(node) {
    if (node.querySelector('ul')) node.classList.add('has_submenu');
});

// ВИДИМОСТЬ ГЛАВНОГО МЕНЮ
const TOPMENU_FIXPOS = 'topmenu_fixpos';
topmenu_fixpos(cookie_get_fixpos(), false);
function cookie_get_fixpos() {
    let val = getCook(TOPMENU_FIXPOS, true)
    return ((val == 'true') || (val == true));
}
function topmenu_fixpos(show, menu_action=true) {
    setCook(TOPMENU_FIXPOS, show);

    // Пункты меню
    document.getElementById('topmenu_fixpos_on' ).style.display = show?'none':'';
    document.getElementById('topmenu_fixpos_off').style.display = show?'':'none';

    // Класс-признак фиксации меню
    let menu_main = document.getElementById('menu_main');
    if (show) menu_main.classList.add   ('topmenu_fixpos')
    else      menu_main.classList.remove('topmenu_fixpos');

    // Fake-панель: высота
    let menu_main_fake = document.getElementById('menu_main_fake');
    if (show) menu_main_fake.style.height = menu_main.style.height
    else menu_main_fake.style.height = '0px';

    // глобальное событие resize
    window.dispatchEvent(new Event('resize'));

    // Информатор
    if (menu_action) alertify.success('Главное меню: '+(show?'ЗАКРЕПИТЬ':'СКРЫВАТЬ'));
};


// ОТКЛЮЧЕНИЕ ПОДСКАЗОК
const TOPMENU_HINTS = 'topmenu_hints';
topmenu_hints(cookie_get_hints(), false);
function cookie_get_hints() {
    let val = getCook(TOPMENU_HINTS, true)
    return ((val == 'true') || (val == true));
}
function topmenu_hints(show, menu_action=true) {
    setCook(TOPMENU_HINTS, show, 3600*24);

    // Пункты меню
    document.getElementById('topmenu_hints_on' ).style.display = show?'none':'';
    document.getElementById('topmenu_hints_off').style.display = show?'':'none';

    // Команда
    alerts.monitor(show);

    // Информатор
    if (menu_action) alertify.success('Подсказки '+(show?'ВКЛЮЧЕНЫ':'ОТКЛЮЧЕНЫ'));
}


// ОТКЛЮЧЕНИЕ УВЕДОМЛЕНИЙ
const TOPMENU_ALERTS = 'topmenu_alerts';
topmenu_alerts(cookie_get_alerts(), false);
function cookie_get_alerts() {
    let val = getCook(TOPMENU_ALERTS, true)
    return ((val == 'true') || (val == true));
}
function topmenu_alerts(show, menu_action=true) {
    setCook(TOPMENU_ALERTS, show, 3600*24*30);

    // Пункты меню
    document.getElementById('topmenu_alerts_on' ).style.display = show?'none':'';
    document.getElementById('topmenu_alerts_off').style.display = show?'':'none';

    // Команда
    alerts.monitor(show);

    // Информатор
    if (menu_action) alertify.success('Уведомления '+(show?'ВКЛЮЧЕНЫ':'ОТКЛЮЧЕНЫ'));
}


// ОТМЕТИТЬ ПУНКТ ГЛАВНОГО МЕНЮ КАК ТЕКУЩИЙ
function topmenu_select(id) {
    document.querySelector('#'+id+' a').removeAttribute('href');
    document.getElementById(id).classList.add('item_select');
}

// // СКОРРЕКТИРОВАТЬ ПУНКТ ГЛАВНОГО МЕНЮ КАК РАБОЧИЙ
// // DOM:
// //      li.has_submenu
// //          a
// //              i
// //              'text'
// //              ::after
// //          ul.submenu
// //
// //    topmenu_item_ini('nav-graph', [
// //        {id: 'graph-add',   icon: 'fa-plus',        title: 'Добавить элемент',  action: function(){ alert('Добавить')}},
// //        {id: 'graph-other', icon: 'fa-info-circle', title: 'Разное',            menu: [
// //            {id: 'graph-add1',   icon: 'fa-plus',        title: 'Добавить элемент1',  action: function(){ alert('Добавить1')}},
// //            {id: 'graph-add2',   icon: 'fa-plus',        title: 'Добавить элемент2',  action: function(){ alert('Добавить2')}},
// //        ],},
// //        {},
// //        {id: 'graph-set',   icon: 'fa-cog',         title: 'Настройки',         action: function(){ alert('Добавить5')}},
// // допустимо menu=[]
// function topmenu_item_ini(id, menu=undefined) {
//     function add_ul(parent, menu=undefined){
//         if (menu==undefined) return;

//         // добавить ul submenu
//         parent.classList.add('has_submenu');
//         let ul = document.createElement('ul');
//         ul.classList.add('submenu');
//         parent.appendChild(ul);

//         let li, a, icon;
//         menu.forEach(function(item, i, arr) {
//             li = document.createElement('li');

//             if ((item.id || '')=='')  {                                 // сепаратор: menu_item == {}
//                 li.classList.add('divider');
//                 ul.appendChild(li);
//                 return;
//             }

//             a    = document.createElement('a');                         // иное
//             icon = document.createElement('i');
//             a .appendChild(icon);
//             li.appendChild(a);
//             ul.appendChild(li);
//             if (item.id)     li.setAttribute('id', item.id);
//             if (item.action) li.onclick = item.action;
//             icon.classList.add('fa', item.icon, 'fa-md');
//             icon.after(item.title);

//             // подменю
//             if (item.menu!=undefined) {
//                 li.classList.add('has_submenu');
//                 add_ul(li, item.menu);
//             }
//         });
//     }

//     document.querySelector('#'+id+' a').removeAttribute('href');
//     let parent=document.getElementById(id);
//     parent.classList.add((menu.length==0)?'item_select':'item_work');    // при отсутствии меню - аналог topmenu_select
//     add_ul(parent, menu);
// }

