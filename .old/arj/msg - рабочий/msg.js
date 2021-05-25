// ЧИСТЫЙ JAVA SCRIPT, ЗАВИСИМОСТЕЙ НЕТ

// Анонимная самовызывающаяся функция-обертка msg
// @param {document} d - получает документ
// https://web3r.ru/js-css-alerts

// использование
// msg({
//     content: 'Привет!',
//     content: "<img src='https://placeimg.com/100/100/any' style='width:5em; height: 5em; border-radius: 100%; float: left; margin-right: .5em;'> <b>Lorem Ipsum</b> is simply dummy text of the printing and typesetting industry.",
//     type: 'error',
//     time: 10
// });

!function(d) {
    // Строгий режим
    "use strict";

    // Полифилл для Object.assign()
    Object.assign||Object.defineProperty(Object,"assign",{enumerable:!1,configurable:!0,writable:!0,value:function(e,r){"use strict";if(null==e)throw new TypeError("Cannot convert first argument to object");for(var t=Object(e),n=1;n<arguments.length;n++){var o=arguments[n];if(null!=o)for(var a=Object.keys(Object(o)),c=0,b=a.length;c<b;c++){var i=a[c],l=Object.getOwnPropertyDescriptor(o,i);void 0!==l&&l.enumerable&&(t[i]=o[i])}}return t}});
    // Полифилл для Element.remove()
    "remove" in Element.prototype||(Element.prototype.remove=function(){this.parentNode&&this.parentNode.removeChild(this)});

    // Основная функция.
    // @param {Object} [settings] - предвартиельные настройки
    window.msg = function(settings) {
        // Настройки по умолчанию
        settings = Object.assign({},{
            callback:    false,
            content:     "",
            time:        4.5,
            type:        "info"
        }, settings);

        if (!settings.content.length) return;

        // Функция создания элементов
        // @param {String} name      - название DOM-элемента
        // @param {Object} attr      - объект с атрибутами
        // @param {Object} append    - DOM-элемент, в который будет добавлен новый узел
        // @param {String} [content] - контент DOM-элемента
        var create = function(name, attr, append, content) {
            var node = d.createElement(name);
            for (var val in attr) { if(attr.hasOwnProperty(val)) node.setAttribute(val, attr[val]); }
            if (content) node.insertAdjacentHTML("afterbegin", content);
            append.appendChild(node);
            if (node.classList.contains("msg-item-hidden")) node.classList.remove("msg-item-hidden");
            return node;
        };

        // Генерация элементов
        var noteBox = d.getElementById("notes") || create("div", { "id": "notes" }, d.body);
        var noteItem = create(
            "div",
            {
                "class":     "msg-item",
                "data-show": "false",
                "role":      "alert",
                "data-type": settings.type
            },
            noteBox),
            noteItemText = create("div", { "class": "msg-item-text" }, noteItem, settings.content),
            noteItemBtn  = create("button", {
                "class":      "msg-item-btn",
                "type":       "button",
                "aria-label": "Скрыть"
            },
            noteItem);

        // Функция проверки видимости алерта во viewport
        // @returns {boolean}
        var isVisible = function() {
            var coords = noteItem.getBoundingClientRect();
            return (
                coords.top    >= 0 &&
                coords.left   >= 0 &&
                coords.bottom <= (window.innerHeight || d.documentElement.clientHeight) &&
                coords.right  <= (window.innerWidth  || d.documentElement.clientWidth)
            );
        };

        // Функция удаления алертов
        // @param {Object} [el] - удаляемый алерт
        var remove = function(el) {
            el = el || noteItem;
            el.setAttribute("data-show","false");
            window.setTimeout(function() { el.remove(); }, 250);
            if (settings.callback) settings.callback(); // callback
        };

        // Удаление алерта по клику на кнопку
        noteItemBtn.addEventListener("click", function() { remove(); });

        // Визуальный вывод алерта
        window.setTimeout(function() { noteItem.setAttribute("data-show","true"); }, 250);

        // Проверка видимости алерта и очистка места при необходимости
        if (!isVisible()) remove(noteBox.firstChild);

        // Автоматическое удаление алерта спустя заданное время
        window.setTimeout(remove, settings.time * 1000);
    };
}(document);

// пример
// var exampleBtns = document.querySelectorAll("[data-type][data-text]");
// exampleBtns.forEach(function(el) {
//     el.addEventListener("click", function(e) {
//         msg({
//             content: e.target.dataset.text,
//             type: e.target.dataset.type,
//             time: 5
//         });
//     });
// });

// <p id="content">
//     <button type="button" class="btn" data-type="info" data-text="Уведомление">
//       Info
//     </button>
//     <button type="button" class="btn" data-type="warn" data-text="Предупреждение">
//       Warn
//     </button>
//     <button type="button" class="btn" data-type="success" data-text="Успешное действие">
//       Success
//     </button>
//     <button type="button" class="btn" data-type="error" data-text="Ой, вот ведь незадача">
//       Error
//     </button>
//     <button type="button" class="btn" data-type="warn" data-text="<img src='https://placeimg.com/100/100/any' style='width:5em; height: 5em; border-radius: 100%; float: left; margin-right: .5em;'> <b>Lorem Ipsum</b> is simply dummy text of the printing and typesetting industry.">
//       Warn
//     </button>
//     <button type="button" class="btn" data-type="error" data-text="<span style='display: block; font-size: 120%; padding-bottom: .25em; font-weight: 500;'>Lorem Ipsum</span>is simply dummy text of the printing and typesetting industry.">
//       Error
//     </button>
//     <button type="button" class="btn" data-type="info" data-text="<b>Lorem Ipsum</b> is simply dummy text of the printing and typesetting industry. Lorem Ipsum <u>has been the industry's standard</u> dummy text ever since the 1500s">
//       Long Info
//     </button>
//   </p>
