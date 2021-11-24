// COMMON
function dig2(val){ return ("0"+val).slice(-2); }

// COOKIES
export function cook_set(name, value, max_age=3600*24*30*12*30) {   // 30 лет
  document.cookie = encodeURIComponent(name)+"="+encodeURIComponent(value)+"; path=/; max-age="+max_age;
}
export function cook_get_str(name, valueEmpty) {
  let matches = document.cookie.match(new RegExp("(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"));
  return matches ? decodeURIComponent(matches[1]) : valueEmpty;
}
export function cook_get_int (name, valueEmpty) { return parseInt(cook_get_str(name, valueEmpty))  }
export function cook_get_bool(name, valueEmpty) { return (cook_get_str(name, valueEmpty)==='true') }



// DATE-TIME
// текущее смещение времени относительно нулевого меридиана
export var myUTC = new Date().getTimezoneOffset()*60*1000;

// дата/время строкой в timestamp с UTC
export function datesql_to_ts(datestr) { return (datestr!='')?(Date.parse(datestr+'Z')+myUTC):0; }

// timestamp в sql-формат с UTC: "2021-01-01 09:00"
export function ts_to_datesql(ts, isTime = true) {
  let d    = new Date(ts);
  let yyyy = d.getFullYear();
  let mm   = dig2(d.getMonth() + 1);
  let dd   = dig2(d.getDate());
  let ret  = yyyy+'-'+mm+'-'+dd;
  if (isTime) {
    var hh  = dig2(d.getHours());
    var min = dig2(d.getMinutes());
    ret    += ' '+hh+':'+min;
  }
  return ret;
}

// timestamp в отображаемый на экране вид с UTC: "01.01.2021 9:00"
export function ts_to_screen(ts, isDate = true, isTime = true) {
  let ret  = '';
  let d    = new Date(ts);
  if (isDate == true) {
    let yyyy = d.getFullYear();
    let mm   = dig2(d.getMonth() + 1);
    let dd   = dig2(d.getDate());
    ret      = dd+'.'+mm+'.'+yyyy;
  }
  if (isTime == true) {
    let hh  = d.getHours();
    let min = dig2(d.getMinutes());
    ret    += ' '+hh+':'+min;
  }
  return ret.trim();
}


// timestamp сейчас с UTC
// export function ts_now() { return Math.floor(new Date().getTime()/1000); }

// // timestamp с UTC в дата/время строкой
// export function ts_to_datestr(ts) {
//   // return new Date().setTime(ts*1000);
//   let ret = new Date();
//   ret.setTime(ts);   // ts*1000
//   return ret;
// }




// простой хэш
// function hashSimple(str) {
//   if (str.length % 32 >  0) str += Array(33 - str.length % 32).join("z");
//   var hash = '', bytes = [], i = j = k = a =  0, dict = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','1','2','3','4','5','6','7','8','9'];
//   for (i =  0; i < str.length; i++ ) {
//     ch = str.charCodeAt(i);
//     bytes[j++] = (ch < 127) ? ch & 0xFF : 127;
//   }
//   var chunk_len = Math.ceil(bytes.length / 32);
//   for (i= 0; i<bytes.length; i++) {
//     j += bytes[i];
//     k++;
//     if ((k == chunk_len) || (i == bytes.length-1)) {
//       a = Math.floor( j / k );
//       if (a < 32)
//         hash += '0';
//       else if (a > 126)
//         hash += 'z';
//       else
//         hash += dict[ Math.floor( (a-32) / 2.76) ];
//       j = k =  0;
//     }
//   }
//   return hash;
// }
