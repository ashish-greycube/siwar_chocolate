// Copyright (c) 2016, GreyCube Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Tray availability"] = {
	"filters": [
		{
			"fieldname":"delivery_date",
			"label": __("Check On Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"default": frappe.datetime.get_today(),
		}
	]
};
