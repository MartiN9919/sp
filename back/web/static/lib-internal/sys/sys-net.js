

/**
 *  AJAX на чистом JS
*/
function net_ajax(options) {
    var
    url     = options.url,          // адрес отправки
    data    = options.data || '',   // отправляемые данные
    success = options.success,      // callback ok
    error   = options.error;        // callback error
    const Request = new XMLHttpRequest();
    Request.onreadystatechange = function() {
        if (Request.readyState != 4) return
        if (Request.status     == 200) { success(JSON.parse(unescape(Request.responseText))); }
        else                           { if (error) error(undefined); }
    }
    Request.open('POST', url, true);
    Request.setRequestHeader('Content-Type','application/json; charset=utf-8');
    Request.setRequestHeader('X-CSRFToken', getCook('csrftoken'));
    Request.setRequestHeader('X-Requested-With', 'XMLHttpRequest');     // признак ajax-запроса
    Request.send(JSON.stringify(data));
}
