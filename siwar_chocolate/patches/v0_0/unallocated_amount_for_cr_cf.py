import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
	custom_field = {
		"Payment Entry": [
			{
				"fieldname": "unallocated_amount_for_cr_cf",
				"label": "Unallocated Amount For CR",
				"fieldtype": "Currency",
				"insert_after": "cr_reference_payment_ct",
				"is_custom_field":1,
				"is_system_generated":0,
				"allow_on_submit":1,
				"translatable":0,
				"no_copy":1,
				"read_only":1,
				"precision": 2,
			},			
		]
	}
	
	print('Add Unallocated Amount For CR field in Payment Entry.....')
	create_custom_fields(custom_field, update=True)