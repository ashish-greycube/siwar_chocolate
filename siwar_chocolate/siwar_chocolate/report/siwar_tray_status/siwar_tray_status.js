// Copyright (c) 2023, GreyCube Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Siwar Tray Status"] = {
	"filters": [
		{
			"label":"Cr No.",
			"fieldname":"cr_no",
			"fieldtype":"Link",
			"options":"Client Request CT"
		},
		{
			"label":"Tray Code",
			"fieldname":"tray_code",
			"fieldtype":"Link",
			"options":"Item"
		},
		{
			"label":"Delivery/Pickup Date",
			"fieldname":"delivery_date",
			"fieldtype":"Date",
			// "reqd": 1,
			// "default": frappe.datetime.get_today(),			
		},
		{
			fieldname:"client_request_date",
			label: "From Date To Date(Delivery Dt)",
			fieldtype: "DateRange",
			// depends_on: "eval: !doc.delivery_date",
			// default: [frappe.datetime.add_months(frappe.datetime.get_today(),-1), frappe.datetime.get_today()]
		},
		{
			"label":"Return Date",
			"fieldname":"return_date",
			"fieldtype":"Date",
			"default": frappe.datetime.get_today()
		},		
		{
			"label":"Customer Name",
			"fieldname":"customer",
			"fieldtype":"Link",
			"options":"Customer"
		}
	],
	"formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (column.fieldname == "to_be_available_cr_list") {
			if (data.to_be_available_cr_list) {
				let to_be_available_cr_list_all=String(data.to_be_available_cr_list).split(',');
				let links=[]
				for (let index = 0; index < to_be_available_cr_list_all.length; index++) {
					let cr_name=String(to_be_available_cr_list_all[index]).split(',');
					cr_name=String(cr_name).trim()
					links.push(`<a title="${cr_name}" href="/app/client-request-ct/${cr_name}" >${cr_name}</a>`)
				}
				let link_value = links.join(",")
				return link_value;				
			}
		}		
		// for other normal cols
		return value;
	},	
};