# Copyright (c) 2023, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import add_months, nowdate
from frappe.utils import getdate
from frappe.utils import flt,add_days,cint


def execute(filters=None):
	if not filters:
		filters = {}

	columns = get_columns(filters)
	data = get_entries(filters)
	# message='Note : when no date is specified, to be available is calculated based on today'
	return columns, data

def get_columns(filters):
	columns = [
		{
			"label": _("Cr No"),
			"fieldname": "cr_no",
			"fieldtype": "Link",
			"options": "Client Request CT",
			"width": 100,
		},
		{
			"label": _("Customer Name"),
			"fieldname": "customer",
			"fieldtype": "Link",
			"options": "Customer",
			"width": 140,
		},
		{
			"label": _("Phone No"),
			"fieldname": "phone_no",
			"fieldtype": "Data",
			"width": 100,
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
			"label": _("CR Qty"),
			"fieldname": "qty",
			"fieldtype": "Int",
			"width": 100,
		},		
		{
			"label": _("Available"),
			"fieldname": "available_qty",
			"fieldtype": "Int",
			"width": 100,
		},
		{
			"label": _("Booked"),
			"fieldname": "already_booked_qty",
			"fieldtype": "Int",
			"width": 100,
		},		
		{
			"label": _("Total Trays"),
			"fieldname": "total_trays_owned",
			"fieldtype": "Int",
			"width": 100,
		},		
		{
			"label": _("To Be Available"),
			"fieldname": "booked_tray_which_will_be_available",
			"fieldtype": "Int",
			"width": 140,
		},
		{
			"label": _("Booked-To Be Av.."),
			"fieldname": "tray_not_cancelled",
			"fieldtype": "Int",
			"width": 140,
		},	
		{
			"label": _("ToBe Avail CR List"),
			"fieldname": "to_be_available_cr_list",
			"fieldtype": "Small Text",
			"width": 250,
		},			
	]

	return columns

def get_entries(filters):
	return_date=filters.get("return_date")
	# precision_for_qty = 2
	conditions = get_conditions(filters)
	entries = frappe.db.sql(
		"""
		SELECT
			cr.name as cr_no, cr.customer, cr.phone_no, cr.delivery_date, cri.item_code, cri.qty
		FROM
			`tabClient Request CT` cr, `tabClient Request CT Tray Item` cri
		WHERE
			cr.name = cri.parent
		{0}
		""".format(conditions),filters,as_dict=1,
	)

	default_company = frappe.db.get_single_value('Global Defaults', 'default_company')
	default_tray_warehouse_cf = frappe.db.get_value('Company', default_company, 'default_tray_warehouse_cf')
	default_tray_booking_warehouse_cf=frappe.db.get_value('Company', default_company, 'default_tray_booking_warehouse_cf')
	reserved_booked_trays_for_days = frappe.db.get_single_value('Siwar Settings', 'reserved_booked_trays_for_days') or 3

	for entry in entries:
		item = entry.get("item_code")
		# entry.qty=flt(entry.get("qty"),precision_for_qty)
	
		#available_qty 
		available_qty = 0
		default_tray_warehouse_bin_list = frappe.db.get_all('Bin', filters={
            'warehouse': ['=', default_tray_warehouse_cf],
            'item_code': ['=', entry.item_code]
        }, fields=['actual_qty'], as_list=False)
		
		if len(default_tray_warehouse_bin_list) > 0:
			available_qty = default_tray_warehouse_bin_list[0]['actual_qty']
			entry["available_qty"] = available_qty
			# entry["available_qty"] = flt(available_qty,precision_for_qty)

		# already_booked_qty
		already_booked_qty=0									
		default_tray_booking_warehouse_bin_list=frappe.db.get_all('Bin', filters={
											'warehouse': ['=', default_tray_booking_warehouse_cf],
											'item_code': ['=', entry.item_code]},
										fields=['actual_qty'],
										as_list=False)			
		if len(default_tray_booking_warehouse_bin_list)>0:
			already_booked_qty=default_tray_booking_warehouse_bin_list[0]['actual_qty']
			# entry["already_booked_qty"]=flt(already_booked_qty,precision_for_qty)
			entry["already_booked_qty"]=already_booked_qty

		# total_trays_owned
		# entry["total_trays_owned"]=flt((available_qty+already_booked_qty),precision_for_qty)
		entry["total_trays_owned"]=available_qty+already_booked_qty
		
		# booked_tray_which_will_be_available
		booked_tray_which_will_be_available = 0
		cr_list=[]
		booked_from_date = add_days(return_date,-cint(reserved_booked_trays_for_days))
		booked_tray_list = frappe.db.sql('''
            SELECT Trays.qty, CR.name
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
				cr_list.append(tray['name'])
		entry["booked_tray_which_will_be_available"] = booked_tray_which_will_be_available				
		# entry["booked_tray_which_will_be_available"] = flt((booked_tray_which_will_be_available),precision_for_qty)
		entry["to_be_available_cr_list"]=" , ".join(cr_list)
		entry["tray_not_cancelled"]=already_booked_qty-booked_tray_which_will_be_available
		# entry["tray_not_cancelled"]=flt((already_booked_qty-booked_tray_which_will_be_available),precision_for_qty)

	return entries

def get_conditions(filters):
	
	conditions =""

	if filters.get("cr_no"):
		conditions += " and cr.name = %(cr_no)s"

	if filters.get("customer"):
		conditions += " and customer = %(customer)s"

	if filters.get("client_request_date"):
			conditions += " and cr.delivery_date between {0} and {1}".format(
        		frappe.db.escape(filters["client_request_date"][0]),
        		frappe.db.escape(filters["client_request_date"][1]),
    )
	elif filters.get("delivery_date"):
		conditions += " and cr.delivery_date = %(delivery_date)s"

	if filters.get("tray_code"):
		conditions += " and cri.item_code = %(tray_code)s"

	return conditions