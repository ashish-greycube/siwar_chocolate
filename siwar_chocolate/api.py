from __future__ import unicode_literals
import frappe, erpnext
import frappe.defaults
from frappe import msgprint, _
from frappe.utils import flt

def update_client_request_status(self,method):
	client_request_list=frappe.db.get_list('Client Request CT',filters={'stock_entry': self.name},fields=['name', 'status'],as_list=True)
	if client_request_list:
		client_request_name=client_request_list[0][0]
		frappe.db.set_value('Client Request CT',client_request_name, 'status', 'Ready To Deliver')
		stock_items=self.get("items")
		client_request_doc=frappe.get_doc('Client Request CT',client_request_name)
		client_request_items=client_request_doc.get("items")
		changed=False
		for stock_item in stock_items:
			for client_item in client_request_items:
				if (stock_item.item_code==client_item.item_code and flt(stock_item.qty)!= flt(client_item.qty)):
					client_item.qty=flt(stock_item.qty)
					client_item.amount=client_item.qty*flt(client_item.rate)
					changed=True
		if (changed==True):
			client_request_doc.total = sum([flt(client_item.amount) for client_item in client_request_items ])
			client_request_doc.base_grand_total=client_request_doc.total
			client_request_doc.save()