frappe.ui.form.on("Company", {
    setup: function (frm) {
        let filters = [
            ["Warehouse", 'company', '=', frm.doc.name],
            ["Warehouse", "is_group", "=", 0],
        ]
        frm.set_query("default_client_warehouse_cf", function () {
            return {
                filters: filters
            };
        });
        frm.set_query("default_tray_warehouse_cf", function () {
            return {
                filters: filters
            };
        });

    },
    validate: function (frm) {
        if (frm.doc.default_client_warehouse_cf && frm.doc.default_tray_warehouse_cf) {
            if (frm.doc.default_client_warehouse_cf === frm.doc.default_tray_warehouse_cf) {
                frappe.throw(__("Default warehouse for client and tray should be different."));
            }
        }
    }
});