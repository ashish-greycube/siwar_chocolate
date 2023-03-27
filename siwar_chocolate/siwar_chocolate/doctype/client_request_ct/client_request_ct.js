// Copyright (c) 2020, GreyCube Technologies and contributors
// For license information, please see license.txt
{% include 'erpnext/selling/sales_common.js' %}

frappe.ui.form.on('Client Request CT', {
	setup: function (frm) {
		frm.set_query('item_code', 'packing_items', () => {
			return {
				filters: {
					is_stock_item: 1
				}
			}
		})
	},
	crt_discount_percentage: function (frm) {
		if (frm.doc.crt_discount_percentage > 0) {
			frm.set_value('crt_discount_amount', 0)
		}
	},
	crt_discount_amount: function (frm) {
		if (frm.doc.crt_discount_amount > 0) {
			frm.set_value('crt_discount_percentage', 0)
		}
	},
	is_tray_required: function (frm) {
		frm.toggle_reqd('tray_items', frm.doc.is_tray_required === 1 ? 1 : 0);
	},

	validate: function (frm) {
		frm.toggle_reqd('pickup_date_time', frm.doc.pickup == 1 ? 1 : 0);

		frm.set_intro("");
		if (frm.doc.tray_items && frm.doc.tray_items.length > 0) {
			var tray_items_grid = frm.fields_dict['tray_items'].grid;
			// filter the rows by the specified condition
			var tray_items_non_reserved_rows = tray_items_grid.grid_rows.filter(function (row) {
				return (row.doc.reserve_tray == '' || row.doc.reserve_tray == undefined);
			});
			// log the filtered rows
			console.log(tray_items_non_reserved_rows);
			if (tray_items_non_reserved_rows.length > 0) {
				frm.set_intro(__("Attention : {0}/{1} Tray Items are pending for reservation", [tray_items_non_reserved_rows.length, frm.doc.tray_items.length]));
			}
		}

	},
	onload: function (frm) {
		if (!frm.doc.delivery_date) {
			frm.set_value('delivery_date', frappe.datetime.get_today())
		}
		if (frm.doc.delivery_date) {
			frm.trigger('update_available_tray_list');
		}
	},

	delivery_date: function (frm) {
		if (frm.doc.delivery_date) {
			frm.trigger('update_available_tray_list');
			frm.set_value('tray_items', [])
		}
	},
	update_available_tray_list: function (frm) {
		frappe.db.get_single_value('Siwar Settings', 'tray_group')
			.then(tray_group => {
				frm.set_query('item_code', 'tray_items', function (doc, cdt, cdn) {
					return {
						filters: {
							'item_group': tray_group,
							'disabled': 0
						}
					}
				});
			})


		// frm.set_query('item_code', 'tray_items',function(doc, cdt, cdn) {
		// 	return {
		// 		query: "siwar_chocolate.siwar_chocolate.doctype.client_request_ct.client_request_ct.get_available_tray_list",
		// 		filters: {
		// 			'delivery_date': doc.delivery_date
		// 		}
		// 	}
		// });	
	},
	// code to check only 1 checkbox at a time, rest all will be set 0
	// --citry request type group  
	showroom_crt: function (frm) {
		var curfieldname = 'showroom_crt';
		var grp_name = 'client_request_type';
		if (frm.doc.showroom_crt == 1) {
			disable_other(frm, curfieldname, grp_name);
		}
	},
	occasion_section_crt: function (frm) {
		var curfieldname = 'occasion_section_crt';
		var grp_name = 'client_request_type';
		if (frm.doc.occasion_section_crt == 1) {
			disable_other(frm, curfieldname, grp_name);
		}
	},
	customer_service_crt: function (frm) {
		var curfieldname = 'customer_service_crt';
		var grp_name = 'client_request_type';
		if (frm.doc.customer_service_crt == 1) {
			disable_other(frm, curfieldname, grp_name);
		}
	},
	in_call_crt: function (frm) {
		var curfieldname = 'in_call_crt';
		var grp_name = 'client_request_type';
		if (frm.doc.in_call_crt == 1) {
			disable_other(frm, curfieldname, grp_name);
		}
	},
	// -- customer city group
	// -- synch with city select
	dammam_city: function (frm) {
		var curfieldname = 'dammam_city';
		var grp_name = 'customer_city_cf';
		if (frm.doc.dammam_city == 1) {
			disable_other(frm, curfieldname, grp_name);
			frm.set_value('customer_city_cf', 'الدمام Dammam');
		}
	},
	al_medina: function (frm) {
		var curfieldname = 'al_medina';
		var grp_name = 'customer_city_cf';
		if (frm.doc.al_medina == 1) {
			disable_other(frm, curfieldname, grp_name);
			frm.set_value('customer_city_cf', 'المدينة المنورة Al-Medina');
		}
	},
	jadda: function (frm) {
		var curfieldname = 'jadda';
		var grp_name = 'customer_city_cf';
		if (frm.doc.jadda == 1) {
			disable_other(frm, curfieldname, grp_name);
			frm.set_value('customer_city_cf', 'جدة jadda');
		}
	},
	riyadh: function (frm) {
		var curfieldname = 'riyadh';
		var grp_name = 'customer_city_cf';
		if (frm.doc.riyadh == 1) {
			disable_other(frm, curfieldname, grp_name);
			frm.set_value('customer_city_cf', 'الرياض Riyadh');
		}
	},

	customer_city_cf: function (frm) {
		const field_cities = ["الرياض Riyadh", "جدة jadda", "الدمام Dammam", "المدينة المنورة Al-Medina"]
		if (field_cities.includes(frm.doc.customer_city_cf)) {
			// valid cities, so do nothing
			if (frm.doc.customer_city_cf == "الرياض Riyadh") {
				if (frm.doc.riyadh == 0) {
					frm.set_value('riyadh', 1)
				}
			}
			if (frm.doc.customer_city_cf == "جدة jadda") {
				if (frm.doc.jadda == 0) {
					frm.set_value('jadda', 1)
				}
			}
			if (frm.doc.customer_city_cf == "الدمام Dammam") {
				if (frm.doc.dammam_city == 0) {
					frm.set_value('dammam_city', 1)
				}
			}
			if (frm.doc.customer_city_cf == "المدينة المنورة Al-Medina") {
				if (frm.doc.al_medina == 0) {
					frm.set_value('al_medina', 1)
				}
			}

		} else {
			//  other than four valid cities
			if (frm.doc.riyadh == 1) {
				// uncheck only if particualr city is checked
				frm.set_value('riyadh', 0);
			}
			if (frm.doc.jadda == 1) {
				// uncheck only if particualr city is checked
				frm.set_value('jadda', 0);
			}
			if (frm.doc.al_medina == 1) {
				// uncheck only if particualr city is checked
				frm.set_value('al_medina', 0);
			}
			if (frm.doc.dammam_city == 1) {
				// uncheck only if particualr city is checked
				frm.set_value('dammam_city', 0);
			}
		}
	},

	// -- delivery time group
	// -- synch with delivery select
	pdt_5_to_7_30_pm: function (frm) {
		var curfieldname = 'pdt_5_to_7_30_pm';
		var grp_name = 'pickup_delivery_times';
		if (frm.doc.pdt_5_to_7_30_pm == 1) {
			disable_other(frm, curfieldname, grp_name);
			frm.set_value('pickup_delivery_times_select', 'من الساعة 5:00 حتى الساعة 7:30 مساءً');
		}
	},
	pdt_4_pm: function (frm) {
		var curfieldname = 'pdt_4_pm';
		var grp_name = 'pickup_delivery_times';
		if (frm.doc.pdt_4_pm == 1) {
			disable_other(frm, curfieldname, grp_name);
			frm.set_value('pickup_delivery_times_select', 'الساعة 4 مساءً');
		}
	},
	pdt_5_pm: function (frm) {
		var curfieldname = 'pdt_5_pm';
		var grp_name = 'pickup_delivery_times';
		if (frm.doc.pdt_5_pm == 1) {
			disable_other(frm, curfieldname, grp_name);
			frm.set_value('pickup_delivery_times_select', 'الساعة 5 مساءً');
		}
	},

	pickup_delivery_times_select: function (frm) {
		const field_timing = ["من الساعة 5:00 حتى الساعة 7:30 مساءً", "الساعة 4 مساءً", "الساعة 5 مساءً"]
		if (field_timing.includes(frm.doc.pickup_delivery_times_select)) {
			// valid timing, so do nothing
			if (frm.doc.pickup_delivery_times_select == "من الساعة 5:00 حتى الساعة 7:30 مساءً") {
				if (frm.doc.pdt_5_to_7_30_pm == 0) {
					frm.set_value('pdt_5_to_7_30_pm', 1)
				}
			}
			if (frm.doc.pickup_delivery_times_select == "الساعة 4 مساءً") {
				if (frm.doc.pdt_4_pm == 0) {
					frm.set_value('pdt_4_pm', 1)
				}
			}
			if (frm.doc.pickup_delivery_times_select == "الساعة 5 مساءً") {
				if (frm.doc.pdt_5_pm == 0) {
					frm.set_value('pdt_5_pm', 1)
				}
			}
		} else {
			if (frm.doc.pdt_5_to_7_30_pm == 1) {
				frm.set_value('pdt_5_to_7_30_pm', 0);
			}
			if (frm.doc.pdt_4_pm == 1) {
				frm.set_value('pdt_4_pm', 0);
			}
			if (frm.doc.pdt_5_pm == 1) {
				frm.set_value('pdt_5_pm', 0);
			}
		}
	},
	// shipment type group
	// -- set district for pickup and set item to cover delivery cost
	pickup: function (frm) {
		var curfieldname = 'pickup';
		var grp_name = 'shipment_type';


		if (frm.doc.pickup == 1) {
			frm.toggle_reqd('pickup_date_time', frm.doc.pickup == 1 ? 1 : 0);

			disable_other(frm, curfieldname, grp_name);
			frm.set_value('customer_district_cf', 'Siwar');
		} else {
			frm.set_value('customer_district_cf', '');
		}
	},
	customer_district_cf: function (frm) {
		const pickup_city = ["Siwar"]
		if (pickup_city.includes(frm.doc.customer_district_cf)) {
			//valid pickup. so don't do anything
		} else {
			if (frm.doc.pickup == 1) {
				frm.set_value('pickup', 0);
			}
		}
	},
	// on click on delivery checkbox, get delivery item from siwar settings and check if item is not exists 
	// in child table then add it into child table.
	delivery: function (frm) {
		var curfieldname = 'delivery';
		var grp_name = 'shipment_type';

		if (frm.doc.delivery == 1) {
			disable_other(frm, curfieldname, grp_name);

			frappe.db.get_single_value('Siwar Settings', 'delivery_item')
				.then(delivery_item => {
					let found = false;
					for (let i = 0; i < frm.doc.items.length; i++) {
						if (frm.doc.items[i].item_code == delivery_item) {
							found = true
							frappe.show_alert('Delivery Item already exist');
							break;
						}
					}
					if (found === false) {
						frappe.db.get_value('Item', delivery_item, ['item_name', 'description', 'delivery_cost_cf'])
							.then(r => {
								remove_empty_child_table_row_from_items(frm)
								let rate = r.message.delivery_cost_cf
								let item_name = r.message.item_name
								let description = r.message.description
								let qty = 1
								let row = frm.add_child('items', {
									item_code: delivery_item,
									description: description,
									item_name: item_name,
									qty: qty,
									rate: rate,
									amount: flt(qty * rate)
								});
								frm.refresh_field('items');
							})
					}
				})
		} else {
			frappe.db.get_single_value('Siwar Settings', 'delivery_item')
				.then(delivery_item => {

					for (let i = 0; i < frm.doc.items.length; i++) {
						if (frm.doc.items[i].item_code == delivery_item) {
							{
								frm.get_field("items").grid.grid_rows[i].remove();
							}
							frm.refresh_field('items');
						}
					}

				})
		}

	},
	// supervision   status group
	// cover supervision cost
	supervision: function (frm) {
		var curfieldname = 'supervision';
		var grp_name = 'supervision_status';
		if (frm.doc.supervision == 1) {
			disable_other(frm, curfieldname, grp_name);

			frappe.db.get_single_value('Siwar Settings', 'supervision_item')
				.then(supervision_item => {

					let found = false;
					for (let i = 0; i < frm.doc.items.length; i++) {
						if (frm.doc.items[i].item_code == supervision_item) {
							found = true
							frappe.show_alert('Supervision Item already exist');
							break;
						}
					}
					if (found === false) {
						frappe.db.get_value('Item', supervision_item, ['item_name', 'description', 'supervision_cost_cf'])
							.then(r => {
								let rate = 0
								if (frm.doc.supervision_rate > 0) {
									rate = frm.doc.supervision_rate
								} else {
									rate = r.message.supervision_cost_cf
								}
								remove_empty_child_table_row_from_items(frm)

								let item_name = r.message.item_name
								let description = r.message.description
								let qty = 1
								let row = frm.add_child('items', {
									item_code: supervision_item,
									description: description,
									item_name: item_name,
									qty: qty,
									rate: rate,
									amount: flt(qty * rate)
								});
								frm.refresh_field('items');
							})
					}
				})
		} else {
			frappe.db.get_single_value('Siwar Settings', 'supervision_item')
				.then(supervision_item => {

					for (let i = 0; i < frm.doc.items.length; i++) {
						if (frm.doc.items[i].item_code == supervision_item) {
							{
								frm.get_field("items").grid.grid_rows[i].remove();
							}
							frm.refresh_field('items');
						}
					}

				})
		}
	},
	no_supervision: function (frm) {
		var curfieldname = 'no_supervision';
		var grp_name = 'supervision_status';
		if (frm.doc.no_supervision == 1) {
			disable_other(frm, curfieldname, grp_name);
		}
	},
	// stop user from  submit whenn client request type is in call or not confirmed.
	before_submit: function (frm) {
		if ((frm.doc.in_call_crt) ) {
			frappe.throw(__('You cannot submit as the client request type is either <b>in call</b> or <b>not confirmed</b>'));
		}
	},
	cancel_tray: function (frm) {
		// get the selected child table rows
		var selected_rows = frm.fields_dict['tray_items'].grid.get_selected_children();
		if (selected_rows.length == 0) {
			frappe.show_alert({
				message: __('Please select tray items for cancellation..'),
				indicator: 'red'
			}, 5);
		} else {
			frm.call('cancel_tray', {
					selected_rows: selected_rows
				})
				.then(r => {
					frm.reload_doc()
					console.log(r)
				})

		}

		// log the selected rows
		console.log(selected_rows);
	},
	reserve_tray: function (frm) {
		// get the selected child table rows
		var selected_rows = frm.fields_dict['tray_items'].grid.data
		if (selected_rows.length == 0) {
			frappe.show_alert({
				message: __('Please select tray items for reservation..'),
				indicator: 'red'
			}, 5);
		} else {
			frm.call('reserve_tray', {
					selected_rows: selected_rows
				})
				.then(r => {
					frm.reload_doc()
					console.log(r)
				})

		}

		// log the selected rows
		console.log(selected_rows);
	},
	refresh: function (frm) {
		if (frm.is_new() == undefined && frm.doc.tray_items && frm.doc.tray_items.length > 0) {
			frm.add_custom_button(__('Reserve Tray'), () => frm.trigger('reserve_tray'));
			frm.add_custom_button(__('Cancel Tray'), () => frm.trigger('cancel_tray'));
		}
		if (frm.is_new() == undefined && frm.doc.outstanding_amount>0) {
			frm.add_custom_button(__('Payment'), () => frm.trigger('make_payment_entry_dialog'));
		}		
	},
	make_payment_entry_dialog: function (frm) {

		frappe.call('siwar_chocolate.siwar_chocolate.doctype.client_request_ct.client_request_ct.get_mode_of_payment_for_which_ref_is_required',{
				company:frm.doc.company
		})
		.then(records => {
			console.log(records);
			let list_of_mop_for_which_ref_is_required=records.message
			console.log('list_of_mop_for_which_ref_is_required',list_of_mop_for_which_ref_is_required,typeof(list_of_mop_for_which_ref_is_required))
			let mop_condition=$.map(list_of_mop_for_which_ref_is_required, (row, idx)=>{ console.log(row);return "(doc.mode_of_payment =='"+row+"')" })
			let mandatory_condition="eval:"+mop_condition.join('||')
			console.log(mandatory_condition)
			let d = new frappe.ui.Dialog({
				title: 'Enter Payment Details',
				fields: [
					{
						label: 'Posting Date',
						fieldname: 'posting_date',
						fieldtype: 'Date',
						default:'Today',
					},
					{
						label: 'Party',
						fieldname: 'party',
						fieldtype: 'Link',
						options: 'Customer',
						default:frm.doc.customer,
						read_only:1
					},
					{
						label: 'Paid Amount',
						fieldname: 'paid_amount',
						fieldtype: 'Currency',
						default: frm.doc.outstanding_amount
					},
					{
						label: 'Mode of Payment',
						fieldname: 'mode_of_payment',
						fieldtype: 'Link',
						options: 'Mode of Payment',
						reqd :1,
					},
					{
						label: 'Cheque/Reference No',
						fieldname: 'reference_no',
						fieldtype: 'Data',
						mandatory_depends_on: mandatory_condition,
						depends_on:mandatory_condition
						
						
					},
					{
						label: 'Cheque/Reference Date',
						fieldname: 'reference_date',
						fieldtype: 'Date',
						mandatory_depends_on: mandatory_condition,
						depends_on:mandatory_condition
						
					},
					{
						label: 'Client Request',
						fieldname: 'client_request_ct',
						fieldtype: 'Data',
						default: frm.doc.name,
						read_only:1					
						
					},				
					
				],
				primary_action_label: 'Create Payment Entry',
				primary_action: function(values) {
					let user_paid_amount=values.paid_amount
					if (user_paid_amount==0 || user_paid_amount > frm.doc.outstanding_amount) {
						var msg = __("Incorrect Paid Amount: {0}",[user_paid_amount])
					frappe.throw(msg);						
					}
					frappe.call({
						
						method: "siwar_chocolate.siwar_chocolate.doctype.client_request_ct.client_request_ct.get_payment_entry",
						args: {
						"dt": cur_frm.doc.doctype,
						"dn": cur_frm.doc.name,
						"posting_date":values.posting_date,
						"user_paid_amount":user_paid_amount,
						"mode_of_payment":values.mode_of_payment,
						"reference_no":values.reference_no,
						"reference_date":values.reference_date
						},					
						callback: function(response) {
							console.log('response',response)
							if (response.message) {
								let url_list = '<a href="/app/payment-entry/'+ response.message + '" target="_blank">' + response.message + '</a><br>'
								frappe.show_alert({
									title:__('Payment Entry is created'),
									message: __(url_list),
									indicator:'green'
								}, 12);													
							}
						}
					});
					// close the dialog box
					d.hide();
				},
			});
			d.show();
		});
	},
	delivery_rate: function (frm) {
		if (frm.doc.delivery_rate && frm.doc.delivery_rate > 0) {
			frappe.db.get_single_value('Siwar Settings', 'delivery_item')
				.then(delivery_item => {
					let found = false;
					for (let i = 0; i < frm.doc.items.length; i++) {
						if (frm.doc.items[i].item_code == delivery_item) {
							found = true
							frappe.model.set_value(frm.doc.items[i].doctype, frm.doc.items[i].name, "rate", frm.doc.delivery_rate);
							break;
						}
					}
				})
		}
	},
	supervision_rate: function (frm) {
		if (frm.doc.supervision_rate && frm.doc.supervision_rate > 0) {
			frappe.db.get_single_value('Siwar Settings', 'supervision_item')
				.then(supervision_item => {
					let found = false;
					for (let i = 0; i < frm.doc.items.length; i++) {
						if (frm.doc.items[i].item_code == supervision_item) {
							found = true
							frappe.model.set_value(frm.doc.items[i].doctype, frm.doc.items[i].name, "rate", frm.doc.supervision_rate);
							break;
						}
					}
				})
		}
	}
});

