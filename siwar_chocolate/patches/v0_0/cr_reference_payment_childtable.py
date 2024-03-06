import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
	custom_field = {
		"Payment Entry": [
			{
				"fieldname": "cr_reference_payment_ct",
				"label": "Client Request Reference Payment",
				"fieldtype": "Table",
				"insert_after": "references",
				"options":"CR Reference Payment",
				"is_custom_field":1,
				"is_system_generated":0,
				"allow_on_submit":1,
				"translatable":0,
				"no_copy":1,
				"read_only":1
			},			
		]
	}
	
	print('Add Client Request Reference Payment table field in Payment Entry.....')
	create_custom_fields(custom_field, update=True)