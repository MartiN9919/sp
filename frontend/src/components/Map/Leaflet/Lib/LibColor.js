
// ЛОГАРИФМИЧЕСКАЯ ШКАЛА ДЛЯ data
export function scale_log(data) {
    const data_log = [
       -100000000000, -200000000000, -500000000000,
       -10000000000,  -20000000000,  -50000000000,
       -1000000000,   -2000000000,   -5000000000,
       -100000000,    -200000000,    -500000000,
       -10000000,     -20000000,     -50000000,
       -1000000,      -2000000,      -5000000,
       -100000,       -200000,       -500000,
       -10000,        -20000,        -50000,
       -1000,         -2000,         -5000,
       -100,          -200,          -500,
       -10,           -20,           -50,
       -1,            -2,            -5,
       -0.1,          -0.2,          -0.5,
       -0.01,         -0.02,         -0.05,
       -0.001,        -0.002,        -0.005,
       -0.0001,       -0.0002,       -0.0005,
       -0.00001,      -0.00002,      -0.00005,
       -0.000001,     -0.000002,     -0.000005,
       -0.0000001,    -0.0000002,    -0.0000005,
        0,
        0.0000001,     0.0000002,     0.0000005,
        0.000001,      0.000002,      0.000005,
        0.00001,       0.00002,       0.00005,
        0.0001,        0.0002,        0.0005,
        0.001,         0.002,         0.005,
        0.01,          0.02,          0.05,
        0.1,           0.2,           0.5,
        1,             2,             5,
        10,            20,            50,
        100,           200,           500,
        1000,          2000,          5000,
        10000,         20000,         50000,
        100000,        200000,        500000,
        1000000,       2000000,       5000000,
        10000000,      20000000,      50000000,
        100000000,     200000000,     500000000,
        1000000000,    2000000000,    5000000000,
        10000000000,   20000000000,   50000000000,
        100000000000,  200000000000,  500000000000,
        1000000000000, 2000000000000, 5000000000000,
    ];
    let val_min     = Math.min(... data);
    let val_max     = Math.max(... data);
    let val_min_log = Math.max(... data_log.filter(v => v <= val_min));
    let val_max_log = Math.min(... data_log.filter(v => v >  val_max));
    if (!isFinite(val_min_log)) val_min_log = data_log[0];
    if (!isFinite(val_max_log)) val_max_log = data_log[data_log.length-1];
    let ind_min_log = data_log.indexOf(val_min_log);
    let ind_max_log = data_log.indexOf(val_max_log);
    let scale       = data_log.slice(ind_min_log, ind_max_log);   // ind_max_log+1
    for (let i=scale.length-2; i>=0; i--) {
        if (data.filter(v => ((v>=scale[i])&&(v<scale[i+1]))).length==0) { scale.splice(i, 1); }
    }
    return scale;
}

// массив промежуточных цветов из len элементов, включая начальный и конечный цвета
// color_array('FF9900', '66FF33', 4);
export function color_array(color_begin, color_end, len) {
    let ret = [color_begin];
    for (let i=1; i<=len-2; i++) {
        ret.push(color_mid(color_begin, color_end, 1.0*i/(len-1)));
    }
    ret.push(color_end);
    return ret;
}
function color_mid(color_begin, color_end, k) {
    function color_mid_dig(color_begin, color_end, k) { return ('0'+Math.round(parseInt(color_begin,16)*(1-k)+parseInt(color_end,16)*k).toString(16)).slice(-2); }
    let ret = '';
    for (let i=0; i<3; i++) { ret += color_mid_dig(color_begin.substr(i*2,2), color_end.substr(i*2,2), k); }
    return ret;
}
