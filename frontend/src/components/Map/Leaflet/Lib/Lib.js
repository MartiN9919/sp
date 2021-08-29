
// word - обрезать по границе слов
export function str_cut(str, len, word=false) {
  if (!str) return str;
  let str_orig = str.trim();
  let str_ret  = str_orig.slice(0, len);
  let str_end  = '';
  if (str_ret.length < str_orig.length) { str_end = '...'; }

  if ((word) && (str_end != '')) {
    let last_space = str_ret.lastIndexOf(' ');
    if (last_space > 0) { str_ret = str_ret.substr(0, last_space); str_end = '...'; }
  }

  return str_ret + str_end;
}
