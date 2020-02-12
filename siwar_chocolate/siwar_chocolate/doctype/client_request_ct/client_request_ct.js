// Copyright (c) 2020, GreyCube Technologies and contributors
// For license information, please see license.txt
{% include 'erpnext/selling/sales_common.js' %}

frappe.ui.form.on('Client Request CT', {
	refresh: function(frm) {

	},
	onload: function(frm) {
		if (!frm.doc.delivery_date){
			frm.set_value('delivery_date', frappe.datetime.get_today())
		}
		if (frm.doc.delivery_date){
		frm.set_query('tray_no', function(doc, cdt, cdn) {
			return {
				query: "siwar_chocolate.siwar_chocolate.doctype.client_request_ct.client_request_ct.get_available_tray_list",
				filters: {
					'delivery_date': doc.delivery_date
				}
			}
		});	
	}	
	
	}
});
