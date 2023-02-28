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
			client_request_doc.grand_total = sum([flt(client_item.amount) for client_item in client_request_items ])
			client_request_doc.base_grand_total=client_request_doc.grand_total
			client_request_doc.save()


def unlink_client_request_from_sales_invoice(self,method):
	if self.linked_client_request:
		linked_client_request=self.linked_client_request
		sales_invoice=self.name
		frappe.db.set_value('Client Request CT',linked_client_request, 'sales_invoice', '')
		frappe.db.set_value('Sales Invoice', sales_invoice , 'linked_client_request', '')
		frappe.db.set_value('Client Request CT', linked_client_request, 'status', 'Submitted')
		frappe.db.commit()
		frappe.msgprint(_("Sales Invoice {0} and Client Request {1} are unlinked.")
						.format(sales_invoice, linked_client_request))	
				

def unlink_client_request_from_stock_entry(self,method):
	# unlink material issue
	if self.client_request_material_issue:
		client_request_material_issue=self.client_request_material_issue
		stock_entry=self.name
		frappe.db.set_value('Client Request CT',client_request_material_issue, 'stock_entry', '')
		frappe.db.set_value('Stock Entry', stock_entry , 'client_request_material_issue', '')
		frappe.db.set_value('Client Request CT', client_request_material_issue, 'status', 'Submitted')
		frappe.db.commit()
		frappe.msgprint(_("Stock Entry {0} and Client Request {1} are unlinked.")
						.format(stock_entry, client_request_material_issue))
	# unlink material transfer
	client_request_for_material_transfers=frappe.db.get_list('Client Request CT Tray Item', filters={'reserve_tray': ['=', self.name]},fields=['name', 'parent']) 
	for client_request in client_request_for_material_transfers:
		frappe.db.set_value('Client Request CT Tray Item',client_request.name, 'reserve_tray', None)
		frappe.msgprint(_("Stock Entry {0} and Client Request {1} are unlinked.")
						.format(self.name, client_request.parent))		