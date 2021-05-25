/*
 * NEW
 */

// COOKIES
function setCook(name, value, max_age=3600*24*30*12*30) {   // 30 лет
    document.cookie = encodeURIComponent(name)+"="+encodeURIComponent(value)+"; path=/; max-age="+max_age;
}
function getCook(name, valueEmpty) {
    let matches = document.cookie.match(new RegExp("(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"));
    return matches ? decodeURIComponent(matches[1]) : valueEmpty;
}



/*
 * OLD
 */
const ID_DEFS_GLOBAL = 'defsGlobal';

// ПРОТОТИПЫ
// заменить все
String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
};

function dig2(val){ return ("0"+val).slice(-2); }

// Генерация случайного целого числа в диапазоне [lo..up]
function iRnd(lo, up) { return Math.floor(Math.random()*(up-lo+1)+lo); }
// Генерация случайного массива [0..len-1] целых чисел в диапазоне [lo..up]
function iRndArr(len, lo, up) { var data = []; for (var i=0; i<len; i++) { data.push(iRnd(lo, up)); } return data; }

// обработка NaN
function noNaN(val) { if (isNaN(val)) return 0; else return val; }

// обработка undefinedd
//function noUndefinedStr(val) { if (val === undefined) return ''; else return val; }

function randomInteger(min, max) {
  var rand = min + Math.random() * (max - min)
  rand = Math.round(rand);
  return rand;
}

// переместить элемент массива
function arrayMove(arr, fromIndex, toIndex) {
    var element = arr[fromIndex];
    arr.splice(fromIndex, 1);
    arr.splice(toIndex, 0, element);
}

// генерация уникального числа (ts+)
function uniqueInteger() { return (Date.now()*100)+randomInteger(0, 99); }

// первая буква заглавная
function capitalize(str) { return str.charAt(0).toUpperCase() + str.slice(1); }
// убрать пробелы по краям
function strip(str) { return str.replace(/\s+/g, ''); }
// заменить < > на мнемоники
function strMnemonic(str) {
    const KEY = '!A!T!L!A!S!';
    return str
        .replaceAll('<span>', KEY+'1')
        .replaceAll('</span>', KEY+'2')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll(KEY+'2', '</span>')
        .replaceAll(KEY+'1', '<span>');
}


// ЛУЧШЕ ИСПОЛЬЗОВАТЬ d3.event.ctrlKey
//**********************************************************************
//*****   КЛАВИАТУРА   *************************************************
//**********************************************************************
//var isCtrl = false;
//var keyDown = function(event){
//    isCtrl = event.ctrlKey;
//     //if(event.keyCode === 16 || event.charCode === 16){
//     //    window.shiftDown = true;
//     //}
// };

// var keyUp = function(event){
//     isCtrl = event.ctrlKey;
//     //if(event.keyCode === 16 || event.charCode === 16){
//     //    window.shiftDown = false;
//     //}
// };

// window.addEventListener ? document.addEventListener('keydown', keyDown) : document.attachEvent('keydown', keyDown);
// window.addEventListener ? document.addEventListener('keyup',   keyUp)   : document.attachEvent('keyup',   keyUp);


//**********************************************************************
//*****   РАБОТА С КУРСОРОМ   ******************************************
//**********************************************************************
function getCaretPos(element) {
    //element.focus();
    if (document.selection) {
        var sel = document.selection.createRange();
        var clone = sel.duplicate();
        sel.collapse(true);
        clone.moveToElementText(element);
        clone.setEndPoint('EndToEnd', sel);
        return clone.text.length;
    } else {
        return window.getSelection().getRangeAt(0).startOffset;
    }
    return 0;
}


function setCaretPos(element, pos) {
    if (element[0].firstChild == null) return;
    var sText = element[0].textContent;
    if (sText == '') return;
    var range = document.createRange();
    range.setStart(element[0].firstChild, Math.min(pos, sText.length));
    range.collapse(true);

    var sel= window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
}




