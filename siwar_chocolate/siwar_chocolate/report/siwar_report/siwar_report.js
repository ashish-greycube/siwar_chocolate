// Copyright (c) 2023, GreyCube Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["siwar report"] = {
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
			"fieldtype":"Date"
		},
		{
			"label":"Return Date",
			"fieldname":"return_date",
			"fieldtype":"Date"
		},
		{
			fieldname:"client_request_date",
			label: "From Date To Date",
			fieldtype: "DateRange",
			default: [frappe.datetime.add_months(frappe.datetime.get_today(),-1), frappe.datetime.get_today()]
		},
		{
			"label":"Customer Name",
			"fieldname":"customer",
			"fieldtype":"Link",
			"options":"Customer"
		}
	]
};
