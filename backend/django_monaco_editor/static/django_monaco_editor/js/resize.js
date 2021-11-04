require.config({paths: {'vs': '/static/external/monaco-editor/min/vs'}});

require(['vs/editor/editor.main'], function () {
    let resize = document.getElementById('resize-point')
    let editor = document.getElementById('editor-id')
    let body = document.getElementsByTagName('body')[0]
    function resizeMouseUp() {
        body.removeEventListener('mousemove', resizeMouseMove)
    }

    function resizeMouseDown() {
        body.addEventListener('mouseup', resizeMouseUp)
        body.addEventListener('mousemove', resizeMouseMove)
    }

    function resizeMouseMove(e) {
        editor.style.height = editor.clientHeight + e.movementY + 'px';
    }

    resize.addEventListener("mousedown", resizeMouseDown)
})