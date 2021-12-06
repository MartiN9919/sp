// COMMON
function dig2(val){ return ("0"+val).slice(-2); }

// DATE-TIME
// текущее смещение времени относительно нулевого меридиана
export var myUTC = new Date().getTimezoneOffset()*60*1000;

// дата/время строкой в timestamp с UTC
export function datesql_to_ts(datestr) { return (datestr!='')?(Date.parse(datestr+'Z')+myUTC):0; }

// дата/время признак - только дата без времени: "2021-01-01"
// некорректно когда "2021-01-01 00:00": ((((datesql_to_ts(datestr)/1000) % (60*60*24))|0) != 75600)
export function datesql_is_time(datestr) { return (datestr.length > 10) }


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
export function hash_simple(str, seed = 0) {
    let h1 = 0xdeadbeef ^ seed, h2 = 0x41c6ce57 ^ seed;
    for (let i = 0, ch; i < str.length; i++) {
        ch = str.charCodeAt(i);
        h1 = Math.imul(h1 ^ ch, 2654435761);
        h2 = Math.imul(h2 ^ ch, 1597334677);
    }
    h1 = Math.imul(h1 ^ (h1>>>16), 2246822507) ^ Math.imul(h2 ^ (h2>>>13), 3266489909);
    h2 = Math.imul(h2 ^ (h2>>>16), 2246822507) ^ Math.imul(h1 ^ (h1>>>13), 3266489909);
    return 4294967296 * (2097151 & h2) + (h1>>>0);
}
// этот хэш короче
// export function hash_simple(str) {
//   let hash = 0;
//   if (str.length == 0) return hash;
//   for (let i = 0; i < str.length; i++) {
//       const char = str.charCodeAt(i);
//       hash = ((hash<<5)-hash)+char;
//       hash &= hash; // Convert to 32bit integer
//   }
//   return hash;
// }



// // COOKIES
// export function cook_set(name, value, max_age=3600*24*30*12*30) {   // 30 лет
//   document.cookie = encodeURIComponent(name)+"="+encodeURIComponent(value)+"; path=/; max-age="+max_age;
// }
// export function cook_get_str(name, valueEmpty) {
//   let matches = document.cookie.match(new RegExp("(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"));
//   return matches ? decodeURIComponent(matches[1]) : valueEmpty;
// }
// export function cook_get_int (name, valueEmpty) { return parseInt(cook_get_str(name, valueEmpty))  }
// export function cook_get_bool(name, valueEmpty) { return (cook_get_str(name, String(valueEmpty)) === 'true') }
