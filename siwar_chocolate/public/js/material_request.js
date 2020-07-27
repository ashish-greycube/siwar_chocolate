frappe.ui.form.on("Material Request", {
    refresh: function (frm) {
        if (frappe.route_options) {
            let is_exact_qty_required = frappe.route_options.is_exact_qty_required
            if (is_exact_qty_required === 1) {
                var df = frappe.meta.get_docfield("Material Request Item","qty", cur_frm.doc.name);
                df.read_only = 1; 
                if (frm.is_dirty()) {
                    frm.save()             
                }
            }
        }
    }
});