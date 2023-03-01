// Copyright (c) 2021, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Siwar Settings', {
	setup: function(frm) {
		frm.set_query('delivery_item', () => {
			return {
				filters: {
					is_stock_item: 0
				}
			}
		})
		frm.set_query('supervision_item', () => {
			return {
				filters: {
					is_stock_item: 0
				}
			}
		})
		frm.set_query('rent_item', () => {
			return {
				filters: {
					is_stock_item: 0
				}
			}
		})				
	}
});
