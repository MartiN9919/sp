'use strict';



//**********************************************************************
//*****   SVG   ********************************************************
//**********************************************************************
function svg_copy(svg_js, cb_svg_modify) {
    svg_2_canvas(svg_js, 'jpeg', cb_svg_modify, function(data, canvas) {
        canvas.toBlob(function(blob) {
            // work only localhost or https or Insecure origins treated as secure
            if (navigator.clipboard) {
                const item = new ClipboardItem({ "image/png": blob });
                navigator.clipboard.write([item]).catch(err => { alert('Объект не скопирован в буфер обмена'); });
            } else {
                // alert('Для включения возможности копирования\n'+
                //     '1. в окне браузера наберите: chrome://flags\n'+
                //     '2. включите опцию: Insecure origins treated as secure\n'+
                //     '3. в поле под опцией укажите: '+window.location.protocol+'//'+window.location.host
                // );
                // return;

                // let dx   = svg_js.scrollWidth,
                //     dy   = svg_js.scrollHeight;
                // let dx0  = Math.min(dx, 800); if (dx0 < dx) { dy*=(dx0/dx); dx=dx0; }
                // let dy0  = Math.min(dy, 600); if (dy0 < dy) { dx*=(dy0/dy); dy=dy0; }
                // let body = document.querySelector('body');
                // let x    = (body.scrollWidth-dx)/2,
                //     y    = (body.scrollHeight-dy)/2-20;

                // // вариант 1: в windows не работает
                // // window.open(data, String(tsNowUTC()), 'left='+x+', top='+y+', width='+dx+', height='+dy);  // '_blank'

                // // вариант 2
                // // let w = window.open('', String(tsNowUTC()), 'left='+x+', top='+y+', width='+(dx+25)+', height='+(dy+25));  // '_blank'
                // // w.document.write(canvas.outerHTML);
                // // let newCanvas = w.document.querySelector('canvas:first-of-type');
                // // newCanvas.style.display = null;
                // // let newCtx = newCanvas.getContext('2d');
                // // newCtx.drawImage(canvas, 0,0);

                // // вариант 3
                // let w   = window.open('', String(tsNowUTC()), 'left='+x+', top='+y+', width='+(dx+25)+', height='+(dy+25));  // '_blank'
                // if (!w) { alert('Ошибка отображения всплывающего окна. Включите в браузере данную опцию.'); return; }

                // let img = w.document.createElement('img');
                // img.style.width  = dx;
                // img.style.height = dy;
                // img.src          = data; //canvas.toDataURL("image/jpg");
                // w.document.body.appendChild(img);
            };


        });


    });
}

function svg_save(svg_js, cb_svg_modify) {
    svg_2_canvas(svg_js, 'png', cb_svg_modify, function(data) {
        // вариант 1: для Chrome - новых браузеров
        data_save_as('Без названия.png', data.replace('image/png', 'image/octet-stream'));
        // вариант 2: универсальный, но без имени по умолчанию
        // document.location.href = data.replace('image/png', 'image/octet-stream');
    });
}

function svg_print(svg_js, cb_svg_modify) {
    // вариант 1 - через CANVAS
    svg_2_canvas(svg_js, 'jpeg', cb_svg_modify, function(data, canvas) {
        let dx   = svg_js.scrollWidth,
            dy   = svg_js.scrollHeight;
        let dx0  = Math.min(dx, 800); if (dx0 < dx) { dy*=(dx0/dx); dx=dx0; }
        let dy0  = Math.min(dy, 600); if (dy0 < dy) { dx*=(dy0/dy); dy=dy0; }
        let body = document.querySelector('body');
        let x    = (body.scrollWidth-dx)/2,
            y    = (body.scrollHeight-dy)/2-20;

        let w    = window.open('', String(tsNowUTC()), 'left='+x+', top='+y+', width='+(dx+25)+', height='+(dy+25));
        if (!w) { alert('Ошибка отображения всплывающего окна. Включите в браузере данную опцию.'); return; }

        w.document.write(`
            <html>
            <body onload="window.print();window.close();">
            <style>@page { size: auto; margin: 0mm; }</style>
            <img src="${data}" style="width: ${dx}px; height: ${dy}px;">
            </body>
            </html>
        `);
        w.document.close();
    });
    // вариант 2 - через SVG - проблемы с центрированием
    // let parent = svg_js.closest('div');
    // w.document.writeln('<style>@page { margin: 0mm; }</style><html><body onload="window.print()">'+parent.innerHTML+'</body></html>');
}


// svg_js = document.querySelector('#svg0')
// format = ['png', 'jpeg', 'octet-stream', 'svg+xml']
function svg_2_canvas(svg_js, format, cb_svg_modify, cb_image_load) {
    // получить svgURL
    style_save(svg_js.childNodes);                                                                      // сохранить стили SVG
    style_full(svg_js.childNodes);                                                                      // явно установить все стили
    if (cb_svg_modify) cb_svg_modify(svg_js);                                                           // изменить стили SVG для устранения возможных багов при конвертации SVG --> CANVAS
    var svgURL = new XMLSerializer().serializeToString(svg_js);                                         // SVG to svgURL
    style_restore(svg_js.childNodes);                                                                   // восстановить стили SVG

    // создать скрытый canvas
    var canvas    = document.createElement('canvas');
    canvas.width  = svg_js.scrollWidth;
    canvas.height = svg_js.scrollHeight;
    canvas.style.cssText+='display:none;';
    document.body.appendChild(canvas);

    // URL to Canvas
    var img = new Image();
    img.onload = function() {
        let context = canvas.getContext('2d');
        if (format == 'jpeg') {
            context.beginPath();
            context.rect(0, 0, canvas.width, canvas.height);
            context.fillStyle = '#fff';
            context.fill();
        }
        context.drawImage(this, 0,0);

        if (cb_image_load) cb_image_load(canvas.toDataURL('image/'+format, 1.0), canvas, img);          // callback
        document.body.removeChild(canvas);                                                              // удалить canvas
    }
    img.src = 'data:image/svg+xml; charset=utf8, '+encodeURIComponent(svgURL);                          // задание на фоновую загрузку svgURL в IMG
}



function data_save_as(file, data) {
    var link = document.createElement('a');
    link.href     = data;
    link.download = file;
    link.click();
}





//**********************************************************************
//*****   STYLE   ******************************************************
//**********************************************************************
// cохраняет стиль в .styleOld
function style_save(children) {
    for (let i = 0; i < children.length; i++) {
        let child = children[i];
        if (child instanceof Element) {
            child['styleOld'] = child.getAttribute('style');
            style_save(child.childNodes);
        }
    }
}

// восстанавлявает стиль из .styleOld
function style_restore(children) {
    for (let i = 0; i < children.length; i++) {
        let child = children[i];
        if (child instanceof Element) {
            let cssText = child['styleOld'];
            if (cssText !== undefined) {
                if (cssText !== null) { child.setAttribute('style', cssText); }
                else                  { child.removeAttribute('style');       }
            }
            delete child['styleOld'];
            style_restore(child.childNodes);
        }
    }
}

// явно устанавливает все стили
function style_full(children) {
    for (let i = 0; i < children.length; i++) {
        let child = children[i];
        if (child instanceof Element) {
            let cssText = '';
            let computedStyle = window.getComputedStyle(child, null);
            for (let i = 0; i < computedStyle.length; i++) {
                let prop = computedStyle[i];
                cssText += prop + ':' + computedStyle.getPropertyValue(prop) + ';';
            }
            child.styleOld = child.getAttribute('style');
            child.setAttribute('style', cssText);
            style_full(child.childNodes);
        }
    }
}
