
            console.log(param);


        // tt.textbox('textbox').bind('contextmenu', function(e){
        //     console.info('contextmenu');
        // });
        // tt.textbox('textbox').bind('click', function(e){
        //     console.info('click');
        // });
        // tt.textbox('textbox').bind('paste', function(e){
        //     console.info('paste');
        // });
        // tt.textbox('textbox').bind('cut', function(e){
        //     console.info('cut');
        // });
        // tt.textbox('textbox').bind('keydown', function(e){
        //     console.info(e.keyCode);
        //     if (e.keyCode == 13){   // ENTER
        //         t.textbox('setValue', $(this).val());
        //         console.info('keydown');

        //     }
        // });


    // $(this.obj_selector).treegrid({
    //     idField:        'id',
    //     treeField:      'key',
    //     animate:        true,
    //     fit:            true,   // автоширина
    //     fitColumns:     true,   // автоширина
    //     scrollbarSize:  0,
    //     nowrap:         true,   // в одну строку
    //     singleSelect:   true,
    //     width:          '100%',
    //     height:         '100%',
    //     onResizeColumn: this.on_resize_col.bind(this),
    //     columns:[[
    //         { field: 'key', title: 'Ключ',     width: '30%', },
    //         { field: 'val', title: 'Значение', width: '50%', },
    //         { field: 'dat', title: 'Дата',     width: '20%', resizable: false, fixed: true, }, //width: '20%', },   // , align: 'right'
    //     ]],
    //     data: {
    //         //total:tree_data.length,
    //         rows: FORM_TREE.tree_child(_tree_data, 0),
    //     },
    //     // loadFilter: function(rows) {
    //     // },
    // });



function disableEdit(){
    $('#PROGRAM_NAME').textbox({icons:[{
        iconCls:'icon-add',
        handler: iconAddAction
      },
    ]});
    $('#PROGRAM_NAME').textbox({editable: false});
}
function enableEdit(){
    $('#PROGRAM_NAME').textbox({icons:[{
        iconCls:'icon-add',
        handler: iconAddAction
      }, {
        iconCls:'icon-edit',
        handler: iconEditAction
      }
   ]});
    $('#PROGRAM_NAME').textbox({editable: true});
}
function iconAddAction(e){
    alert('add');
}
function iconEditAction(e) {
    alert('edit');
}