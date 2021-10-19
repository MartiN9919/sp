export class PATH_PATTERN {
  constructor(color='gray') {
    this.dat = {
      'path_arrow': [
        {
          offset: 12,
          repeat: 25,
          symbol: L.Symbol.arrowHead({ pixelSize: 15, pathOptions: { color: color, weight: 2, stroke: true }, }),
        },
      ],
    }

  }

  get = function(key) {
    return this.dat[key] ?? []
  }
}



      // var markerLine = L.polyline([[58.44773, -28.65234], [52.9354, -23.33496], [53.01478, -14.32617], [58.1707, -10.37109], [59.68993, -0.65918]], {}).addTo(this.map);
      // var markerPatterns = L.polylineDecorator(markerLine, {
      //   //patterns: this.style_patterns,
      //   patterns: [
      //     { offset: '5%', repeat: '10%', symbol: L.Symbol.marker()}
      //   ]
      // }).addTo(this.map);

