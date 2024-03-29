# -*- coding: utf-8 -*-
# Copyright (c) 2020, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, scrub,msgprint
from frappe.model.document import Document
from erpnext.controllers.selling_controller import SellingController
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt,get_url_to_form,nowdate,cstr,nowtime,get_link_to_form
from erpnext.stock.utils import get_stock_balance
from frappe.utils import get_link_to_form,flt
from six import string_types
from frappe.utils import add_days
from frappe.utils import cint


class ClientRequestCT(Document):
	# def create_stock_entry(self,tray_return=False):
	# 	default_company = frappe.db.get_single_value('Global Defaults', 'default_company')
	# 	default_client_warehouse_cf=frappe.db.get_value('Company', default_company, 'default_client_warehouse_cf')
	# 	default_tray_warehouse_cf=frappe.db.get_value('Company', default_company, 'default_tray_warehouse_cf')

	# 	if tray_return==False:
	# 		from_warehouse=default_tray_warehouse_cf
	# 		to_warehouse=default_client_warehouse_cf
	# 		posting_date=self.delivery_date
	# 		posting_time="00:01"
	# 	elif tray_return==True:
	# 		from_warehouse=default_client_warehouse_cf
	# 		to_warehouse=default_tray_warehouse_cf
	# 		posting_date=nowdate()
	# 		posting_time=nowtime()
	# 	stock_entry = frappe.new_doc("Stock Entry")
	# 	stock_entry.naming_series='STE-'
	# 	stock_entry.stock_entry_type = "Material Transfer"
	# 	stock_entry.posting_date=posting_date
	# 	stock_entry.posting_time=posting_time
	# 	stock_entry.from_warehouse = from_warehouse
	# 	stock_entry.to_warehouse = to_warehouse
	# 	stock_entry.company = default_company

	# 	if tray_return==False:
	# 		for tray in self.tray_items:
	# 			row=stock_entry.append('items',{})
	# 			row.item_code=tray.item_code
	# 			row.qty=tray.qty
	# 	elif tray_return==True:
	# 		for tray in self.tray_items:
	# 			if tray.return_requested_qty>0:
	# 				if tray.qty-tray.tray_returned_qty>=tray.return_requested_qty:
	# 					row=stock_entry.append('items',{})
	# 					row.item_code=tray.item_code
	# 					row.qty=tray.return_requested_qty
	# 				else:
	# 					frappe.throw(_("Tray {0} has entered qty {1} more than possible return qty {2}.")
	# 					.format(tray.item_code,tray.return_requested_qty,tray.qty-tray.tray_returned_qty),
	# 					title=_('Error'))

	# 	stock_entry.insert(ignore_permissions = True)
	# 	stock_entry.submit()
	# 	if tray_return==True:
	# 		fully_returned=True
	# 		for tray in self.tray_items:
	# 			if tray.return_requested_qty>0:
	# 				if tray.qty-tray.tray_returned_qty>=tray.return_requested_qty:
	# 					tray_returned_qty=flt(tray.return_requested_qty)+flt(tray.tray_returned_qty)
	# 					frappe.db.set_value('Client Request CT Tray Item', tray.name, 'tray_returned_qty', flt(tray_returned_qty))
	# 					frappe.db.set_value('Client Request CT Tray Item', tray.name, 'return_requested_qty',0)
	# 					frappe.db.commit()

	# 		for tray in self.tray_items:
	# 			if tray.qty>flt(tray.return_requested_qty)+flt(tray.tray_returned_qty):
	# 				fully_returned=False
	# 		if fully_returned==True:
	# 			frappe.db.set(self, 'tray_status', 'Available')	
	# 		elif fully_returned==False:
	# 			frappe.db.set(self, 'tray_status', 'Partial Available')																
	# 	return stock_entry.name	

	# def make_tray_return(self):
	# 	default_company = frappe.db.get_single_value('Global Defaults', 'default_company')
	# 	stock_entry=self.create_stock_entry(tray_return=True)
	# 	self.reload()
	# 	self.append('tray_return_stock_entry',{'tray_return_stock_entry':stock_entry})
	# 	self.save()
	# 	self.reload()

	# 	return stock_entry
		
	def on_submit(self):
		if self.is_tray_required==1:
			for tray in self.tray_items:
				if tray.qty>tray.available_qty:
					frappe.throw(_("For Row : {0}, Tray : {1} entered qty is {2}. It should be less than available qty {3}.").format(tray.idx,tray.item_code,tray.qty,tray.available_qty),title=_('Error'))
				tray_list=get_available_tray_list('Item','','name',0,20,{'delivery_date': self.delivery_date},tray.item_code,tray.qty)
				if len(tray_list)==0:
					frappe.throw(_("Tray {0} is occupied. Cannot submit.").format(tray.item_code),title=_('Error'))

			# frappe.db.set(self, 'tray_status', 'Booked')
			# stock_entry=self.create_stock_entry(tray_return=False)
			# frappe.db.set(self, 'tray_issue_stock_entry', stock_entry)

		frappe.db.set(self, 'status', 'Submitted')

	def on_cancel(self):
		stock_entry_docstatus = frappe.db.get_value('Stock Entry', self.stock_entry, 'docstatus')
		sales_invoice_docstatus = frappe.db.get_value('Sales Invoice', self.sales_invoice, 'docstatus')
		# Cannot cancel
		if stock_entry_docstatus == 1 and sales_invoice_docstatus == 1:
			frappe.throw(_("Cannot cancel client request as linked material issue {0} and ").format("<a href='desk#Form/Stock Entry/{0}'> Stock Entry {0} </a>".format(self.stock_entry))
			+_(" linked sales invoice {0} are in submitted state.").format("<a href='desk#Form/Sales Invoice/{0}'> Sales Invoice {0} </a>".format(self.sales_invoice)))
		elif stock_entry_docstatus == 1:
			frappe.throw(_("Cannot cancel client request as linked material issue {0} is in submitted state.").format("<a href='desk#Form/Stock Entry/{0}'> Stock Entry {0} </a>".format(self.stock_entry)))
		elif sales_invoice_docstatus == 1:
			frappe.throw(_("Cannot cancel client request as linked sales invoice {0} is in submitted state.").format("<a href='desk#Form/Sales Invoice/{0}'> Sales Invoice {0} </a>".format(self.sales_invoice)))
		frappe.db.set(self, 'status', 'Cancelled')
		# frappe.db.set(self, 'tray_status', 'Available')

	def get_tray_qty_details(self, args=None):
		default_company = frappe.db.get_single_value('Global Defaults', 'default_company')
		default_tray_warehouse_cf=frappe.db.get_value('Company', default_company, 'default_tray_warehouse_cf')


		if not args:
			args = frappe.form_dict.get('args')

		if isinstance(args, string_types):
			import json
			args = json.loads(args)				
		item = args['item_code']
		qty=args.get('qty') or 1
		delivery_date=self.delivery_date
		pre_days=frappe.db.get_single_value('Siwar Settings', 'booked_days_before')
		post_days=frappe.db.get_single_value('Siwar Settings', 'booked_days_after')
		bin_list=frappe.db.get_all('Bin', filters={
    										'warehouse': ['=', default_tray_warehouse_cf],
											'item_code': ['=', item]},
										fields=['actual_qty'],
										as_list=False)	
		print('bin'*100,bin_list)	
		actual_qty=0									
		if len(bin_list)>0:
			actual_qty=bin_list[0]['actual_qty']
		already_booked_qty=0
		available_qty=0
		booked_from_date=add_days(delivery_date,-cint(pre_days))
		booked_to_date=add_days(delivery_date,cint(post_days))
		booked_tray_list=frappe.db.sql('''select Trays.qty from `tabClient Request CT` CR inner join  `tabClient Request CT Tray Item` Trays
							on Trays.parent=CR.name
							where 
							CR.docstatus=1 
							and Trays.item_code=%s
							and CR.delivery_date between %s and %s
				''', (item,booked_from_date, booked_to_date), as_dict=True)

		if booked_tray_list:
			for tray in booked_tray_list:
				already_booked_qty=tray['qty']+already_booked_qty
		print('--'*100,pre_days,post_days,booked_from_date,booked_to_date,booked_tray_list)
		available_qty=actual_qty-already_booked_qty
		ret_item = {
			 'item_name'	: item and args.get('item_name') or '',
			 'total_qty'  : actual_qty or 0,
			 'already_booked_qty':already_booked_qty or 0,
			 'available_qty':available_qty,
			 'qty'			: args.get("qty") or 1
		}

		return ret_item			


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_available_tray_list(doctype, txt, searchfield, start, page_len, filters,item_code=None,qty=1):
	default_company = frappe.db.get_single_value('Global Defaults', 'default_company')
	tray_item_group_cf=frappe.db.get_value('Company', default_company, 'tray_item_group_cf')
	default_tray_warehouse_cf=frappe.db.get_value('Company', default_company, 'default_tray_warehouse_cf')
	delivery_date=filters.get("delivery_date")
	pre_days=frappe.db.get_single_value('Siwar Settings', 'booked_days_before')
	post_days=frappe.db.get_single_value('Siwar Settings', 'booked_days_after')	
	booked_from_date=add_days(delivery_date,-cint(pre_days))
	booked_to_date=add_days(delivery_date,cint(post_days))	
	if item_code==None:
		condition_1=" "
	else:
		condition_1=" and item.item_code='{item_code}'".format(item_code=item_code)

	tray_items_sql="""
		SELECT
			item.item_code as item_code,
			item.item_name as item_name,
			item.description as description,
			0.0 as qty
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
		item.qty =available_qty
		if item.qty>0:
			tray_list.append([item.item_code,item.item_name,item.description,item.qty])
	return tray_list

#scheduler function
# @frappe.whitelist()
# def update_tray_status():
# 	tray_list=frappe.db.get_all('Client Request CT',
#     filters={
# 		'docstatus':1,
#         'tray_status': 'Booked',
# 		'delivery_date': ['<', nowdate()],
# 		'tray_return_stock_entry':['=', ''],
#     },
#     fields=['name','tray_return_stock_entry'],
#     as_list=False
# 	)
# 	for tray in tray_list:
# 		frappe.db.set_value('Client Request CT', tray.name, 'tray_status', 'With Client')

@frappe.whitelist()
def make_stock_entry(source_name, target_doc=None):
	def update_item(obj, target, source_parent):
		# change due to siwari
		target.qty = flt(obj.qty) or 0
		target.conversion_factor = obj.conversion_factor

		if source_parent.material_request_type == "Material Transfer" or source_parent.material_request_type == "Customer Provided":
			target.t_warehouse = obj.warehouse
		else:
			target.s_warehouse = obj.warehouse

	def set_missing_values(source, target):
		target.client_request_material_issue=source.name
		target.purpose = source.material_request_type

		target.run_method("calculate_rate_and_amount")
		target.set_stock_entry_type()
		target.set_job_card_data()


	doclist = get_mapped_doc("Client Request CT", source_name, {
		"Client Request CT": {
			"doctype": "Stock Entry",
			"validation": {
				"docstatus": ["=", 1],
				"material_request_type": ["in", ["Material Transfer", "Material Issue"]]
			}
		},
		"Client Request CT Item": {
			"doctype": "Stock Entry Detail",
			"field_map": {
				"name": "client_request_ct_item",
				"parent": "client_request_ct",
				"uom": "stock_uom",
			},
			"postprocess": update_item,
			"condition": lambda doc:frappe.get_cached_value('Item', doc.item_code, 'is_stock_item')==1
		}
	}, target_doc, set_missing_values)
	# change due to siwari
	doclist.save()
	frappe.db.set_value('Client Request CT', source_name, 'stock_entry', doclist.name)
	frappe.db.set_value('Client Request CT', source_name, 'status', 'Under Preparation')
	return doclist


@frappe.whitelist()
def make_sales_invoice(source_name, target_doc=None, ignore_permissions=False):
	def postprocess(source, target):
		if source.combine_all_as_mixed_chocolate==1:
			rate=0
			for item in source.get('items'):
				if frappe.get_cached_value('Item', item.item_code, 'is_stock_item')==1:
					rate=rate+item.amount
			row = target.append('items', {})
			row.item_code='Mixed Chocolates'
			row.qty =1
			row.rate = flt(rate)		
		target.linked_client_request=source.name
		set_missing_values(source, target)
		#Get the advance paid Journal Entries in Sales Invoice Advance
		if target.get("allocate_advances_automatically"):
			target.set_advances()	

	def set_missing_values(source, target):
		target.is_pos = 0
		target.ignore_pricing_rule = 1
		target.flags.ignore_permissions = True
		target.run_method("set_missing_values")
		target.run_method("set_po_nos")
		target.run_method("calculate_taxes_and_totals")

		if target.company_address:
			target.update(get_fetch_values("Sales Invoice", 'company_address', target.company_address))

	def update_item(source, target, source_parent):
		target.item_code=source.item_code
		target.item_name=source.item_name
		target.qty=source.qty
		target.rate=source.rate
		target.amount=source.amount
	combine_all_as_mixed_chocolate=frappe.get_cached_value('Client Request CT', source_name, 'combine_all_as_mixed_chocolate')
	doclist = get_mapped_doc("Client Request CT", source_name, {
		"Client Request CT": {
			"doctype": "Sales Invoice",
			"field_map": {
				"party_account_currency": "party_account_currency",
				"payment_terms_template": "payment_terms_template"
			},
			"validation": {
				"docstatus": ["=", 1]
			},
		},
		"Client Request CT Item": {
			"doctype": "Sales Invoice Item",
			"postprocess": update_item,
			"condition": lambda doc:((frappe.get_cached_value('Item', doc.item_code, 'is_stock_item')==0 and combine_all_as_mixed_chocolate==1) or combine_all_as_mixed_chocolate==0)
		},
		"Sales Taxes and Charges": {
			"doctype": "Sales Taxes and Charges",
			"add_if_empty": True
		},
		"Sales Team": {
			"doctype": "Sales Team",
			"add_if_empty": True
		}
	}, target_doc,postprocess,ignore_permissions=ignore_permissions)

	#change due to siwari	
	doclist.save()
	frappe.db.set_value('Client Request CT', source_name, 'sales_invoice', doclist.name)
	frappe.db.set_value('Client Request CT', source_name, 'status', 'Delivered')
	return doclist	

@frappe.whitelist()	
def make_stock_entry_for_gift_qty(dt,dn):
	default_company = frappe.db.get_single_value('Global Defaults', 'default_company')
	default_company_warehouse_cf=frappe.db.get_value('Company', default_company, 'default_company_warehouse_cf')	
	doc = frappe.get_doc(dt, dn)
	stock_entry = frappe.new_doc('Stock Entry')
	stock_entry.naming_series='STE-'
	stock_entry.stock_entry_type='Material Issue'
	stock_entry.from_warehouse=default_company_warehouse_cf
	stock_entry.run_method("set_missing_values")
	stock_entry.run_method("calculate_taxes_and_totals")	
	return stock_entry.as_dict()

@frappe.whitelist()	
def make_stock_entry_for_return_qty(source_name, target_doc=None):
	def update_item(obj, target, source_parent):
		target.qty = flt(obj.qty) or 0
		target.basic_rate = obj.rate
		target.uom=frappe.db.get_value('Item', obj.item_code, 'stock_uom')

	def set_missing_values(source, target):
		target.naming_series='STE-'
		target.stock_entry_type='Material Receipt'		
		target.run_method("onload")
		target.run_method("set_missing_values")
		target.run_method("calculate_rate_and_amount")

	doclist = get_mapped_doc("Client Request CT", source_name, {
		"Client Request CT": {
			"doctype": "Stock Entry",
		},
		"Client Request CT Item": {
			"doctype": "Stock Entry Detail",
			"field_map": {
				"name": "client_request_ct_item",
				"parent": "client_request_ct"
			},
			"postprocess": update_item,
		}
	}, target_doc, set_missing_values)
	return doclist	

@frappe.whitelist()	
def make_jv_entry(dt,dn):
	default_company = frappe.db.get_single_value('Global Defaults', 'default_company')
	default_cash_account=frappe.db.get_value('Company', default_company, 'default_cash_account')
	default_receivable_account=frappe.db.get_value('Company', default_company, 'default_receivable_account')
	doc = frappe.get_doc(dt, dn)
	customer=doc.customer
	insurance_amount=doc.insurance_amount


	journal_entry = frappe.new_doc('Journal Entry')
	journal_entry.voucher_type = 'Journal Entry'
	journal_entry.naming_series='SJV-'
	journal_entry.company = default_company
	journal_entry.posting_date = nowdate()
	account_amt_list = []

	account_amt_list.append({
		"account": default_cash_account,
		"debit_in_account_currency": insurance_amount,
		"reference_type":'Client Request CT',
		"reference_name":dn
		})
	account_amt_list.append({
		"account": default_receivable_account,
		"credit_in_account_currency": insurance_amount,
		"party_type": "Customer",
		"party":customer
		})
	journal_entry.set("accounts", account_amt_list)
	journal_entry.save(ignore_permissions=True)
	frappe.db.set_value(dt, dn, 'journal_entry', journal_entry.name)
	return journal_entry.as_dict()	

@frappe.whitelist()
def get_payment_entry(dt, dn, party_amount=None, bank_account=None, bank_amount=None):
	from erpnext.accounts.party import get_party_account
	from erpnext.accounts.utils import get_account_currency
	from erpnext.accounts.doctype.journal_entry.journal_entry import get_default_bank_cash_account
	from erpnext.accounts.doctype.bank_account.bank_account import get_party_bank_account
	doc = frappe.get_doc(dt, dn)
	# siwari change
	dt="Sales Order"

	if dt in ("Sales Order", "Purchase Order") and flt(doc.per_billed, 2) > 0:
		frappe.throw(_("Can only make payment against unbilled {0}").format(dt))

	if dt in ("Sales Invoice", "Sales Order"):
		party_type = "Customer"
	elif dt in ("Purchase Invoice", "Purchase Order"):
		party_type = "Supplier"
	elif dt in ("Expense Claim", "Employee Advance"):
		party_type = "Employee"
	elif dt in ("Fees"):
		party_type = "Student"

	# party account
	if dt == "Sales Invoice":
		party_account = get_party_account_based_on_invoice_discounting(dn) or doc.debit_to
	elif dt == "Purchase Invoice":
		party_account = doc.credit_to
	elif dt == "Fees":
		party_account = doc.receivable_account
	elif dt == "Employee Advance":
		party_account = doc.advance_account
	elif dt == "Expense Claim":
		party_account = doc.payable_account
	else:
		party_account = get_party_account(party_type, doc.get(party_type.lower()), doc.company)

	if dt not in ("Sales Invoice", "Purchase Invoice"):
		party_account_currency = get_account_currency(party_account)
	else:
		party_account_currency = doc.get("party_account_currency") or get_account_currency(party_account)

	# payment type
	if (dt == "Sales Order" or (dt in ("Sales Invoice", "Fees") and doc.outstanding_amount > 0)) \
		or (dt=="Purchase Invoice" and doc.outstanding_amount < 0):
			payment_type = "Receive"
	else:
		payment_type = "Pay"

	# amounts
	grand_total = outstanding_amount = 0
	if party_amount:
		grand_total = outstanding_amount = party_amount
	elif dt in ("Sales Invoice", "Purchase Invoice"):
		if party_account_currency == doc.company_currency:
			grand_total = doc.base_rounded_total or doc.base_grand_total
		else:
			grand_total = doc.rounded_total or doc.grand_total
		outstanding_amount = doc.outstanding_amount
	elif dt in ("Expense Claim"):
		grand_total = doc.total_sanctioned_amount + doc.total_taxes_and_charges
		outstanding_amount = doc.grand_total \
			- doc.total_amount_reimbursed
	elif dt == "Employee Advance":
		grand_total = doc.advance_amount
		outstanding_amount = flt(doc.advance_amount) - flt(doc.paid_amount)
	elif dt == "Fees":
		grand_total = doc.grand_total
		outstanding_amount = doc.outstanding_amount
	else:
		if party_account_currency == doc.company_currency:
			grand_total = flt(doc.get("base_rounded_total") or doc.base_grand_total)
		else:
			grand_total = flt(doc.get("rounded_total") or doc.grand_total)
		outstanding_amount = grand_total - flt(doc.advance_paid)

	# bank or cash
	bank = get_default_bank_cash_account(doc.company, "Bank", mode_of_payment=doc.get("mode_of_payment"),
		account=bank_account)

	if not bank:
		bank = get_default_bank_cash_account(doc.company, "Cash", mode_of_payment=doc.get("mode_of_payment"),
			account=bank_account)

	paid_amount = received_amount = 0
	if party_account_currency == bank.account_currency:
		paid_amount = received_amount = abs(outstanding_amount)
	elif payment_type == "Receive":
		paid_amount = abs(outstanding_amount)
		if bank_amount:
			received_amount = bank_amount
		else:
			received_amount = paid_amount * doc.conversion_rate
	else:
		received_amount = abs(outstanding_amount)
		if bank_amount:
			paid_amount = bank_amount
		else:
			# if party account currency and bank currency is different then populate paid amount as well
			paid_amount = received_amount * doc.conversion_rate

	pe = frappe.new_doc("Payment Entry")
	pe.payment_type = payment_type
	pe.company = doc.company
	pe.cost_center = doc.get("cost_center")
	pe.posting_date = nowdate()
	pe.mode_of_payment = doc.get("mode_of_payment")
	pe.party_type = party_type
	pe.party = doc.get(scrub(party_type))
	pe.contact_person = doc.get("contact_person")
	pe.contact_email = doc.get("contact_email")
	pe.ensure_supplier_is_not_blocked()

	pe.paid_from = party_account if payment_type=="Receive" else bank.account
	pe.paid_to = party_account if payment_type=="Pay" else bank.account
	pe.paid_from_account_currency = party_account_currency \
		if payment_type=="Receive" else bank.account_currency
	pe.paid_to_account_currency = party_account_currency if payment_type=="Pay" else bank.account_currency
	pe.paid_amount = paid_amount
	pe.received_amount = received_amount
	pe.letter_head = doc.get("letter_head")

	if pe.party_type in ["Customer", "Supplier"]:
		bank_account = get_party_bank_account(pe.party_type, pe.party)
		pe.set("bank_account", bank_account)
		pe.set_bank_account_data()

	# only Purchase Invoice can be blocked individually
	if doc.doctype == "Purchase Invoice" and doc.invoice_is_blocked():
		frappe.msgprint(_('{0} is on hold till {1}'.format(doc.name, doc.release_date)))
	else:
		# siwari change
		pass


	pe.setup_party_account_field()
	pe.set_missing_values()
	if party_account and bank:
		pe.set_exchange_rate()
		pe.set_amounts()
	return pe