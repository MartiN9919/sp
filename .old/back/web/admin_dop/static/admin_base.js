// закладка
document.querySelector('head title' ).innerText = 'Сапфир админ';
document.querySelector('head').insertAdjacentHTML('afterbegin', '<link rel="shortcut icon" href="/static/img/logo/logo-title.png" type="image/png">');


// window.onload = function() { };
var windowOnloadAdd = function (event) {
   if (window.onload) { window.onload = window.onload + event; }
   else               { window.onload = event; };
};

windowOnloadAdd(function() {
    // заголовок
    document.querySelector('#site-name a').innerHTML = '<i class="far fa-gem"></i><span>САПФИР АДМИНИСТРАТОР</span>'
});




