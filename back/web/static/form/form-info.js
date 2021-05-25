'use strict';

// КЛАСС: ФОРМА - ИНФОРМАЦИЯ
class FORM_INFO {

// создаваемый DOM-элемент: #obj_name
constructor(obj_name='form-info') {
    this.obj_name  = obj_name;
    this.id_window = this.html_id('');

    this.html_set();
    $('#'+this.id_window).window({
        title:       '&nbsp;<i class="fa fa-info-circle fa-md"></i>&nbsp;&nbsp;Справка',
        modal:       false,
        maximizable: false,
        minimizable: false,
        collapsible: false,
        left:        0,
        width:       300,
        top:         35,
        height:      window.innerHeight-35,
        minWidth:    200,
        minHeight:   300,
        //cls:         'select_off',
        onClose:     function(){ this.html_clear(); }.bind(this),
    });
    this.jq_window = $('#'+this.id_window);
    this.jq_window.css('overflow', 'auto').html(`
        <ul style="list-style:disc;list-style-position:inside;">
            <li>
                <strong>Горячие клавиши</strong><br>
                Добавить значение Ctrl+Shift+1
                Добавить файл Ctrl+Shift+2
                Добавить документ Ctrl+Shift+3
                Добавить точку Ctrl+Shift+4
                Добавить геометрию Ctrl+Shift+5
                Добавить физлицо Ctrl+Shift+6
                Добавить юрлицо Ctrl+Shift+7
                Добавить дело Ctrl+Shift+8
                Добавить транспорт Ctrl+Shift+9
                Справка Ctrl+F1<br>
                Ctrl+K - сохранить<br>
                Ctrl+K - сохранить<br>
                Ctrl+K - сохранить<br>
            </li>
            <li>
                <strong>Горячие клавиши2</strong><br>
                Ctrl+K - сохранить<br>
                Ctrl+K - сохранить<br>
                Ctrl+K - сохранить<br>
                Ctrl+K - сохранить<br>
                Ctrl+K - сохранить<br>
            </li>
        </ul>
        <b>sdf</b><br> vsdf bs df  sd fb sd fb sd fb sd f bs df b sdsdf vsdf bs df  sd fb sd fb sd fb sd f bs df b sdsdf vsdf bs df  sd fb sd fb sd fb sd f bs df b sdsdf vsdf bs df  sd fb sd fb sd fb sd f bs df b sdsdf vsdf bs df  sd fb sd fb sd fb sd f bs df b sdsdf vsdf bs df  sd fb sd fb sd fb sd f bs df b sdsdf vsdf bs df  sd fb sd fb sd fb sd f bs df b sdsdf vsdf bs df  sd fb sd fb sd fb sd f bs df b sdsdf vsdf bs df  sd fb sd fb sd fb sd f bs df b sd
    `);
}


html_id(id=''){ return this.obj_name+((id!='')?('_'+id):''); }
html_set(){
    this.html_clear();
    $('body').append('<section id="'+this.id_window+'" style="padding:5px;"></section>');
}
html_clear(){
    if (this.jq_window) {
        this.jq_window.parent().remove();
        $('.window-shadow').remove();
        $('.window-mask').remove();
    }
};

}
