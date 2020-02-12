# -*- coding: utf-8 -*-
# Copyright (c) 2020, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from erpnext.controllers.selling_controller import SellingController

class ClientRequestCT(SellingController):
	def __init__(self, *args, **kwargs):
		super(ClientRequestCt, self).__init__(*args, **kwargs)	

def get_available_tray_list(doctype, txt, searchfield, start, page_len, filters):

	default_company = frappe.db.get_single_value('Global Defaults', 'default_company')
	tray_asset_category_cf = frappe.db.get_value('Company', default_company, 'tray_asset_category_cf')
	delivery_date=filters.get("delivery_date")
	
	print(tray_asset_category_cf,delivery_date)
	test=frappe.db.sql("""select name from `tabAsset` asset where asset_category =%s and name not in
(select distinct(tray_no) from `tabClient Request CT` where 
`tabClient Request CT`.docstatus = 0 and
`tabClient Request CT`.delivery_date =%s)""",(tray_asset_category_cf,delivery_date))
	print('test',test)
	return test
	


