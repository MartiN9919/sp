// зависимости
// jQuery.js

//======================================================================
//=====   КЛАСС: ПРОКРУТКА ЭКРАНА ВВЕРХ   ==============================
//======================================================================
function classTopScroll() {
    this.scroll = function() { if ($(document).scrollTop() > 100) $('.classTopScroll').fadeIn(); else $('.classTopScroll').fadeOut(); }
    this.click  = function() { $('html,body').animate({ scrollTop: 0 }, 800); return false; }
    this.free   = function() { window.removeEventListener('scroll', this.scroll, false); $('.classTopScroll').on("click", null).remove(); }

    $('body').append('<i class="classTopScroll fa fa-toggle-up fa-3x" style="display: none;"></i>');
    $('.classTopScroll').on("click", this.click);
    window.addEventListener('scroll', this.scroll, false);
    this.scroll();
}



//======================================================================
//=====   КЛАСС: LOADER   ==============================================
//======================================================================
// родитель должен иметь стиль: position: fixed; ??? не надо
//======================================================================
function classLoader(selParent) {
    this.visible = function(isVisible) { $obj.css("display", (isVisible) ? "" : "none"); }

    $(selParent).append('<div class="classLoader select_off" style="display: none;"></div>');
    var $obj = $(selParent+' .classLoader');
}



//======================================================================
//=====   КЛАСС: ERR   =================================================
//======================================================================
// родитель должен иметь стиль: position: fixed; ??? не надо
//======================================================================
function classErr(selParent) {
    this.visible = function(text=undefined) {
        if (text !== undefined) {
            $obj.text(text);
            $obj.css("display", (text != "") ? "" : "none");
        } else {
            return $obj.text();
        }
    }

    $(selParent).append('<div class="classErr select_off" style="display: none;"></div>');
    var $obj = $(selParent+' .classErr');
}



//======================================================================
//=====   КЛАСС: ARR - стрелка влево  ==================================
//======================================================================
function classArr(selParent, text, left) {
    this.visible = function(isVisible, delayVisible=0) {
        $obj.css("display", (isVisible) ? "" : "none");
        if (isVisible && (delayVisible>0)) {
            setTimeout(this.visible.bind(this), delayVisible, false);
        }
    }
    this.top     = function(top)       { $obj.css("top",  top +"px"); }
    this.left    = function(left)      { $obj.css("left", left+"px"); }
    this.text    = function(text)      { $obj_text.text(text); }

    $(selParent).append(
        '<div class="classArr select_off" style="display: none; left: '+left+'px;">'+
            '<i class="fa fa-hand-point-left fa-md"></i>'+
            '<span>'+text+'</span>'+
        '</div>'
    );
    var $obj      = $(selParent+' .classArr');
    var $obj_text = $(selParent+' .classArr span');
}
