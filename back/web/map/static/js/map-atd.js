const atd = [
// [0] id_parent               [1] id                                        [2] id_name                        [3] title
['atd',                        'atd.by',                                     'Беларусь',                        'Беларусь'],

['atd.by',                     'atd.by.o_brest',                             'Брестская область',               'Брестская область'],
['atd.by.o_brest',             'atd.by.o_brest.g_brest',                     'Брест',                           'Брест'],
['atd.by.o_brest',             'atd.by.o_brest.r_brest',                     'Брестский район',                 'Брестский район'],
['atd.by.o_brest',             'atd.by.o_brest.r_baran',                     'Барановичский район',             'Барановичский район'],
['atd.by.o_brest',             'atd.by.o_brest.r_gabin',                     'Жабинковский район',              'Жабинковский район'],
['atd.by.o_brest',             'atd.by.o_brest.r_kamenetc',                  'Каменецкий район',                'Каменецкий район'],
['atd.by.o_brest',             'atd.by.o_brest.r_kobrin',                    'Кобринский район',                'Кобринский район'],
['atd.by.o_brest',             'atd.by.o_brest.r_malorita',                  'Малоритский район',               'Малоритский район'],

['atd.by',                     'atd.by.o_vitebsk',                           'Витебская область',               'Витебская область'],
['atd.by.o_vitebsk',           'atd.by.o_vitebsk.g_vitebsk',                 'Витебск',                         'Витебск'],
['atd.by.o_vitebsk',           'atd.by.o_vitebsk.r_vitebsk',                 'Витебский район',                 'Витебский район'],
['atd.by.o_vitebsk',           'atd.by.o_vitebsk.r_beshenk',                 'Бешенковичский район',            'Бешенковичский район'],
['atd.by.o_vitebsk',           'atd.by.o_vitebsk.r_braslav',                 'Браславский район',               'Браславский район'],
['atd.by.o_vitebsk',           'atd.by.o_vitebsk.r_vdvinsk',                 'Верхнедвинский район',            'Верхнедвинский район'],
['atd.by.o_vitebsk',           'atd.by.o_vitebsk.r_glubokoe',                'Глубокский район',                'Глубокский район'],
['atd.by.o_vitebsk',           'atd.by.o_vitebsk.r_gorodok',                 'Городокский район',               'Городокский район'],
['atd.by.o_vitebsk',           'atd.by.o_vitebsk.r_dokshitc',                'Докшицкий район',                 'Докшицкий район'],
['atd.by.o_vitebsk',           'atd.by.o_vitebsk.r_dubrovno',                'Дубровенский район',              'Дубровенский район'],
['atd.by.o_vitebsk',           'atd.by.o_vitebsk.r_lepel',                   'Лепельский район',                'Лепельский район'],
['atd.by.o_vitebsk',           'atd.by.o_vitebsk.r_liozno',                  'Лиозненский район',               'Лиозненский район'],
//['atd.by.o_vitebsk',         'atd.by.o_vitebsk.r_miory',                   'Миорский район',                  'Миорский район'],
['atd.by.o_vitebsk',           'atd.by.o_vitebsk.g_npolotsk',                'Новополоцк',                      'Новополоцк'],
['atd.by.o_vitebsk',           'atd.by.o_vitebsk.r_orsha',                   'Оршанский район',                 'Оршанский район'],
['atd.by.o_vitebsk',           'atd.by.o_vitebsk.g_polotsk',                 'Полоцк',                          'Полоцк'],
['atd.by.o_vitebsk',           'atd.by.o_vitebsk.r_polotsk',                 'Полоцкий район',                  'Полоцкий район'],
['atd.by.o_vitebsk',           'atd.by.o_vitebsk.r_postawy',                 'Поставский район',                'Поставский район'],
['atd.by.o_vitebsk.r_postawy', 'atd.by.o_vitebsk.r_postawy.g_postawy',       'Поставы',                         'Поставы'],
['atd.by.o_vitebsk.r_postawy', 'atd.by.o_vitebsk.r_postawy.s_volki',         'Волковский сельский Совет',       'Волковский сельсовет'],
['atd.by.o_vitebsk.r_postawy', 'atd.by.o_vitebsk.r_postawy.s_voropaevo',     'Воропаевский сельский Совет',     'Воропаевский сельсовет'],
['atd.by.o_vitebsk.r_postawy', 'atd.by.o_vitebsk.r_postawy.s_dunilovichi',   'Дуниловичский сельский Совет',    'Дуниловичский сельсовет'],
['atd.by.o_vitebsk.r_postawy', 'atd.by.o_vitebsk.r_postawy.s_kamai',         'Камайский сельский Совет',        'Камайский сельсовет'],
//['atd.by.o_vitebsk.r_postawy', 'atd.by.o_vitebsk.r_postawy.s_kozlov',        'Козловщинский сельский Совет',    'Козловщинский сельсовет'],
['atd.by.o_vitebsk.r_postawy', 'atd.by.o_vitebsk.r_postawy.s_kuropol',       'Куропольский сельский Совет',     'Куропольский сельсовет'],
['atd.by.o_vitebsk.r_postawy', 'atd.by.o_vitebsk.r_postawy.p_lyntupy',       'Лынтупы',                         'Лынтупы'],
['atd.by.o_vitebsk.r_postawy', 'atd.by.o_vitebsk.r_postawy.s_lyntupy',       'Лынтупский сельский Совет',       'Лынтупский сельсовет'],
['atd.by.o_vitebsk.r_postawy', 'atd.by.o_vitebsk.r_postawy.s_novoselki',     'Новосёлковский сельский Совет',   'Новоселковский сельсовет'],
['atd.by.o_vitebsk.r_postawy', 'atd.by.o_vitebsk.r_postawy.s_yunki',         'Юньковский сельский Совет',       'Юньковский сельсовет'],
['atd.by.o_vitebsk.r_postawy', 'atd.by.o_vitebsk.r_postawy.s_yarevo',        'Яревский сельский Совет',         'Яревский сельсовет'],
['atd.by.o_vitebsk',           'atd.by.o_vitebsk.r_rossony',                 'Россонский район',                'Россонский район'],
['atd.by.o_vitebsk',           'atd.by.o_vitebsk.r_senno',                   'Сенненский район',                'Сенненский район'],
['atd.by.o_vitebsk',           'atd.by.o_vitebsk.r_tolochin',                'Толочинский район',               'Толочинский район'],
['atd.by.o_vitebsk',           'atd.by.o_vitebsk.r_ushachi',                 'Ушачский район',                  'Ушачский район'],
['atd.by.o_vitebsk',           'atd.by.o_vitebsk.r_chashniki',               'Чашникский район',                'Чашникский район'],
['atd.by.o_vitebsk',           'atd.by.o_vitebsk.r_sharkov',                 'Шарковщинский район',             'Шарковщинский район'],
['atd.by.o_vitebsk',           'atd.by.o_vitebsk.r_shumilin',                'Шумилинский район',               'Шумилинский район'],

['atd.by',                     'atd.by.o_gomel',                             'Гомельская область',              'Гомельская область'],
['atd.by',                     'atd.by.o_grodmo',                            'Гродненская область',             'Гродненская область'],
['atd.by',                     'atd.by.o_minsk',                             'Минская область',                 'Минская область'],
['atd.by',                     'atd.by.o_mogilev',                           'Могилёвская область',             'Могилевская область'],
['atd.by',                     'atd.by.g_minsk',                             'Минск',                           'Минск'],

['atd',                        'atd.lt',                                     'Республика Литва',                'Литва'],
['atd',                        'atd.lv',                                     'Республика Латвия',               'Латвия'],
['atd',                        'atd.pl',                                     'Республика Польша',               'Польша'],
['atd',                        'atd.ua',                                     'Украина',                         'Украина'],
['atd',                        'atd.ru',                                     'Российская Федерация',            'Россия'],
];
