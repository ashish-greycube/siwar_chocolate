# Copyright (c) 2013, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from __future__ import unicode_literals
import frappe, erpnext
from frappe import _
from frappe.utils import add_days,cint

def execute(filters=None):
	if not filters: filters = {}
	columns, data = [], []
	columns = get_columns(filters)
	default_company = frappe.db.get_single_value('Global Defaults', 'default_company')
	tray_item_group_cf=frappe.db.get_value('Company', default_company, 'tray_item_group_cf')
	default_tray_warehouse_cf=frappe.db.get_value('Company', default_company, 'default_tray_warehouse_cf')
	delivery_date=filters.get("delivery_date")
	pre_days=frappe.db.get_single_value('Siwar Settings', 'booked_days_before')
	post_days=frappe.db.get_single_value('Siwar Settings', 'booked_days_after')	
	booked_from_date=add_days(delivery_date,-cint(pre_days))
	booked_to_date=add_days(delivery_date,cint(post_days))	
	condition_1=" "

	tray_items_sql="""
		SELECT
			item.item_code as item_code,
			item.item_name as item_name,
			item.description as description,
			0.0 as total_qty,
			0.0 as already_booked_qty,
			0.0 as available_qty_for_booking
		FROM			
			`tabItem` AS item
		WHERE
			item.item_group='{tray_item_group_cf}'
		{condition}""".format(tray_item_group_cf=tray_item_group_cf,condition=condition_1)

	tray_items = frappe.db.sql(tray_items_sql,as_dict=1)
	tray_list=[]
	for item in tray_items:
		bin_list=frappe.db.get_all('Bin', filters={
    										'warehouse': ['=', default_tray_warehouse_cf],
											'item_code': ['=', item.item_code]},
										fields=['actual_qty'],
										as_list=False)	
		actual_qty=0									
		if len(bin_list)>0:
			actual_qty=bin_list[0]['actual_qty']
		already_booked_qty=0
		available_qty=0
		booked_tray_list=frappe.db.sql('''select Trays.qty from `tabClient Request CT` CR inner join  `tabClient Request CT Tray Item` Trays
							on Trays.parent=CR.name
							where 
							CR.docstatus=1 
							and Trays.item_code=%s
							and CR.delivery_date between %s and %s
				''', (item.item_code,booked_from_date, booked_to_date), as_dict=True)


		if booked_tray_list:
			for tray in booked_tray_list:
				already_booked_qty=tray['qty']+already_booked_qty
		available_qty=actual_qty-already_booked_qty		
		item.total_qty=actual_qty
		item.already_booked_qty=already_booked_qty
		item.available_qty_for_booking=available_qty
		tray_list.append([item.item_code,item.item_name,item.description,item.total_qty,item.already_booked_qty,item.available_qty_for_booking])
	data=tray_list
	return columns, data

def get_columns(filters):
	"""return columns"""
	columns = [
		{"label": _("Tray Code"), "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 170},
		{"label": _("Tray Name"), "fieldname": "item_name", "width": 200},
		{"label": _("Description"), "fieldname": "description", "width": 250},
		{"label": _("Total Qty"), "fieldname": "total_qty", "fieldtype": "Float", "width": 130, "convertible": "qty"},
		{"label": _("Already Booked Qty"), "fieldname": "already_booked_qty", "fieldtype": "Float", "width": 140, "convertible": "qty"},
		{"label": _("Available Qty For Booking"), "fieldname": "available_qty_for_booking", "fieldtype": "Float", "width": 140, "convertible": "qty"},
	]
	return columns		
