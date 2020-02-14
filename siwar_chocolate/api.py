from __future__ import unicode_literals
import frappe, erpnext
import frappe.defaults
from frappe import msgprint, _


def update_client_request_status(self,method):
	client_request_list=frappe.db.get_list('Client Request CT',filters={'stock_entry': self.name},fields=['name', 'status'],as_list=True)
	if client_request_list:
		frappe.db.set_value('Client Request CT', client_request_list[0][0], 'status', 'Ready To Deliver')