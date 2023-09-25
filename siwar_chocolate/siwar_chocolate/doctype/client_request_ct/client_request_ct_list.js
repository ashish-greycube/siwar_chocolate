frappe.listview_settings['Client Request CT'] = {
	add_fields: ["customer", "delivery_date", "status","grand_total"],
	hide_name_column: true,
	get_indicator: function (doc) {
		if (doc.status === "Draft") {
			return [__("Draft"), "yellow", "status,=,Draft"];
		} else if (doc.status === "Submitted") {
			return [__("Submitted"), "orange", "status,=,Submitted"];
		} else if (doc.status === "Under Preparation") {
			return [__("Under Preparation"), "red", "status,=,Under Preparation"];
		} else if (doc.status === "Ready To Deliver") {
			return [__("Ready To Deliver"), "green", "status,=,Ready To Deliver"];
		} else if (doc.status === "Delivered") {
			return [__("Delivered"), "purple", "status,=,Delivered"];
		}
		else if (doc.status === "Cancelled") {
			return [__("Cancelled"), "red", "status,=,Cancelled"];
		}
		
	},
	onload: function(listview) {
	}
};
