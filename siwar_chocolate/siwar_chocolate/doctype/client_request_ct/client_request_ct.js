// Copyright (c) 2020, GreyCube Technologies and contributors
// For license information, please see license.txt
{% include 'erpnext/selling/sales_common.js' %}

frappe.ui.form.on('Client Request CT', {
	onload: function(frm) {
		if (!frm.doc.delivery_date){
			frm.set_value('delivery_date', frappe.datetime.get_today())
		}
		if (frm.doc.delivery_date){
			frm.trigger('update_available_tray_list');
		}	
	},
	delivery_date: function(frm) {
		if (frm.doc.delivery_date){
			frm.trigger('update_available_tray_list');
		}		
	},	
	tray_no: function(frm) {
		if (frm.doc.delivery_date){
			frm.trigger('update_available_tray_list');
		}		
	},
	update_available_tray_list: function(frm) {
		frm.set_query('tray_no', function(doc, cdt, cdn) {
			return {
				query: "siwar_chocolate.siwar_chocolate.doctype.client_request_ct.client_request_ct.get_available_tray_list",
				filters: {
					'delivery_date': doc.delivery_date
				}
			}
		});	
	}	
});

erpnext.selling.ClientRequestController = erpnext.selling.SellingController.extend({
	onload: function(doc, dt, dn) {
		this._super();
	},

	refresh: function(doc, dt, dn) {
		var me = this;
		this._super();

		this.frm.page.set_inner_btn_group_as_primary(__('Create'));
		this.frm.add_custom_button(__('Tray Return'), () => this.make_tray_return(), __('Create'));

		if (this.frm.doc.status == 'Draft' && this.frm.is_new()==undefined) {
			this.frm.add_custom_button(__('Payment'), () => this.make_payment_entry(), __('Create'));
		}
		
		if(flt(doc.docstatus)==1) {
			this.frm.add_custom_button(__('Payment'), () => this.make_payment_entry(), __('Create'));
			if (doc.stock_entry == undefined) {
				this.frm.add_custom_button(__("Issue Material"),() => this.make_stock_entry(this.frm), __('Create'));
			}

			if (doc.stock_entry) {
				frappe.db.get_value('Stock Entry', doc.stock_entry, 'docstatus')
				.then(r => {
					if (r.message.docstatus==1 && doc.sales_invoice == undefined) {
						this.frm.add_custom_button(__('Invoice'), () => me.make_sales_invoice(), __('Create'));
					}
				})			
			}		
		}
	},
	make_sales_invoice: function() {
		frappe.model.open_mapped_doc({
			method: "siwar_chocolate.siwar_chocolate.doctype.client_request_ct.client_request_ct.make_sales_invoice",
			frm: this.frm
		})
	},
	make_tray_return: function() {
		
	},
	make_payment_entry: function() {
		return frappe.call({
			method:"siwar_chocolate.siwar_chocolate.doctype.client_request_ct.client_request_ct.get_payment_entry",
			args: {
				"dt": cur_frm.doc.doctype,
				"dn": cur_frm.doc.name
			},
			callback: function(r) {
				var doclist = frappe.model.sync(r.message);
				frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
			}
		});
	},
	make_stock_entry: function(frm) {
		frappe.model.open_mapped_doc({
			method: "siwar_chocolate.siwar_chocolate.doctype.client_request_ct.client_request_ct.make_stock_entry",
			frm: frm
		});
	}
});
$.extend(cur_frm.cscript, new erpnext.selling.ClientRequestController({frm: cur_frm}));
