# ПАРСИНГ RSS+Site

## ВАЖНО
* сначала выкачивается RSS, потом данные дополняются/заменяются выкачанными непосредственно с сайта

## ПРИМЕР

```py
[
  {
    "field":        "content",                                                          ## заполняемое поле
    "warning":      false,                                                              ## предупреждение в лог о пустом поле
    "DOM_del":      "#article_body > div",                                              ## DOM-блоки для удаления
    "DOM_del":      ["#article_body > div", "#article_body > blockquote"],              ## DOM-блоки для удаления
    "text":         "#article_body",                                                    ## получить текст
    "text":         [["#article_body", "..."]],                                         ## получить текст
    "text_replace": ["\n", " "],                                                        ## текст для замены
    "text_replace": [["\n", " "]],                                                      ## текст для замены
    "text_del":     "-0-",                                                              ## текст для удаления
    "text_del":     ["-0-", "Все материалы конференции можно прочитать по ссылке"]      ## текст для удаления
  },

  {
    "field":   "repost",
    "operation": "sum",                                                                 ## тип операции
    "text": [
        ["div[data-role=\"share-block\"][data-view=\"desktop-bottom\"]", "odnoklassniki:(\\d+)"],   ## отбор по регулярным выражением
        ["div[data-role=\"share-block\"][data-view=\"desktop-bottom\"]", "vkontakte:(\\d+)"],
    ]
  }
]


или

{   "except":   "nina.nn.by",                                                           ## маски (в т.ч. регулярки) исключаемых из обработки url, проверка до и после выкачки
    "except":   ["nina.nn.by", "blog.tam.by", "http://zautra.by$"],                     ## маски (в т.ч. регулярки) исключаемых из обработки url, проверка до и после выкачки
    "decode":   true,                                                                   ## при загрузке в парсер вместо content использовать text
    "parse":    [ сокращенная форма ... ]
}
```
