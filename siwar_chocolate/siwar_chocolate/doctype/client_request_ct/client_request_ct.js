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
    not_confirmed_crt: function (frm) {
        var curfieldname = 'not_confirmed_crt';
        var grp_name = 'client_request_type';
        if (frm.doc.not_confirmed_crt == 1) {
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
    // -- delivery time group
    // -- synch with delivery select
    pdt_5_to_7_30_pm: function (frm) {
        var curfieldname = 'pdt_5_to_7_30_pm';
        var grp_name = 'pickup_delivery_times';
        if (frm.doc.pdt_5_to_7_30_pm == 1) {
            disable_other(frm, curfieldname, grp_name);
            frm.set_value('أوقات_التوصيل', 'من الساعة 5:00 حتى الساعة 7:30 مساءً');
        }
    },
    pdt_4_pm: function (frm) {
        var curfieldname = 'pdt_4_pm';
        var grp_name = 'pickup_delivery_times';
        if (frm.doc.pdt_4_pm == 1) {
            disable_other(frm, curfieldname, grp_name);
            frm.set_value('أوقات_التوصيل', 'الساعة 4 مساءً');
        }
    },
    pdt_5_pm: function (frm) {
        var curfieldname = 'pdt_5_pm';
        var grp_name = 'pickup_delivery_times';
        if (frm.doc.pdt_5_pm == 1) {
            disable_other(frm, curfieldname, grp_name);
            frm.set_value('أوقات_التوصيل', 'الساعة 5 مساءً');
        }
    },
    // shipment type group
    // -- set district for pickup and set item to cover delivery cost
    pickup: function (frm) {
        var curfieldname = 'pickup';
        var grp_name = 'shipment_type';
        if (frm.doc.pickup == 1) {
            disable_other(frm, curfieldname, grp_name);
            frm.set_value('customer_district_cf', 'Siwar');
        } else {
            frm.set_value('customer_district_cf', '');
        }
    },
    // on click on delivery checkbox, get delivery item from siwar settings and check if item is not exists 
    // in child table then add it into child table.
    delivery: function (frm) {
        var curfieldname = 'delivery';
        var grp_name = 'shipment_type';
        if (frm.doc.delivery == 1) {
            disable_other(frm, curfieldname, grp_name);
        }
        frappe.db.get_single_value('Siwar Settings', 'delivery_item')
            .then(delivery_item => {
                let found = false;
                let i = frm.doc.items;
                for (i = 0; i < frm.doc.items.length; i++) {
                    if (frm.doc.items[i].item_code == delivery_item) {
                        found = true
                        frappe.show_alert('Delivery Item already exist');
                        break;
                    }
                }
                if (found === false) {
                    let row = frm.add_child('items', {
                        item_code: delivery_item,
                    });
                    frm.refresh_field('items');
                }
            })
    },
    // supervision   status group
    // cover supervision cost
    supervision: function (frm) {
        var curfieldname = 'supervision';
        var grp_name = 'supervision_status';
        if (frm.doc.supervision == 1) {
            disable_other(frm, curfieldname, grp_name);
        }
        frappe.db.get_single_value('Siwar Settings', 'supervision_item')
            .then(supervision_item => {
                let found = false;
                let i = frm.doc.items;
                for (i = 0; i < frm.doc.items.length; i++) {
                    if (frm.doc.items[i].item_code == supervision_item) {
                        found = true
                        frappe.show_alert('Supervision Item already exist');
                        break;
                    }
                }
                if (found === false) {
                    let row = frm.add_child('items', {
                        item_code: supervision_item,
                    });
                    frm.refresh_field('items');
                }
            })
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
        if ((frm.doc.in_call_crt) || (frm.doc.not_confirmed_crt)) {
            frappe.throw(__('You cannot submit as the client request type is either <b>in call</b> or <b>not confirmed</b>'));
        }
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


				// let release_date=frappe.datetime.add_days(doc.delivery_date,booked_days_after);
				// let todays_date=frappe.datetime.get_today()
				if (doc.insurance_amount>0 && doc.is_tray_required===1 && (doc.journal_entry==''||doc.journal_entry===undefined)) {
					this.frm.add_custom_button(__('Return Insurance Amount'), () => this.make_jv_for_insurance_amount(doc), __('Create'));
				}				
					


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
				let url_list = '<a href="#Form/'+doclist[0].doctype+'/'+ doclist[0].name+'" target="_blank">' + doclist[0].name + '</a><br>'
				frappe.msgprint({
					title: __('Returned Insurance Amount'),
					indicator: 'green',
					message: __(url_list)
				})	
				setTimeout(() => {
				window.open("#Form/"+doclist[0].doctype+"/" + doclist[0].name)
				}, 500);			
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

function disable_other(frm,curfieldname,grp_name){
     
    var select_grp_type_values = {
        "client_request_type": ['showroom_crt','occasion_section_crt', 'customer_service_crt', 'in_call_crt','not_confirmed_crt'],
        "customer_city_cf" : ['dammam_city','al_medina','jadda','riyadh'],
        "pickup_delivery_times": ['pdt_5_to_7_30_pm','pdt_4_pm','pdt_5_pm'],
        "shipment_type" : ['delivery','pickup'],
        "supervision_status" : ['supervision','no_supervision']
    };

    var all_uncheck = select_grp_type_values[grp_name]
    

    for (var i = 0; i < all_uncheck.length; i++) {
         if (curfieldname != all_uncheck[i] ) 
         {
              frm.set_value(all_uncheck[i], 0);
             
         }
         else{
             frm.set_value(all_uncheck[i], 1);
         }
    }

}
