'use strict';

class Map_media {
constructor({lf}) {
    var that            = this;
    this.PANEL_NAME     = 'panel_media';
    this.lf             = lf;
    this.obj_panel      = new FORM_HIDE('#form_hide_tools', {
        objName:        this.PANEL_NAME,
        objTitle:       'Работа с медиа',
        objWidth:       600,
        objPosition:    'right',
        objTimeVisible: 10,
        selAnchor:      '#panel_main',
    });

    this.refresh();
    this.obj_panel.show();
}

free() {
    this.obj_panel.hide();
    // this.edit_off();

    // if (this.obj_tree) {
    //     this.obj_tree.free();
    //     this.obj_tree = null;
    //     delete this.obj_tree;
    // }

    this.obj_panel.free();
    this.obj_panel = null;
    delete this.obj_panel;
}

getRandomInt(max) {
  return Math.floor(Math.random() * Math.floor(max));
}

refresh() {
    var DOM = {};
    DOM.JS_obj = document.querySelector('#'+this.PANEL_NAME+' .panelScroll');
    DOM.JS_obj.innerHTML = (
        '<div id="panorama" style="height: calc( 100% - 200px );"></div>'+
        '<div id="info" style="height: 200px;"></div>'
    );

    this.viewer = pannellum.viewer('panorama', {
        type:               'equirectangular',
        panorama:           '/static/file/'+this.getRandomInt(4)+'.jpg',
        showControls:       true,
        showZoomCtrl:       false,
        showFullscreenCtrl: true,
        compass:            true,
        autoLoad:           true,
        //hotSpotDebug:     true,
        hotSpots: [
            {
                pitch:              1.7,
                yaw:                -69.1,
                type:               "scene",
                text:               "Идти туда",
                sceneId:            "garreg_lwyd",
                targetPitch:        2.7,
                targetYaw:          -66.9,
                //createTooltipFunc:  customTooltipFunction,
                createTooltipArgs:  ["Garreg Lwyd Trig Point", "gl_marker"],
            }, {
                pitch:              1.7,
                yaw:                -129.1,
                type:               "scene",
                text:               "Туда не ходить",
                sceneId:            "garreg_lwyd",
                targetPitch:        2.7,
                targetYaw:          -126.9,
                //createTooltipFunc:  customTooltipFunction,
                createTooltipArgs:  ["Garreg Lwyd Trig Point", "gl_marker"],
            }, {
                pitch:              -14.7,
                yaw:                147.25,
                type:               "info",
                text:               "Здесь что-то есть!",
            },

        ],
    });

    net_ajax({
        url:  AJ.PANORAMA_GET,
        data: {
            //group: MAIN_GEOMERTY.TYPE,
            //keys:  [DAT_SYS_KEY.ID_GEOMETRY_PARENT, DAT_SYS_KEY.ID_GEOMETRY_NAME,],
        },
        success: function(data) {


            this.obj_panel.loader(false);
        }.bind(this),
    });

}

}
