// Copyright (c) 2020, GreyCube Technologies and contributors
// For license information, please see license.txt
{% include 'erpnext/selling/sales_common.js' %}

frappe.ui.form.on('Client Request CT', {

	is_tray_required:function (frm) {
		frm.toggle_reqd('tray_items', frm.doc.is_tray_required === 1 ? 1:0);
	},
	
	validate:function (frm) {
		frm.toggle_reqd('pickup_date_time', frm.doc.shipment_type === 'PickUp' ? 1:0);
		},
	
	shipment_type:function (frm) {
			frm.toggle_reqd('pickup_date_time', frm.doc.shipment_type === 'PickUp' ? 1:0);
	},
	
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
			frm.set_value('tray_items',[])
		}		
	},	
	update_available_tray_list: function(frm) {

		frm.set_query('item_code', 'tray_items',function(doc, cdt, cdn) {
			return {
				query: "siwar_chocolate.siwar_chocolate.doctype.client_request_ct.client_request_ct.get_available_tray_list",
				filters: {
					'delivery_date': doc.delivery_date
				}
			}
		});	
	}	
});

frappe.ui.form.on('Client Request CT Tray Item', {
	item_code: function(frm, cdt, cdn) {
		if (frm.doc.delivery_date){
			cur_frm.trigger('update_available_tray_list');
		}	
		var row = locals[cdt][cdn];	
		if (frm.doc.delivery_date && row.item_code){
			return frappe.call({
				doc: frm.doc,
				method: "get_tray_qty_details",
				args: {
					"item_code": row.item_code,
					"qty": row.qty

				},
				callback: function(r) {
					console.log(r)
					row = locals[cdt][cdn];
					$.extend(row, r.message);
					refresh_field("tray_items");
				},
				freeze: true
			});			
		}
	},
	qty: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];	
		if (row.qty && row.available_qty && (row.qty>row.available_qty)){
			var msg = __("Table: Tray Item <br> For Row : {0} , Tray : {2} qty entered is : <b>{3}</b>. <br> It should be less than available qty <b>{4}</b>.",
			[row.idx, __(row.doctype), row.item_code, row.qty,row.available_qty])
			frappe.throw(msg);			
		}
	}
})

