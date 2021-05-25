
onclick="open1('../../easyui/demo/window/inlinewindow.html',this)"
onclick="open2();event.stopPropagation();"


```html
    <div id="map" class="easyui-layout" data-options="fit:true" style="width:100%;height:100%;">
        <div data-options="region:'north',split:false,border:false,collapsible:true" style="height:35px;"></div>
        <div data-options="region:'east',split:true,title:'East'" style="width:100px;"></div>
        <div data-options="region:'west',split:true,title:'Анализ',collapsed:true,expandMode:'dock',collapsedSize:2,headerCls:'map-head'"style="width:300px;"></div>
        <div data-options="region:'center',title:'1111'" style="padding:5px;background:#eee;"></div>
    </div>
```


# options
```python
function west_on_mouseenter(){
       var opts = $(this).panel('options');
    var ep = 'expand'+opts.region.substr(0,1).toUpperCase()+opts.region.substr(1);
    $('#layout').layout('panel',ep).unbind('.ep').bind('mouseenter.ep',function(){
       $('#layout').layout('expand', opts.region);
    })
}
```

# expand / collapse
```python
$(document).ready(function(){
    var p = $('#map');
    var p_main = p.layout('panel','west');
    var p_parent = p_main.parent().panel();
    var p_expand = p.layout('panel','expandWest');
    p_main.panel('options');
    //p_expand.trigger('click');
    $('#map').layout({
        onExpand: function(region){
            //var cp = $(this).layout('panel','center');
            //var width = cp.panel('panel').outerWidth();
            //console.log('onExpand');
            if (WEST_NEED_COLLAPSE) $('#map').layout('collapse', 'west');
            WEST_NEED_COLLAPSE = false;
        },
        onCollapse: function(region){
            //var cp = $(this).layout('panel','center');
            //var width = cp.panel('panel').outerWidth();
            //console.log('onCollapse');
            WEST_NEED_COLLAPSE = false;
        }
    })
```

```python
var p = $('body').layout('panel','west');  // get the west panel
console.log(p.panel('options').width);  // output the panel's width
console.log(p.width());  // output the panel's inner width
```
    // let p_main = $('#layout').layout('panel','center').panel();
    // p_main.panel('resize', function(){
    //     console.log('+');
    // });
