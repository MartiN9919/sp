
class FORM_OBJ_FIND {
constructor(options) {
    this.parent    = options.parent;

    this.DOM          = {};
    this.DOM.parent   = d3.select(this.parent);
    this.DOM.title    = this.DOM.parent.append('p').attr('class', 'mTitle select_off').html('<i class="fa fa-arrow fa-md"></i>Совпадения');
}

free = function() {
    //window.removeEventListener('resize', this.resize, false);
    this.DOM = undefined;
}

}