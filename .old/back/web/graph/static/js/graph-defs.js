class GRAPH_DEFS {

// ***********************************************
// INI
// ***********************************************
defs_ini = function(){
    // function defsAddGradient(nam) {
    // let gradient;
    //     gradient = this.DEFS_D3.append("linearGradient")
    //         .attr("id", nam)
    //         .attr("x2", "0%")
    //         .attr("y2", "100%");
    //     gradient.append("stop")
    //         .attr("class", "start-color")
    //         .attr("offset", "0%");
    //     gradient.append("stop")
    //         .attr("class", "end-color")
    //         .attr("offset", "100%");
    // }

    let shadow = (nam, size) => {
        let tag = this.DEFS_D3.append('filter')
            .attr('id', nam)
            .attr('height', '140%')
            .attr('width',  '140%')             // чтобы тень не обрезалась
            .attr('x', '-20%')
            .attr('y', '-20%');
        tag.append('feGaussianBlur')
            .attr('in', 'SourceAlpha')
            .attr('stdDeviation', size+1)
            .attr('result', 'blur');
        tag.append('feOffset')
            .attr('in', 'blur')
            .attr('dx', size)
            .attr('dy', size)
            .attr('result', 'offsetBlur');
        let feMerge = tag.append('feMerge');
        feMerge.append('feMergeNode')
            .attr('in', 'offsetBlur')
        feMerge.append('feMergeNode')
            .attr('in', 'SourceGraphic');
    };

    let shine = (nam, size) => {
        let tag = this.DEFS_D3.append('filter')
            .attr('id', nam)
            .attr('x', '-5%')
            .attr('y', '-5%')
            .attr('height', '110%')
            .attr('width',  '110%');
        tag.node().innerHTML =
            '<feFlood flood-color="#FFFFFF"/>'+
            '<feGaussianBlur stdDeviation="2"/>'+
                '<feComponentTransfer>'+
                    '<feFuncA type="table"tableValues="0 0 0 1"/>'+
                '</feComponentTransfer>'+
                '<feComponentTransfer>'+
                    '<feFuncA type="table"tableValues="0 1 1 1 1 1 1 1"/>'+
                '</feComponentTransfer>'+
            '<feComposite operator="over" in="SourceGraphic"/>';
    };



    this.DEFS_D3 = this.SVG_D3.append('defs')
        .attr('class', 'global');

    // // .bar1 { fill: url(#gradientGreen); }
    // defsAddGradient("gradientGray");
    // defsAddGradient("gradientGrayLight");
    // defsAddGradient("gradientGreen");
    // defsAddGradient("gradientGreenLight");
    // defsAddGradient("gradientRed");
    // defsAddGradient("gradientRedLight");
    // defsAddGradient("gradientBlue");
    // defsAddGradient("gradientBlueLight");

    // подключить: .style('filter', 'url(#drop-shadow-2)')
    shadow('def-shadow-0', 0);
    shadow('def-shadow-1', 1);
    //shadow('def-shadow-2', 2);
    //shadow('def-shadow-3', 3);

    shine('def-shine-2', 2);
}

}
