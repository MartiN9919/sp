
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

export function str_copy_deep(str) {
  return (str) ? (' '+str).slice(1) : str;
}


// РАБОТАЕТ, ПОКА НЕ НУЖНО
// export function dict_set(dict, chain, val) {
//   let dict_item = dict;
//   for (let ind=0; ind<chain.length-1; ind++) {
//     if (dict_item[chain[ind]]==undefined) dict_item[chain[ind]] = {};
//     dict_item = dict_item[chain[ind]];
//   }
//   dict_item[chain[chain.length-1]] = val;
//   return dict;
// }

// export function dict_get(dict, chain, val_default) {
//   let dict_item = dict;
//   for (let ind=0; ind<chain.length-1; ind++) {
//     dict_item = dict_item[chain[ind]] ?? {};
//   }
//   return dict_item[chain[chain.length-1]] ?? val_default;
// }