//**********************************************************************
//*****   ДАТА - ВРЕМЯ   ***********************************************
//**********************************************************************
// !!! в БД cервака время хранится без UTC, хотя он уже учтен !!!
// UTC = -10 800 000
// UTC клиента может не соответствовать действительности или он может быть в разных часовых поясах, но результат всегда будет верным
function timezoneOffsetMinutes() { return new Date().getTimezoneOffset(); }
var myUTC = timezoneOffsetMinutes()*60*1000; //

function tsNowUTC() { return Math.floor(new Date().getTime())/1000; }

// перевод TS с сервера(GMT без миллисекунд) в TS клиента (GMT+UTC с миллисекундами)
function tsServerToClient(timestamp)    { return (timestamp*1000)+myUTC; }              // на клиенте JS сама добавит UTC
function tsServerToClientInv(timestamp) { return (timestamp*1000)-myUTC; }
function tsClientToServer(timestamp)    { return Math.floor((timestamp-myUTC)/1000); }
function tsClientToServerInv(timestamp) { return Math.floor((timestamp+myUTC)/1000); }

// Date в поле ввода Input (YYYY-MM-DDTHH:MM)
function dateToInput(val) { return val.getFullYear()+"-"+dig2(val.getMonth()+1)+"-"+dig2(val.getDate())+'T'+dig2(val.getHours())+":"+dig2(val.getMinutes()); }
function tsServerToInput(timestamp) { return dateToInput(tsToDate(timestamp)); }

// вывод даты на экран (GMT без учета UTC)
// можно выводить получаемую от сервера инфо * 1000
function tsServerToScreen(timestamp, isTime = true) { return tsClientToScreen(timestamp * 1000, isTime); }
function tsClientToScreen(timestamp, isTime = true) {
    var d = new Date(timestamp);
    var yyyy = d.getFullYear();
    var mm = dig2(d.getMonth() + 1);
    var dd = dig2(d.getDate());
    if (isTime) {
        var hh  = d.getHours();
        var min = dig2(d.getMinutes());
        return dd+'.'+mm+'.'+yyyy+' '+hh+':'+min;
    } else {
        return dd+'.'+mm+'.'+yyyy;
    }
}


function tsToDate(timestamp) {
    var ret = new Date();
    ret.setTime(timestamp*1000);
    return ret;
}

function tomorrow() {
    var ret = new Date();
    ret.setDate(ret.getDate()+1);
    ret.setHours(0, 0, 0, 0);
    return ret;
}

function secToStr(sec) {
    var h = Math.floor(sec/3600),
        m = Math.floor(sec/60)-(Math.floor(sec/3600)*60),
        s = sec % 60;
    var hStr = (h > 0) ? h      +" час. " : "",
        mStr = (m > 0) ? dig2(m)+" мин. " : "",
        sStr = (s > 0) ? dig2(s)+" сек. " : "";
    return hStr+mStr+sStr;
}


//======================================================================
//=====   ИНФОРМАТОРЫ  =================================================
//======================================================================
function loader(parentSelector, isVisible, dy = 0) {   // parentSelector - не обязательно непосредственный родитель
    var $obj    = $(parentSelector+' .loader');
    $obj.css("display", (isVisible) ? "" : "none");
}

function msgErr(parentSelector, text, dy = 0) {   // parentSelector - не обязательно непосредственный родитель
    var $obj    = $(parentSelector+' .msgerr');
    $obj.text(text);
    $obj.css("display", (text != "") ? "" : "none");
}

// дополнительная информация
function infoDop(val1, val2) {
    var n = val2 - val1;
    var ret = (n > 0) ? ("+"+String(n)) : String(n);
    if (val1 > 0) {
        n = Math.floor(val2 * 100 / val1) - 100;
        n = (n > 0) ? ("+"+String(n)) : String(n);
        ret = ret + " (" + n + "%)";
    }
    return ret;
}




//**********************************************************************
//*****   JSON URL URI   ***********************************************
//**********************************************************************
function isURLSearch()  { return (location.search != ""); }
function URLToJSON()    { return URIToJSON(location.search.substr(1)); }
function JSONToURL(val) { return "search?"+JSONToURI(val); }

