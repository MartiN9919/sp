/**
 * ВСПЛЫВАЮЩАЯ ПАНЕЛЬ
 *
 * чистый JS
 * зависимости:
 * sys/sys-common.js
 * lib-internal/sys/sys_form.js
 * lib-internal/sys/sys_form.css
 * lib-internal/form/form.css
 *
 * 1    FORM_HIDE       КЛАСС-ОРГАНАЙЗЕР (ПАНЕЛЬ+TITLE+SCROLL_PANEL+LOADER+ERR)
 * @this    show                                            принудительно показать панель
 * @this    hide                                            принудительно скрыть панель
 * @this    loader                                          показать/скрыть loader
 * @this    err                                             показать/скрыть сообщение об ошибке
 * @this    free                                            деструктор
 *
 * 2    FORM_HIDE_LITE   БАЗОВЫЙ КЛАСС    (ТОЛЬКО ПАНЕЛЬ)
 * @this    free                                            деструктор
 *
 * @param   {string}    selParent_                          1,2 Селектор родительского элемента: '#id'; если несколько панелей, то родители должны быть РАЗНЫМИ
 * @param   {dict}      options                             1,2 Параметры
 *          {string}    objName         ['objPanelHide']    1,2 id создаваемого DOM-элемена: #objName
 *          {string}    objPosition     ['left']            2   расположение панели: ['left'], 'right'
 *          {number}    objWidth        [500]               1,2 width  объекта
 *          {number}    objWidthVisible [2]                 1,2 размер нескрываемой части панели, без 'px'
 *          {number}    objTimeVisible  [0]                 1   время принудительного отображения окна, с
 *          {number}    objHeight       [undefined]         1,2 height объекта, по умолчанию - автоматически
 *          {number}    objTop          [38],               2   top    объекта
 *          {string}    objTitle        [undefined]         1   заголовок окна
 *          {string}    selAnchor       [undefined]         2   селектор объекта, относительно которого устанавливается objTop и objHeight: '#id'
 *          {string}    arrText         ['']                1   текст стрелки-подсказки, только для objPosition=left, если не задано - не показывается
 *          {number}    arrTop          [50]                1   высота расположения стрелки-подсказки, только для objPosition=left
 *          {number}    arrDelay        [0]                 1   время видимости стрелки-подсказки, 0 - не скрывать, только для objPosition=left
 */
function FORM_HIDE(selParent, options) {
const
    POSITION_LEFT   = 'left',
    POSITION_RIGHT  = 'right';

var objName         = options.objName         || 'objPanelHide',
    objWidth        = options.objWidth        || 500,
    objHeight       = options.objHeight       || undefined,
    objWidthVisible = options.objWidthVisible || 2,
    objTitle        = options.objTitle        || undefined,
    objPosition     = options.objPosition     || POSITION_LEFT,
    objTimeVisible  = options.objTimeVisible  || 0,
    arrowText       = options.arrText         || '',
    arrowTop        = options.arrTop          || 50,
    arrowDelay      = options.arrDelay        || 0,
    arrowMouseEnter = undefined,
    DOM             = {};

// PUBLIC
this.show        = function()          { DOM.JS_obj.classList.add('active');    pin_set();      } //{ let val = '0';                              if (objPosition==POSITION_LEFT) DOM.JS_obj.style.left = val; else DOM.JS_obj.style.right = val; }}
this.hide        = function()          { DOM.JS_obj.classList.remove('active'); pin_set();      } //{ let val = (-objWidth+objWidthVisible)+'px'; if (objPosition==POSITION_LEFT) DOM.JS_obj.style.left = val; else DOM.JS_obj.style.right = val; }}
this.loader      = function(isVisible) { if (DOM.OBJ_LOADER) DOM.OBJ_LOADER.visible(isVisible); }
this.err         = function(text)      { if (DOM.OBJ_ERR)    DOM.OBJ_ERR   .visible(text);      }
this.free        = function() {
    arr_free();
    if (DOM.JS_title) DOM.JS_title.removeEventListener('click',     title_click);
    if (DOM.OBJ)      DOM.OBJ.free();
    DOM = undefined;
}

// скрыть панель даже при нахождении над ней курсора
var tabTimerHide = undefined;
this.hideHard= function() {
    if (DOM.JS_obj) {
        DOM.JS_obj.classList.remove('form_hide_left');
        tabTimerHide = runDelay(tabTimerHide, 1000, function() { DOM.JS_obj.classList.add('form_hide_left'); });
    }
}

// PRIVATE
ini(this);
arr_ini(this, arrowText, arrowTop);

function ini(self) {
    DOM.OBJ = new FORM_HIDE_LITE(selParent, options);
    DOM.JS_obj = document.querySelector('#'+objName);
    DOM.JS_obj.innerHTML = DOM.JS_obj.innerHTML+
        ((objTitle !== undefined     )?('<div class="mTitle select_off"><p>'+objTitle+'</p><i class="fa fa-thumbtack fa-md"></i></div>'):'')+  // используются классы модального окна form.css
        '<div '+
            'class="panelScroll" '+
            'style="'+
                'height: calc( 100% - '+((objTitle !== undefined)?'30':'0')+'px ); '+
        '"></div>';

    DOM.JS_title = document.querySelector('#'+objName+' .mTitle');
    DOM.JS_title.addEventListener('click', title_click);

    DOM.JS_title_pin = document.querySelector('#'+objName+' .mTitle i');
    pin_set();

    DOM.OBJ_LOADER = new classLoader('#'+objName);
    DOM.OBJ_ERR    = new classErr   ('#'+objName);

    // принудительное отображение
    if (objTimeVisible>0) {
        self.show();
        self.event_timer = setTimeout(() => self.hide(), objTimeVisible*1000);
        DOM.JS_obj.addEventListener('mouseenter', () => { clearTimeout(self.event_timer); }, {once: true});
    }
}

function title_click() { DOM.JS_obj.classList.toggle('active'); pin_set(); }
function pin_set()     { DOM.JS_title_pin.classList.toggle('hide', !(DOM.JS_obj.classList.contains('active'))); }


// СТРЕЛКА-ПОДСКАЗКА
function arr_ini(self, text, top) {
    if ((text == '') || (objPosition != POSITION_LEFT) || (!cookie_get_hints())) return;
    self.arr_text    = function(text)      { if (DOM.OBJ_ARR)    DOM.OBJ_ARR   .text(text);         }
    self.arr_top     = function(top)       { if (DOM.OBJ_ARR)    DOM.OBJ_ARR   .top (top);          }
    self.arr_left    = function(left)      { if (DOM.OBJ_ARR)    DOM.OBJ_ARR   .left(left);         }
    self.arr_visible = function(isVisible) { if (DOM.OBJ_ARR)    DOM.OBJ_ARR   .visible(isVisible, self.arrowDelay); }

    DOM.OBJ_ARR = new classArr   ('#'+objName);
    self.arr_text(arrowText);
    self.arr_top (DOM.JS_obj.offsetTop  + arrowTop);
    self.arr_left(DOM.JS_obj.offsetLeft + DOM.JS_obj.offsetWidth + 50);

    arrowMouseEnter = arr_mouse_over.bind(self);
    DOM.JS_obj.addEventListener('mouseover', arrowMouseEnter);

    self.arr_visible(true);
}

function arr_free() {
    if (DOM.JS_obj) DOM.JS_obj.removeEventListener('mouseover', arrowMouseEnter);
}

function arr_mouse_over(element) {
    this.arr_visible(false);
    arr_free();
}

}



