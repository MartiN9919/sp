'use strict';

class Class_leaflet_edit {
#edit_redoBuffer;
constructor({
    map,                                    // ссылка на карту
    data,                                   // данные для редактирования: FeatureCollection или GeometryCollection
    cb_data_save,                           // переопределяемая callback-функция: сохранить данные
    marker_red,                             // отредактированный маркер
}) {
    var that          = this;
    this.map          = map;
    this.data         = data;
    this.cb_data_save = cb_data_save;
    this.marker_red   = marker_red;

    this.control      = [];

    /*
     *****************************
     * БЛОК ОСНОВНЫХ КНОПОК
     *****************************
     */
    var container_new = L.DomUtil.create('div', 'leaflet-control leaflet-bar');
    L.EditControl     = L.Control.extend({
        options: {
            position:   'topleft',
            callback:   null,
            title:      '',
            class_icon: '',
            html:       '',
        },

        onAdd: function(map) {
            let link       = L.DomUtil.create('a', this.options.class_icon, container_new);
            link.href      = '#';
            link.title     = this.options.title;
            link.innerHTML = this.options.html;
            L.DomEvent
                .on(link, 'click', L.DomEvent.stop)
                .on(link, 'click', function() {
                    window.LAYER = this.options.callback.call(that.map.editTools);
                }, this);
            return container_new;
        }
    });

    L.NewMarkerControl = L.EditControl.extend({
        options: {
            callback:   this.map.editTools.startMarker,
            title:      'Добавить маркер (Shift+M)',
            class_icon: 'fa fa-map-marker-alt fa-md',
        }
    });

    L.NewLineControl = L.EditControl.extend({
        options: {
            callback:   this.map.editTools.startPolyline,
            title:      'Добавить линию (Shift+L)',
            class_icon: 'fa fa-wave-square fa-md',
        }
    });

    L.NewPolygonControl = L.EditControl.extend({
        options: {
            callback:   this.map.editTools.startPolygon,
            title:      'Добавить полигон (Shift+P)',
            class_icon: 'fa fa-draw-polygon fa-md',
        }
    });

    this.control.new_marker  = new L.NewMarkerControl();
    this.control.new_line    = new L.NewLineControl();
    this.control.new_polygon = new L.NewPolygonControl();

    this.map.addControl(this.control.new_marker);
    this.map.addControl(this.control.new_line);
    this.map.addControl(this.control.new_polygon);

    L.DomEvent.addListener(document, 'keydown',    this.#onKeyDown,  this);
    this.map.on('layeradd',               this.#onLayerAdd, this);
    this.map.on('editable:editing',       function(e) { if (e.layer.setStyle)   e.layer.setStyle({color: 'DarkRed'}); }, this);
    this.map.on('editable:dragend',       function(e) { if (e.layer.setIcon)    e.layer.setIcon(this.marker_red);     }, this);
    this.map.on('editable:enable',        function(e) { if (e.layer.setOpacity) e.layer.setOpacity(0.5);              }, this);
    this.map.on('editable:disable',       function(e) { if (e.layer.setOpacity) e.layer.setOpacity(1);                }, this);
    this.map.on('editable:drawing:start', function(e) { if (e.layer.setIcon)    e.layer.setIcon(this.marker_red);     }, this);
    this.map.on('editable:drawing:end',   function(e) {
        this.redoBuffer = [];
        if ((e.layer._defaultShape) && (!e.layer._defaultShape().length)) { this.map.editTools.featuresLayer.removeLayer(e.layer); }
    }, this);
    this.map.on('editable:drawing:cancel',function(e) {
        delete this.map.editTools.featuresLayer._layers[e.layer._leaflet_id];
        if (e.layer.remove) e.layer.remove();
    }, this);


    /*
     *****************************
     * БЛОК ДОПОЛНИТЕЛЬНЫХ КНОПОК
     *****************************
     */
    var container_dop = L.DomUtil.create('div', 'leaflet-control leaflet-bar');
    L.Control.Dop = L.Control.extend({
        options: {
            position:   'topleft',
            callback:   null,
            title:      '',
            class_icon: '',
            html:       '',
        },
        onAdd: function(map) {
            let link       = L.DomUtil.create('a', this.options.class_icon, container_dop);
            link.href      = '#';
            link.title     = this.options.title;
            link.innerHTML = this.options.html;
            L.DomEvent
                .on(link, 'click', L.DomEvent.stop)
                .on(link, 'click', function () { this.options.callback.call(that); }, this);
            return container_dop;
        }
    });

    L.DopSave = L.Control.Dop.extend({
        options: {
            callback:   this.#onDopSave,
            title:      'Сохранить',
            class_icon: 'fa fa-save fa-md',
        }
    });

    L.DopCancel = L.Control.Dop.extend({
        options: {
            callback:   this.#onDopReset,
            title:      'Отменить все',
            class_icon: 'fa fa-undo fa-md',
        }
    });

    L.DopClear = L.Control.Dop.extend({
        options: {
            callback:   this.#onDopClear,
            title:      'Очистить все',
            class_icon: 'fa fa-eraser fa-md',
        }
    });

    this.control.dop_save   = new L.DopSave();
    this.control.dop_cancel = new L.DopCancel();
    this.control.dop_clear  = new L.DopClear();

    this.map.addControl(this.control.dop_save);
    this.map.addControl(this.control.dop_cancel);
    this.map.addControl(this.control.dop_clear);


    // РАЗМЕЩАТЬ ДАННЫЕ ПОСЛЕ ИНИЦИАЛИЗАЦИИ ОБРАБОТЧИКОВ
    this.#layer_set();

    // ДЛЯ UNDO
    this.#edit_redoBuffer = [];
}


free() {
    L.DomEvent.removeListener(document, 'keydown', this.#onKeyDown);

    this.map.removeControl(this.control.new_marker);
    this.map.removeControl(this.control.new_line);
    this.map.removeControl(this.control.new_polygon);
    this.map.removeControl(this.control.dop_save);
    this.map.removeControl(this.control.dop_cancel);
    this.map.removeControl(this.control.dop_clear);

    this.map.off('editable:disable');
    this.map.off('editable:enable');
    this.map.off('editable:dragend');
    this.map.off('editable:drawing:end');
    this.map.off('editable:drawing:start');
    this.map.off('editable:editing');
    this.map.off('layeradd');

    // delete this.control.new_marker;
    // delete this.control.new_line;
    // delete this.control.new_polygon;
    // delete this.control.dop_save;
    // delete this.control.dop_cancel;
    // delete this.control.dop_clear;
    delete this.control;

    this.#layer_clear();
    if (this.data) delete this.data;
}

#onLayerAdd = function(e) {
    if ((e.layer instanceof L.Path) || (e.layer instanceof L.Marker)) {
        e.layer.on('click',    L.DomEvent.stop).on('click',    this.#onElementClick.bind(e.layer, this));  // ,e.layer);
        e.layer.on('dblclick', L.DomEvent.stop).on('dblclick', e.layer.toggleEdit);
    }
}

#onElementClick = function(that, e) {
    if ((e.originalEvent.ctrlKey || e.originalEvent.metaKey) && this.editEnabled()) {
        delete that.map.editTools.featuresLayer._layers[e.target._leaflet_id];
        this.remove();
    }
};

#onKeyDown = function (e) {
    switch (e.keyCode) {
    case 13: // KEY_ENTER
        if (!this.map.editTools._drawingEditor) return;
        this.map.editTools.commitDrawing();
        break;

    case 27: // KEY_ESC
        if (!this.map.editTools._drawingEditor) return;
        this.map.editTools.stopDrawing();
        break;

    case 90: // KEY_Z
        // CTRL+Z or CTRL+SHIFT+Z
        if (!this.map.editTools._drawingEditor) return;
        if (e.shiftKey) {
            if (this.#edit_redoBuffer.length) this.map.editTools._drawingEditor.push(this.#edit_redoBuffer.pop());
        } else {
            this.latlng = this.map.editTools._drawingEditor.pop();
            if (this.latlng) this.#edit_redoBuffer.push(this.latlng);
            else             this.map.editTools.stopDrawing();
        }
        break;

    case 77: // KEY_M
        if ((e.shiftKey)&&(!this.map.editTools._drawingEditor)) { this.map.editTools.startMarker(); }
        break;

    case 76: // KEY_L
        if ((e.shiftKey)&&(!this.map.editTools._drawingEditor)) { this.map.editTools.startPolyline(); }
        break;

    case 80: // KEY_P
        if ((e.shiftKey)&&(!this.map.editTools._drawingEditor)) { this.map.editTools.startPolygon(); }
        break;

    }


}

#onDopSave = function() {
    this.data = this.layer_object.toGeoJSON();
    this.cb_data_save(this.data);
    this.#onDopReset();
}

#onDopReset = function() {
    this.#layer_clear();
    this.#layer_set();
}

#onDopClear = function() {
    this.#layer_clear();
}

#layer_set = function() {
    try {
        this.layer_object = (this.data.type=='FeatureCollection')?L.geoJSON(this.data):L.GeoJSON.geometryToLayer(this.data);
        this.layer_object.addTo(this.map);
    } catch {
        alertify.error('Ошибка в данных!');
    }
    this.map.editTools.featuresLayer = this.layer_object; // указывать после заполнения слоя данными
}

#layer_clear = function() {
    this.map.editTools.featuresLayer.clearLayers();
}

}