frappe.ui.form.on('Client Request CT Tray Item', {
	item_code: function (frm, cdt, cdn) {
		if (frm.doc.delivery_date) {
			cur_frm.trigger('update_available_tray_list');
		}
		var row = locals[cdt][cdn];
		if (frm.doc.delivery_date && row.item_code) {
			return frappe.call({
				doc: frm.doc,
				method: "get_tray_qty_details",
				args: {
					"item_code": row.item_code,
					"qty": row.qty,
					// "delivery_rate_from_user": frm.doc.delivery_rate

				},
				callback: function (r) {
					console.log(r)
					row = locals[cdt][cdn];
					$.extend(row, r.message);
					refresh_field("tray_items");
				},
				freeze: true
			});
		}
	},
	rent_rate: function (frm, cdt, cdn) {caclculate_rent_amount(frm, cdt, cdn)},
	deposit_rate: function (frm, cdt, cdn) {caclculate_deposit_amount(frm, cdt, cdn)},
	qty: function (frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		if (row.qty && row.available_qty && (row.qty > row.available_qty)) {
			var msg = __("Table: Tray Item <br> For Row : {0} , Tray : {2} qty entered is : <b>{3}</b>. <br> It should be less than available qty <b>{4}</b>.",
				[row.idx, __(row.doctype), row.item_code, row.qty, row.available_qty])
			frappe.throw(msg);
		}
		caclculate_rent_amount(frm, cdt, cdn)
		caclculate_deposit_amount(frm, cdt, cdn)
	}
})
var caclculate_rent_amount= function (frm, cdt, cdn) {
	var row = locals[cdt][cdn];
	row.rent_amount=flt(row.rent_rate*row.qty)
	frm.refresh_field('tray_items')
}