// ======================================================================
function FORM_HIDE_LITE(selParent, options) {
const
    POSITION_LEFT   = 'left',
    POSITION_RIGHT  = 'right';
var objName         = options.objName         || 'objPanelHide',
    objWidth        = options.objWidth        || 500,
    objTop          = options.objTop          || 38,
    objHeight       = options.objHeight       || undefined,
    objPosition     = options.objPosition     || POSITION_LEFT,
    objWidthVisible = options.objWidthVisible || 2,
    selAnchor       = options.selAnchor       || undefined,
    DOM             = {};


// PUBLIC
this.free = function() {
    window.removeEventListener('resize', resize, false);
    if (DOM.JS_parent) DOM.JS_parent.removeChild(DOM.JS_obj);
    DOM = undefined;
}


// PRIVATE
ini();
function ini() {
    //DOM.JS_body           = document.querySelector('body');
    DOM.JS_parent           = document.querySelector(selParent);
    DOM.JS_parent.innerHTML = DOM.JS_parent.innerHTML+                          // не совсем корректно, но в данном случае применимо: см. panel-block.js
        '<div '+
            'id="'+objName+'" '+
            'class="form_hide form_hide_'+objPosition+'" '+
            'style="'+
                'width: ' +objWidth +'px; '+
                'top: '   +objTop   +'px; '+
                ((objHeight !== undefined     )?('height: '+objHeight+'px; '):'')+
                ((objPosition ===  POSITION_LEFT )?('left: '  +(-objWidth+objWidthVisible)+'px; '):'')+
                ((objPosition ===  POSITION_RIGHT)?('right: ' +(-objWidth+objWidthVisible)+'px; '):'')+
        '"></div>';
    DOM.JS_obj = document.querySelector('#'+objName);

    // --- events ----------------------------------------------------------------------------------------
    resize(undefined);
    window.addEventListener('resize', resize, false);
}

// EVENT RESIZE
function resize(element) {
    DOM.JS_obj = document.querySelector('#'+objName);
    if (selAnchor !== undefined) {
        var JS_anchor_top    = document.querySelector(selAnchor).offsetTop;
        DOM.JS_obj.style.top = (JS_anchor_top + 5)+'px';
        DOM.JS_obj.offsetTop = (JS_anchor_top + 5);
        if (objHeight === undefined) DOM.JS_obj.style.height = 'calc( 100% - '+(JS_anchor_top + 5)+'px - 10px )';
    } else {
        if (objHeight === undefined) DOM.JS_obj.style.height = 'calc( 100% - '+objTop+'px - 10px )';
    }
}

}