function JSONToURI(val) { return encodeURIComponent(JSON.stringify(val)); }
function URIToJSON(val) { return (val != "") ? JSON.parse(decodeURIComponent(val)) : undefined; }
function openURLFromJSON(val, pathname=location.pathname) {
   var URL = location.protocol+"//"+location.host+pathname;
   if (URL[URL.length-1] != '/') URL += '/';
   URL += JSONToURL(val);
   window.open(URL, '_blank');
}
function urlHost() {
    var ret = location.protocol+"//"+location.host;
    if (ret[ret.length-1] != '/') ret += '/';
    return ret;
}
function visTypeToURL(type) { return "/vis/aj/"+type+"/"; }



//**********************************************************************
//*****   STRING  ******************************************************
//**********************************************************************
// прототипы удаления пробелов'
if (typeof(String.prototype.trim)  === "undefined") { String.prototype.trim  = function() { return String(this).replace(/^\s+|\s+$/g, ''); } }
if (typeof(String.prototype.ltrim) === "undefined") { String.prototype.ltrim = function() { return String(this).replace(/^\s+/, ''); } }
if (typeof(String.prototype.rtrim) === "undefined") { String.prototype.rtrim = function() { return String(this).replace(/\s+$/, ''); } }

function replaceNbsps(str) { return str.replace(/\&nbsp\;/gi, ' '); }

// замена "&lt;", "&gt;", ...
function convertNbsps(convert) { return $("<span />", { html: convert }).text(); };


// ПОИСК В МАССИВЕ
if ([].indexOf) {
    var findInArr = function(array, value) { return array.indexOf(value); }
} else {
    var findInArr = function(array, value) {
        for (var i = 0; i < array.length; i++) { if (array[i] === value) return i; }
        return -1;
    }
}


// cравнение массивов
function compareArr(arr1, arr2){
    if(arr1.length !== arr2.length) return false;
    var i = arr1.length;
    while(i--) if(arr1[i] !== arr2[i]) return false;
    return true;
};


//**********************************************************************
//*****   COPY  ********************************************************
//**********************************************************************
// не проверял
function copyObject(obj) {
    var ret = {};
    for (var key in obj) { ret[key] = obj[key]; }
    return ret;
}

// независимая копия массива, JSON
function copyArray(arr) { return JSON.parse(JSON.stringify(arr)); }


//**********************************************************************
//*****   AJAX  ********************************************************
//**********************************************************************
function ajaxAbort(ajax) {
    if (ajax) { ajax.abort(); ajax = undefined; }
    return ajax;
}


//**********************************************************************
//*****   TIMER  *******************************************************
//**********************************************************************
function timerAbort(timer) {
    if (timer) { clearTimeout(timer); timer = undefined; }
    return timer;
}



//**********************************************************************
//*****   ОТЛОЖЕННЫЙ ЗАПУСК ФУНКЦИИ  ***********************************
//**********************************************************************
// arg = 0 или 1 аргумент
function runDelay(timer, delay, fun, arg=undefined) {
    if (timer) { timer = timerAbort(timer); }
    if (delay == 0) { run(fun, arg); }
    else { timer = setTimeout(timerTick, delay, fun, arg); }

    function timerTick(fun, arg) {
        timer = timerAbort(timer);
        run(fun, arg);
    }

    function run(fun, arg) {
        if (arg === undefined) { fun(); }
        else { fun(arg); }
    }

    return timer;
}



//**********************************************************************
//*****   ПРОСТОЙ ХЭШ  *************************************************
//**********************************************************************
function hashSimple(str) {
    if (str.length % 32 >  0) str += Array(33 - str.length % 32).join("z");
    var hash = '', bytes = [], i = j = k = a =  0, dict = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','1','2','3','4','5','6','7','8','9'];
    for (i =  0; i < str.length; i++ ) {
        ch = str.charCodeAt(i);
        bytes[j++] = (ch < 127) ? ch & 0xFF : 127;
    }
    var chunk_len = Math.ceil(bytes.length / 32);
    for (i= 0; i<bytes.length; i++) {
        j += bytes[i];
        k++;
        if ((k == chunk_len) || (i == bytes.length-1)) {
            a = Math.floor( j / k );
            if (a < 32)
                hash += '0';
            else if (a > 126)
                hash += 'z';
            else
                hash += dict[ Math.floor( (a-32) / 2.76) ];
            j = k =  0;
        }
    }
    return hash;
}