erpnext.selling.ClientRequestController = erpnext.selling.SellingController.extend({
	onload: function(doc, dt, dn) {
		this._super();
	},

	refresh: function(doc, dt, dn) {
		var me = this;
		this._super();

		this.frm.page.set_inner_btn_group_as_primary(__('Create'));

		this.frm.add_custom_button(__('Gift Qty'), () => this.make_stock_entry_for_gift_qty(), __('Create'));
		this.frm.add_custom_button(__('Return Qty'), () => this.make_stock_entry_for_return_qty(), __('Create'));

		if (this.frm.doc.status == 'Draft' && this.frm.is_new()==undefined) {
			this.frm.add_custom_button(__('Payment'), () => this.make_payment_entry(), __('Create'));
		}
		
		if(flt(doc.docstatus)==1) {
			// var show_tray_return_dialog = me.frm.doc.tray_items.filter(d => d.qty-d.tray_returned_qty>0)
			// if (doc.tray_issue_stock_entry && show_tray_return_dialog && show_tray_return_dialog.length && doc.is_tray_required===1) {
			// 	this.frm.add_custom_button(__('Tray Return'), () => this.tray_return_dialog(doc), __('Create'));
			// }
			frappe.db.get_single_value('Siwar Settings', 'booked_days_after')
			.then(booked_days_after => {

				let release_date=frappe.datetime.add_days(doc.delivery_date,booked_days_after);
				let todays_date=frappe.datetime.get_today()
				if (doc.insurance_amount>0 && todays_date>release_date && doc.is_tray_required===1) {
					this.frm.add_custom_button(__('Return Insurance Amount'), () => this.make_jv_for_insurance_amount(doc), __('Create'));
				}				
			})			


			this.frm.add_custom_button(__('Payment'), () => this.make_payment_entry(), __('Create'));
			if (doc.stock_entry == undefined || doc.stock_entry == '') {
				this.frm.add_custom_button(__("Issue Material"),() => this.make_stock_entry(this.frm), __('Create'));
			}

			if (doc.stock_entry) {
				frappe.db.get_value('Stock Entry', doc.stock_entry, 'docstatus')
				.then(r => {
					if (r.message.docstatus==1 && (doc.sales_invoice == undefined || doc.sales_invoice == '')) {
						this.frm.add_custom_button(__('Invoice'), () => me.make_sales_invoice(), __('Create'));
					}
				})			
			}		
		}
	},
	make_jv_for_insurance_amount: function() {
		return frappe.call({
			method:"siwar_chocolate.siwar_chocolate.doctype.client_request_ct.client_request_ct.make_jv_entry",
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
	make_sales_invoice: function() {
		frappe.model.open_mapped_doc({
			method: "siwar_chocolate.siwar_chocolate.doctype.client_request_ct.client_request_ct.make_sales_invoice",
			frm: this.frm
		})
	},
	// tray_return_dialog: function() {
	// 	var me = this;
	// 	var show_dialog = me.frm.doc.tray_items.filter(d => d.qty-d.tray_returned_qty>0);

	// 	if (show_dialog && show_dialog.length) {

	// 		this.data = [];
	// 		const dialog = new frappe.ui.Dialog({
	// 			title: __("Tick Checkbox and enter qty for return."),
	// 			fields: [
	// 				{
	// 					fieldname: "tray_returns", fieldtype: "Table", label: __("Returns"),
	// 					data: this.data, in_place_edit: true,
	// 					get_data: () => {
	// 						return this.data;
	// 					},
	// 					fields: [{
	// 						fieldtype:'Check',
	// 						in_list_view: 1,
	// 						label: __("Return?"),
	// 						fieldname: 'to_be_returned',
	// 						reqd: 1,
	// 						default:1,
	// 						columns:2

	// 					},
	// 						{
	// 						fieldtype:'Link',
	// 						options: 'Item',
	// 						fieldname:"item_code",
	// 						label: __("Tray Code"),
	// 						in_list_view: 1,
	// 						read_only: 1,
	// 						columns:2
	// 						// hidden: 1
	// 					}, {
	// 						fieldtype:'Data',
	// 						fieldname:"item_name",
	// 						label: __("Tray Name"),
	// 						in_list_view: 1,
	// 						read_only: 1,
	// 						columns:4
	// 					}, {
	// 						fieldtype:'Float',
	// 						in_list_view: 1,
	// 						label: __("Return Qty"),
	// 						fieldname: 'return_requested_qty',
	// 						columns:2

	// 					}]
	// 				},
	// 			],
	// 			primary_action: function() {
	// 				const args = dialog.get_values()["tray_returns"];

	// 				args.forEach(d => {
	// 					if (d.to_be_returned==1){
	// 					frappe.model.set_value("Client Request CT Tray Item", d.docname,
	// 						"return_requested_qty", d.return_requested_qty);
	// 					cur_frm.save()
	// 					}
	// 				});

	// 				me.make_tray_return(cur_frm.doc);
	// 				dialog.hide();
	// 			},
	// 			primary_action_label: __('Return')
	// 		});

	// 		this.frm.doc.tray_items.forEach(d => {
	// 			if (d.qty-d.tray_returned_qty>0) {
	// 				dialog.fields_dict.tray_returns.df.data.push({
	// 					'docname': d.name,
	// 					'to_be_returned':1,
	// 					'item_code': d.item_code,
	// 					'item_name': d.item_name,
	// 					'return_requested_qty': d.qty-d.tray_returned_qty,
	// 				});
	// 			}
	// 		});

	// 		this.data = dialog.fields_dict.tray_returns.df.data;
	// 		dialog.fields_dict.tray_returns.grid.refresh();
	// 		dialog.show()
	// 		setTimeout(() => {
	// 			$('.form-group[data-fieldname="tray_returns"] .grid-add-row').hide()
	// 			$('.form-group[data-fieldname="tray_returns"] .grid-remove-rows').hide()
	// 		}, 250);
			
			
	// 	} else {
	// 		// this.reconcile_payment_entries();
	// 	}
	// },	
	// make_tray_return: function(doc) {
	// 	cur_frm.call({
	// 		method: "make_tray_return",
	// 		doc: doc,
	// 		callback: function(r) {
	// 			if (r.message) {
	// 			let stock_entry=r.message	;
	// 			frappe.msgprint(__("Stock Entry {0} is done. Tray is {1} now.", 
	// 			['<a href="#Form/Stock Entry/'+stock_entry+'">' + stock_entry+ '</a>',doc.tray_status]
	// 			));
	// 			}
	// 		}
	// 	});		
	// },
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
	make_stock_entry_for_gift_qty: function(frm) {
		return frappe.call({
			method:"siwar_chocolate.siwar_chocolate.doctype.client_request_ct.client_request_ct.make_stock_entry_for_gift_qty",
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
	make_stock_entry_for_return_qty: function(frm) {
		frappe.model.open_mapped_doc({
			method: "siwar_chocolate.siwar_chocolate.doctype.client_request_ct.client_request_ct.make_stock_entry_for_return_qty",
			frm: this.frm
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