var caclculate_deposit_amount= function (frm, cdt, cdn) {
	var row = locals[cdt][cdn];
	row.deposit_amount=flt(row.deposit_rate*row.qty)
	frm.refresh_field('tray_items')
}
erpnext.selling.ClientRequestController = erpnext.selling.SellingController.extend({
	onload: function (doc, dt, dn) {
		this._super();
	},

	refresh: function (doc, dt, dn) {
		var me = this;
		this._super();

		this.frm.page.set_inner_btn_group_as_primary(__('Create'));

		this.frm.add_custom_button(__('Gift Qty'), () => this.make_stock_entry_for_gift_qty(), __('Create'));
		this.frm.add_custom_button(__('Return Qty'), () => this.make_stock_entry_for_return_qty(), __('Create'));

		// if (this.frm.doc.status == 'Draft' && this.frm.is_new() == undefined) {
		// 	this.frm.add_custom_button(__('Payment'), () => this.make_payment_entry(), __('Create'));
		// }

		if (flt(doc.docstatus) == 1) {
			// var show_tray_return_dialog = me.frm.doc.tray_items.filter(d => d.qty-d.tray_returned_qty>0)
			// if (doc.tray_issue_stock_entry && show_tray_return_dialog && show_tray_return_dialog.length && doc.is_tray_required===1) {
			// 	this.frm.add_custom_button(__('Tray Return'), () => this.tray_return_dialog(doc), __('Create'));
			// }


			// let release_date=frappe.datetime.add_days(doc.delivery_date,booked_days_after);
			// let todays_date=frappe.datetime.get_today()
			if (doc.insurance_amount > 0 && doc.is_tray_required === 1 && (doc.journal_entry == '' || doc.journal_entry === undefined)) {
				this.frm.add_custom_button(__('Return Insurance Amount'), () => this.make_jv_for_insurance_amount(doc), __('Create'));
			}



			// this.frm.add_custom_button(__('Payment'), () => this.make_payment_entry(), __('Create'));
			if (doc.stock_entry == undefined || doc.stock_entry == '') {
				this.frm.add_custom_button(__("Issue Material"), () => this.make_stock_entry(this.frm), __('Create'));
			}

			if (doc.stock_entry) {
				frappe.db.get_value('Stock Entry', doc.stock_entry, 'docstatus')
					.then(r => {
						if (r.message.docstatus == 1 && (doc.sales_invoice == undefined || doc.sales_invoice == '')) {
							this.frm.add_custom_button(__('Invoice'), () => me.make_sales_invoice(), __('Create'));
						}
					})
			}
		}
	},
	make_jv_for_insurance_amount: function () {
		return frappe.call({
			method: "siwar_chocolate.siwar_chocolate.doctype.client_request_ct.client_request_ct.make_jv_entry",
			args: {
				"dt": cur_frm.doc.doctype,
				"dn": cur_frm.doc.name
			},
			callback: function (r) {
				var doclist = frappe.model.sync(r.message);
				let url_list = '<a href="#Form/' + doclist[0].doctype + '/' + doclist[0].name + '" target="_blank">' + doclist[0].name + '</a><br>'
				frappe.msgprint({
					title: __('Returned Insurance Amount'),
					indicator: 'green',
					message: __(url_list)
				})
				setTimeout(() => {
					window.open("#Form/" + doclist[0].doctype + "/" + doclist[0].name)
				}, 500);
			}
		});
	},
	make_sales_invoice: function () {
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
	// make_payment_entry: function () {
	// 	return frappe.call({
	// 		method: "siwar_chocolate.siwar_chocolate.doctype.client_request_ct.client_request_ct.get_payment_entry",
	// 		args: {
	// 			"dt": cur_frm.doc.doctype,
	// 			"dn": cur_frm.doc.name
	// 		},
	// 		callback: function (r) {
	// 			var doclist = frappe.model.sync(r.message);
	// 			frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
	// 		}
	// 	});
	// },
	make_stock_entry_for_gift_qty: function (frm) {
		return frappe.call({
			method: "siwar_chocolate.siwar_chocolate.doctype.client_request_ct.client_request_ct.make_stock_entry_for_gift_qty",
			args: {
				"dt": cur_frm.doc.doctype,
				"dn": cur_frm.doc.name
			},
			callback: function (r) {
				var doclist = frappe.model.sync(r.message);
				frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
			}
		});
	},
	make_stock_entry_for_return_qty: function (frm) {
		frappe.model.open_mapped_doc({
			method: "siwar_chocolate.siwar_chocolate.doctype.client_request_ct.client_request_ct.make_stock_entry_for_return_qty",
			frm: this.frm
		});
	},
	make_stock_entry: function (frm) {
		frappe.model.open_mapped_doc({
			method: "siwar_chocolate.siwar_chocolate.doctype.client_request_ct.client_request_ct.make_stock_entry",
			frm: frm
		});
	}
});
$.extend(cur_frm.cscript, new erpnext.selling.ClientRequestController({
	frm: cur_frm
}));

function disable_other(frm, curfieldname, grp_name) {

	var select_grp_type_values = {
		"client_request_type": ['showroom_crt', 'occasion_section_crt', 'customer_service_crt', 'in_call_crt'],
		"customer_city_cf": ['dammam_city', 'al_medina', 'jadda', 'riyadh'],
		"pickup_delivery_times": ['pdt_5_to_7_30_pm', 'pdt_4_pm', 'pdt_5_pm'],
		"shipment_type": ['delivery', 'pickup'],
		"supervision_status": ['supervision', 'no_supervision']
	};

	var all_uncheck = select_grp_type_values[grp_name]


	for (var i = 0; i < all_uncheck.length; i++) {
		if (curfieldname != all_uncheck[i]) {
			frm.set_value(all_uncheck[i], 0);

		} else {
			frm.set_value(all_uncheck[i], 1);
		}
	}

}

function remove_empty_child_table_row_from_items(frm) {
	// Get the child table
	for (let i = 0; i < frm.doc.items.length; i++) {
		if (frm.doc.items[i].item_code === undefined) {
			{
				frm.get_field("items").grid.grid_rows[i].remove();
			}
			frm.refresh_field('items');
		}
	}

}