//**********************************************************************
//*****   CSRF code   **************************************************
//**********************************************************************
var csrftoken = getCook('csrftoken');

// function getCookie(name) {
//     var cookieValue = null;
//     var i = 0;
//     if (document.cookie && document.cookie !== '') {
//         var cookies = document.cookie.split(';');
//         for (i; i < cookies.length; i++) {
//             var cookie = jQuery.trim(cookies[i]);
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});



//======================================================================
//=====   ОБЛАСТЬ DEFS  ================================================
//======================================================================
// function defsAdd(selParent) {
//     var svg;

//     function defsAddGradient(nam) {
//     var gradient;
//         gradient = svg.select("defs").append("linearGradient")
//             .attr("id", nam)
//             .attr("x2", "0%")
//             .attr("y2", "100%");
//         gradient.append("stop")
//             .attr("class", "start-color")
//             .attr("offset", "0%");
//         gradient.append("stop")
//             .attr("class", "end-color")
//             .attr("offset", "100%");
//     }

//     function defsAddShadow(nam, size) {
//         var shadow = svg.select("defs").append("filter")
//             .attr("id", nam)
//             .attr("height", "130%");
//         shadow.append("feGaussianBlur")
//             .attr("in", "SourceAlpha")
//             .attr("stdDeviation", 2)
//             .attr("result", "blur");
//         shadow.append("feOffset")
//             .attr("in", "blur")
//             .attr("dx", size)
//             .attr("dy", size)
//             .attr("result", "offsetBlur");
//         var feMerge = shadow.append("feMerge");
//         feMerge.append("feMergeNode")
//             .attr("in", "offsetBlur")
//         feMerge.append("feMergeNode")
//             .attr("in", "SourceGraphic");
//     }

//     svg = d3.select(selParent)
//         .append("svg")
//             .style("width", "0")
//             .style("height", "0");

//     svg.append("defs")
//         .attr('id', ID_DEFS_GLOBAL);

//     // .bar1 { fill: url(#gradientGreen); }
//     defsAddGradient("gradientGray");
//     defsAddGradient("gradientGrayLight");
//     defsAddGradient("gradientGreen");
//     defsAddGradient("gradientGreenLight");
//     defsAddGradient("gradientRed");
//     defsAddGradient("gradientRedLight");
//     defsAddGradient("gradientBlue");
//     defsAddGradient("gradientBlueLight");

//     // .style("filter", "url(#drop-shadow-2)")
//     defsAddShadow("drop-shadow-2", 2);
//     defsAddShadow("drop-shadow-3", 3);
// }



