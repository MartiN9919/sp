'use strict';

/*
 **********************************************************************************
 ВАЖНО
 L.AwesomeMarkers
 переделать класс icon-...  ==> icon2-...
 **********************************************************************************
 */

class Class_leaflet_markers {
#leaflet;
constructor(this_leaflet) {
    this.#leaflet     = this_leaflet;
    this.path_images  = '/static/lib-external/leaflet/leaflet/images/';

    //=============================================================================
    this.MARKER_COLOR = 'color_';
    this.COLOR_BLACK  = 'black';    this.MARKER_COLOR_BLACK  = 'color_black';
    this.COLOR_BLUE   = 'blue';     this.MARKER_COLOR_BLUE   = 'color_blue';
    this.COLOR_GOLD   = 'gold';     this.MARKER_COLOR_GOLD   = 'color_gold';
    this.COLOR_GREEN  = 'green';    this.MARKER_COLOR_GREEN  = 'color_green';
    this.COLOR_GRAY   = 'gray';     this.MARKER_COLOR_GRAY   = 'color_gray';
    this.COLOR_ORANGE = 'orange';   this.MARKER_COLOR_ORANGE = 'color_orange';
    this.COLOR_RED    = 'red';      this.MARKER_COLOR_RED    = 'color_red';
    this.COLOR_VIOLET = 'violet';   this.MARKER_COLOR_VIOLET = 'color_violet';
    this.COLOR_YELLOW = 'yellow';   this.MARKER_COLOR_YELLOW = 'color_yellow';
    this.MarkerColor  = L.Icon.extend({
        options: {
            //iconUrl:      'img/marker-icon-2x-green.png',
            shadowUrl:    this.path_images+'marker-shadow2.png',
            iconSize:     [25, 41],
            shadowSize:   [41, 41],
            iconAnchor:   [12, 41],
            popupAnchor:  [1, -34],
        }
    });
    this.#add_color_default(this.COLOR_BLACK);
    this.#add_color_default(this.COLOR_BLUE);
    this.#add_color_default(this.COLOR_GOLD);
    this.#add_color_default(this.COLOR_GREEN);
    this.#add_color_default(this.COLOR_GRAY);
    this.#add_color_default(this.COLOR_ORANGE);
    this.#add_color_default(this.COLOR_RED);
    this.#add_color_default(this.COLOR_VIOLET);
    this.#add_color_default(this.COLOR_YELLOW);


    //=============================================================================
    this.MARKER_PNG = 'png';
    this.MarkerPNG  = L.Icon.extend({
        options: {
            shadowUrl:    this.path_images+'marker-01-shadow.png',
            iconSize:     [32, 37],
            shadowSize:   [51, 37],
            iconAnchor:   [16, 37],
            shadowAnchor: [16, 37],
            popupAnchor:  [0, -30],
        }
    });
    this.add_png(this.MARKER_PNG, this.path_images+'marker-01-ngg.png');

    //=============================================================================
    this.MARKER_DIV     = 'div_';
    this.MARKER_DIV_125 = this.MARKER_DIV+'125';
    this.add_div(this.MARKER_DIV_125, '125');

    //=============================================================================
    this.MARKER_AWESOME     = 'awesome_';
    this.MARKER_EXTRA_TEST  = this.MARKER_AWESOME+'test';
    this.add_awesome(this.MARKER_AWESOME_TEST, 'running');

    //=============================================================================
    this.MARKER_PULSE       = 'pulse_';
    this.MARKER_PULSE_RED   = this.MARKER_PULSE+'red';
    this.MARKER_PULSE_GREEN = this.MARKER_PULSE+'green';
    this.add_pulse(this.MARKER_PULSE_RED,   12, 'red');
    this.add_pulse(this.MARKER_PULSE_GREEN, 12, 'green');

    //L.marker([51.6440259,28.2572954], {icon: icon_ngg}).bindPopup("<strong>НГГ</strong><br />ушел и не поймали").addTo(this.map);

}

#add_color_default = function(color)       { this.add_color(this.MARKER_COLOR+color, this.path_images+'marker-icon-2x-'+color+'.png'); }
add_color = function(marker_name, url_png) { this.#leaflet.markers[marker_name] = new this.MarkerColor({iconUrl: url_png}); }
add_png   = function(marker_name, url_png) { this.#leaflet.markers[marker_name] = new this.MarkerPNG  ({iconUrl: url_png}); }
add_awesome = function(marker_name, icon='star', color_marker='green', color_icon='white') {
    this.#leaflet.markers[marker_name] = L.AwesomeMarkers.icon({
        icon:        icon,
        markerColor: color_marker,
        iconColor:   color_icon,
        prefix:      'fa',
        spin:        true,
    });
}
add_pulse = function(marker_name, size=12, color='red') {
    this.#leaflet.markers[marker_name] = L.icon.pulse({
        iconSize: [size, size],
        color:    color,
    });
}
add_div   = function(marker_name, text) {
    this.#leaflet.markers[marker_name] = L.divIcon({
        iconSize : null,
        html     : '<div class="map-label redborder"><div class="map-label-content">'+text+'</div><div class="map-label-arrow"></div></div>',
    });
}

}