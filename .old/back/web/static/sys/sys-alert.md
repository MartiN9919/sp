#ПРИМЕРЫ

alerts.set(content="...", type='warn', wait=100, descript='...', users='.. ..', groups='.. ..');

alerts.dlg_admin();

alerts.init();

alertify.init();
alertify.set({ labels : { ok: "Ок", cancel: "Отмена" } });
alertify.set({ buttonFocus: "cancel" });
//alertify.confirm("Message");
alertify.confirm("Message", function (e) {
    if (e) {
        // user clicked "ok"
    } else {
        // user clicked "cancel"
    }
});

alertify.alert("Привет!!!");
alertify.success("Success notification");
