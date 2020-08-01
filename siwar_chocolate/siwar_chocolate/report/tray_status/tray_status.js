frappe.query_reports["Tray Status"] = {
	"filters": [
		
		{
			"fieldname":"as_on_date",
			"label": __("As on Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": frappe.datetime.get_today()
        }
    ]
}