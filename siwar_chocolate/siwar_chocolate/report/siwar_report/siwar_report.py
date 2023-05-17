# Copyright (c) 2023, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import add_months, nowdate
from frappe.utils import getdate


def execute(filters=None):
	if not filters:
		filters = {}

	columns = get_columns(filters)
	data = get_entries(filters)

	return columns, data

def get_columns(filters):
	columns = [
		{
			"label": _("Cr No"),
			"fieldname": "cr_no",
			"fieldtype": "Link",
			"options": "Client Request CT",
			"width": 130,
		},
		{
			"label": _("Customer Name"),
			"fieldname": "customer",
			"fieldtype": "Link",
			"options": "Customer",
			"width": 140,
		},
		{
			"label": _("Phone Number"),
			"fieldname": "phone_no",
			"fieldtype": "Data",
			"width": 140,
		},
		{
			"label": _("Delivery/Pickup Date"), 
   			"fieldname": "delivery_date", 
			"fieldtype": "Date", 
			"width": 130
		},
		{
			"label": _("Tray Code"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 100,
		},
		{
			"label": _("Qty of Booked Trays"),
			"fieldname": "already_booked_qty",
			"fieldtype": "Float",
			"width": 160,
		},
		{
			"label": _("Available qty in default tray warehouse"),
			"fieldname": "available_qty",
			"fieldtype": "Float",
			"width": 140,
		},
		{
			"label": _("Qty of Booked trays which will be available"),
			"fieldname": "booked_tray_which_will_be_available",
			"fieldtype": "Float",
			"width": 140,
		}
	]

	return columns

def get_entries(filters):

	conditions = get_conditions(filters)
	entries = frappe.db.sql(
		"""
		SELECT
			cr.name as cr_no, cr.customer, cr.phone_no, cr.delivery_date, cri.item_code, cri.already_booked_qty
		FROM
			`tabClient Request CT` cr, `tabClient Request CT Tray Item` cri
		WHERE
			cr.name = cri.parent
		{0}
		""".format(conditions),filters,as_dict=1,
	)

	for entry in entries:
		item = entry.get("item_code")
		default_company = frappe.db.get_single_value('Global Defaults', 'default_company')
		default_tray_warehouse_cf = frappe.db.get_value('Company', default_company, 'default_tray_warehouse_cf')
		available_qty = 0
		
		
		default_tray_warehouse_bin_list = frappe.db.get_all('Bin', filters={
            'warehouse': ['=', default_tray_warehouse_cf],
            'item_code': ['=', item]
        }, fields=['actual_qty'], as_list=False)
		
		if len(default_tray_warehouse_bin_list) > 0:
			available_qty = default_tray_warehouse_bin_list[0]['actual_qty']
			entry["available_qty"] = available_qty
			
			
		reserved_booked_trays_for_days = frappe.db.get_single_value('Siwar Settings', 'reserved_booked_trays_for_days') or 3
		booked_tray_which_will_be_available = 0
		booked_from_date = frappe.utils.add_days(entry.get("delivery_date"), -int(reserved_booked_trays_for_days))
		booked_tray_list = frappe.db.sql('''
            SELECT Trays.qty
            FROM `tabClient Request CT` CR
            INNER JOIN `tabClient Request CT Tray Item` Trays ON Trays.parent = CR.name
            WHERE 
                CR.docstatus = 1
                AND Trays.item_code = %s
                AND CR.delivery_date <= %s
                AND Trays.reserve_tray IS NOT NULL
        ''', (item, booked_from_date), as_dict=True)
			
		if booked_tray_list:
			for tray in booked_tray_list:
				booked_tray_which_will_be_available += tray['qty']
		entry["booked_tray_which_will_be_available"] = booked_tray_which_will_be_available



	return entries

def get_conditions(filters):
	
	conditions =""

	if filters.get("cr_no"):
		conditions += " and cr.name = %(cr_no)s"

	if filters.get("customer"):
		conditions += " and customer = %(customer)s"

	if filters.get("delivery_date"):
		conditions += " and cr.delivery_date = %(delivery_date)s"
		
	if filters.get("client_request_date"):
			conditions += " and cr.client_request_date between {0} and {1}".format(
        		frappe.db.escape(filters["client_request_date"][0]),
        		frappe.db.escape(filters["client_request_date"][1]),
    )

	if filters.get("tray_code"):
		conditions += " and cri.item_code = %(tray_code)s"

	return conditions