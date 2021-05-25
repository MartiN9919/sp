// !!!!! НЕ ИНИЦИАЛИЗИРОВАТЬ !!!!!!
class FORM_TREE {
static DATA_VAL       = 'val';
static DATA_CHANGED   = 'changed';
static DATA_NEED      = 'need';
static DATA_OBJ_TOP   = 'obj_top';

static icons(data_item){
    let ret='';
    switch(data_item.type_val) {
        case 'str':      ret = 'fa fa-font fa-md';            break;
        case 'int':      ret = 'fa fa-sort-numeric-up fa-md'; break;
        case 'float':    ret = 'fa fa-ellipsis-h fa-md';      break;
        case 'bit':      ret = 'fa fa-check fa-md';           break;
        case 'data':     ret = 'fa fa-calendar-alt fa-md';    break;
        case 'datatime': ret = 'fa fa-clock fa-md';           break;
        case 'geometry': ret = 'fa fa-draw-polygon fa-md';    break;
        case 'point':    ret = 'fa fa-map-marker-alt fa-md';  break;
        default:         ret = 'fa fa-pen-alt fa-md';
    }
    return ret;
}

// аттрибуты-классы узла в строку
static attributes(data_item) {
    let ret = [];
    if (data_item[this.DATA_CHANGED ]===true) ret.push('attr_changed');
    if (data_item[this.DATA_NEED    ]===true) ret.push('attr_need');
    if (data_item[this.DATA_OBJ_TOP ]===true) ret.push('attr_obj_top'); else ret.push('attr_obj_dop');
    ret = (ret.length>0) ? { class: ret.join(' ') } : undefined;
    return ret;
}

// data_obj_keys += parent, val, changed
static data_tree(data_obj_keys) {
    let ret = [];
    for(let data_item of data_obj_keys) {
        data_item[this.DATA_VAL    ] = undefined;
        data_item[this.DATA_CHANGED] = false;

        let title_lst = data_item.title.split('/')
        let parent_id = '';
        for(let title_item of title_lst.slice(0,-1)) {
            let id = parent_id+'_'+title_item;
            if (!(ret.find(function(element){ return (element.id==id) }))) {
                ret.push({
                    id:     id,
                    parent: (parent_id=='')?'#':parent_id,
                    icon:   'fa fa-folder fa-md',
                    text:   title_item,
                    a_attr: { class: 'jstree-title', },
                    state:  { opened: true, },
                });
            }
            parent_id = id;
        };
        ret.push({
            id:     data_item.id,
            parent: (parent_id=='')?'#':parent_id,
            icon:   this.icons(data_item),
            text:   title_lst.slice(-1),
            a_attr: this.attributes(data_item),
        });
    };
    return ret;
}

// del tree.parent_id
// add tree.children: [{...},]
static tree_add_child(data_full, parent_id) {
        let data_child = [];
        for (let data_item of data_full) {
            if (data_item['parent_id'] != parent_id) continue;
            let tmp = Object.assign({}, data_item);             // неглубокая копия
            delete tmp['parent_id'];
            tmp['children'] = this.tree_add_child(data_full, data_item['id']);
            data_child.push(tmp);
            // data_child.push({
            //     a_attr:   data_item['a_attr'],
            //     id:       data_item['id'],
            //     text:     data_item['text'],
            //     icon:     data_item['icon'],
            //     state:    data_item['state'],
            //     children: data_tree(data_item['id']),
            // });
        }
        return data_child;
    };



}