// сортировка данных
function datSort(dataset, ind) {
    var ret = dataset;
    switch(ind) {
        case 0: // текущий период
            ret.sort(function(a, b){
                var ret = b[2]-a[2];
                if (ret == 0) ret = a[0] > b[0]? 1 : -1;
                return ret;
            });
            break
        case 1: // предыдущий период
            ret.sort(function(a, b){
                var ret = b[1]-a[1];
                if (ret == 0) ret = a[0] > b[0]? 1 : -1;
                return ret;
            });
            break
        case 2: // рост, абс.
            ret.sort(function(a, b){
                var ret = (b[2]-b[1])-(a[2]-a[1]);
                if (ret == 0) ret = a[0] > b[0]? 1 : -1;
                return ret;
            });
            for(var i=0; i<ret.length; i++) {
                if (ret[i][2] <= ret[i][1]) {
                    ret = ret.slice(0, i);
                    break;
                }
            }
            break
        case 4: // снижение, абс.
            ret.sort(function(a, b){
                var ret = (a[2]-a[1])-(b[2]-b[1]);
                if (ret == 0) ret = a[0] > b[0]? 1 : -1;
                return ret;
            });
            for(var i=0; i<ret.length; i++) {
                if (ret[i][1] <= ret[i][2]) {
                    ret = ret.slice(0, i);
                    break;
                }
            }
            break
        case 3: // рост, %
            var val = [];
            // add %
            ret.forEach(function(d) { val.push([d[0], d[1], d[2], ((d[1] > 0) ? (d[2] * 100 / d[1]) : (999999999+d[2]))]); });
            // sort val
            val.sort(function(a, b){
                var ret = (b[3]-a[3]);
                if (ret == 0) ret = a[0] > b[0]? 1 : -1;
                return ret;
            });
            // cut val
            for(var i=0; i<val.length; i++) {
                if (val[i][2] <= val[i][1]) {
                    val = val.slice(0, i);
                    break;
                }
            }
            // copy val to ret without d[3]
            ret = [];
            val.forEach(function(d) { ret.push([d[0], d[1], d[2]]); });

            break
        case 5: // снижение, %
            var val = [];
            // add %
            ret.forEach(function(d) { val.push([d[0], d[1], d[2], ((d[1] > 0) ? (d[2] * 100 / d[1]) : 999999999)]); });
            // sort val
            val.sort(function(a, b){
                var ret = (a[3]-b[3]);
                if (ret == 0) ret = a[0] > b[0]? 1 : -1;
                return ret;
            });
            // cut val
            for(var i=0; i<val.length; i++) {
                if (val[i][1] <= val[i][2]) {
                    val = val.slice(0, i);
                    break;
                }
            }
            // copy val to ret without d[3]
            ret = [];
            val.forEach(function(d) { ret.push([d[0], d[1], d[2]]); });

            break
    }
    return ret;
}






//**********************************************************************
//*****   HTML   *******************************************************
//**********************************************************************
function HTMLCopy(htmlElement, callcackSVGModify) {
    var range = document.createRange();
    range.selectNode(htmlElement);
    window.getSelection().addRange(range);

    try {
        var successful = document.execCommand('copy');
        var msg = successful ? 'successful' : 'unsuccessful';
        console.log('Copy email command was ' + msg);
    } catch(err) {
        console.log('Oops, unable to copy');
    }
    // Снятие выделения - ВНИМАНИЕ: вы должны использовать
    // removeRange(range) когда это возможно
    window.getSelection().removeAllRanges();

/*
  var range = document.createRange();
  range.selectNode(DOM.JS_rel);
  window.getSelection().addRange(range);

  try {
    var successful = document.execCommand('copy');
    var msg = successful ? 'successful' : 'unsuccessful';
    console.log('Copy email command was ' + msg);
  } catch(err) {
    console.log('Oops, unable to copy');
  }
    // Снятие выделения - ВНИМАНИЕ: вы должны использовать
  // removeRange(range) когда это возможно
  window.getSelection().removeAllRanges();  }
var nodeMenuData, nodeMenuOpen;


*/
}




//**********************************************************************
//*****   ПОДЗАГРУЗКА HTML  ********************************************
//**********************************************************************
/*
function loadHTML(sURL, selElement) {
    var ret = "";
    var http = createRequestObject();
    if (http) {
        http.open('get', sURL);
        http.onreadystatechange = function () {
            if (http.readyState == 4) { $(selElement).html(http.responseText);  }
        }
        http.send(null);
    }
}

// ajax объект
function createRequestObject() {
    try { return new XMLHttpRequest() }
    catch(e) {
        try { return new ActiveXObject('Msxml2.XMLHTTP') }
        catch(e) {
            try { return new ActiveXObject('Microsoft.XMLHTTP') }
            catch(e) { return null; }
        }
    }
}

//**********************************************************************
//*****   URL.SEARCH  **************************************************
//**********************************************************************
function urlSearchToArr() {
    var ret = {}, param;
    if (location.search) {
        var pair = decodeURIComponent(location.search.substr(1)).split('&');
        for(var i = 0; i < pair.length; i ++) {
            param = pair[i].split('=');
            ret[param[0]] = param[1];
        }
    }
    return ret;
}

function urlArrToSearch(arr) {
    var ret = '';
    for(key in arr) ret = '&'+key+'='+arr[key];
    if (ret != '')  ret = '/search?' + encodeURIComponent(ret.substr(1));
    return ret;
}


*/


