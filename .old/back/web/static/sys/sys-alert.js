// ЧИСТЫЙ JAVA SCRIPT

// ЗАВИСИМОСТИ:

// УБРАТЬ: В HTML КОДЕ ДОЛЖЕН БЫТЬ ЭЛЕМЕНТ id=user_id, КОТОРЫЙ СОДЕРЖИТ id текущего пользователя (nav.html)
// alertify
// lib-internal/sys/sys-net.js

!(function (global, undefined) {
    "use strict";

    var Alerts;
    Alerts = function () {
        var get_timeout, get_interval;

        alertify.init();
        alertify.set({ buttonReverse: true });                                      // порядок кнопок

        // ВКЛЮЧИТЬ/ОТКЛЮЧИТЬ ПРИЕМ СООБЩЕНИЙ (ПО УМОЛЧАНИЮ ВКЛЮЧЕН)
        function get(forcibly=false) {
            net_ajax({
                url:     AJ.ALERT_GET,
                success: function(data) {
                    if (data == undefined) return;
                    //const user_id = global.document.getElementById('user_id').innerText;
                    const cook_id = 'alerts_id_'; //+user_id+'_';
                    for (let data_item of data) {
                        if ((!forcibly) && (getCook(cook_id+data_item.id)=='true')) continue;
                        if (data_item.type=='info') data_item.type='success';
                        alertify.log(data_item.content, data_item.type, data_item.wait*1000);
                        setCook(cook_id+data_item.id, true, 3600*24*7);                 // повторение через 7 дней
                    }
                },
            });
        }
        function monitor_start(interval) {
            get_timeout  = setTimeout (function() { get(false); }, 30*1000);             // первый запуск через 30 секунд
            get_interval = setInterval(function() { get(false); }, 60*1000*interval);    // каждые 10 минут
        }
        function monitor_stop() {
            clearTimeout(get_timeout);   get_timeout =undefined;
            clearInterval(get_interval); get_interval=undefined;
        }

        // УСТАНОВИТЬ СООБЩЕНИЕ, ТОЛЬКО АДМИНИСТРАТОР ИЛИ ТОЛЬКО АДМИНИСТРАТОРУ
        function set(content, type, wait, descript, users, groups) {
            net_ajax({
                url:     AJ.ALERT_SET,
                data:    { 'content': content, 'type': type, 'wait': wait, 'descript': descript, 'users': users, 'groups': groups },
                success: function(data) { alertify.success('Сообщение отправлено'); },
                error:   function()     { alertify.error  ('Ошибка'); },
            });

        }

        // ДИАЛОГ: ПРИЕМ И ОТПРАВКА СООБЩЕНИЯ ТОЛЬКО АДМИНИСТРАТОРУ
        function dlg_admin() {
            alertify.prompt("Текст сообщения администратору", function (e, str) {
                if (e) {
                    set(str, 'info', 0, 'от пользователя с сайта', '1', '');
                }
            });
        }

        return {
            // ВКЛЮЧИТЬ/ОТКЛЮЧИТЬ ПРИЕМ СООБЩЕНИЙ (ПО УМОЛЧАНИЮ ВКЛЮЧЕН)
            monitor   : function (start=true, interval=10) { start?monitor_start(interval):monitor_stop(); },
            // ПРИНУДИТЕЛЬНО ПОКАЗАТЬ ВСЕ СООБЩЕНИЯ
            get       : function () { get(true); },
            // УСТАНОВИТЬ СООБЩЕНИЕ, ТОЛЬКО АДМИНИСТРАТОР ИЛИ ТОЛЬКО АДМИНИСТРАТОРУ: alerts.set(...);
            set       : function (content, type='info', wait=0, descript='', users='', groups='') { set(content, type, wait, descript, users, groups); },
            // ДИАЛОГ: ПРИЕМ И ОТПРАВКА СООБЩЕНИЯ ТОЛЬКО АДМИНИСТРАТОРУ
            dlg_admin : function () { dlg_admin(); }
        };

    };

    // GLOBAL
    if (typeof define === "function") {
        define([], function () { return new Alerts(); });
    } else if (typeof global.alerts === "undefined") {
        global.alerts = new Alerts();
    }
    global.alerts.monitor();

}(this));
