# -*- coding: utf-8 -*-
# Copyright (c) 2020, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, scrub,msgprint
from frappe.model.document import Document
from erpnext.controllers.selling_controller import SellingController
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt,get_url_to_form,nowdate

class ClientRequestCT(Document):
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


def get_available_tray_list(doctype, txt, searchfield, start, page_len, filters):
	default_company = frappe.db.get_single_value('Global Defaults', 'default_company')
	tray_asset_category_cf = frappe.db.get_value('Company', default_company, 'tray_asset_category_cf')
	delivery_date=filters.get("delivery_date")
	available_tray_list=frappe.db.sql("""select name,asset_name from `tabAsset` asset where asset_category =%s and name not in
		(select distinct(tray_no) from `tabClient Request CT` where
		`tabClient Request CT`.docstatus = 1 and
		`tabClient Request CT`.delivery_date =%s)""",(tray_asset_category_cf,delivery_date))
	return available_tray_list

@frappe.whitelist()
def make_stock_entry(source_name, target_doc=None):
	def update_item(obj, target, source_parent):
		# change due to siwari
		target.qty = flt(obj.qty) or 0
		# qty = flt(flt(obj.stock_qty) - flt(obj.qty))/ target.conversion_factor \
		# 	if flt(obj.stock_qty) > flt(obj.qty) else 0
		# target.qty = qty
		# target.transfer_qty = qty * obj.conversion_factor
		target.conversion_factor = obj.conversion_factor

		if source_parent.material_request_type == "Material Transfer" or source_parent.material_request_type == "Customer Provided":
			target.t_warehouse = obj.warehouse
		else:
			target.s_warehouse = obj.warehouse

	def set_missing_values(source, target):
		target.purpose = source.material_request_type
		# if source.job_card:
		# 	target.purpose = 'Material Transfer for Manufacture'

		# if source.material_request_type == "Customer Provided":
		# 	target.purpose = "Material Receipt"

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
			# "condition": lambda doc: doc.qty < doc.stock_qty
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
		# change due to siwari
		target.items=[]
		row = target.append('items', {})
		row.item_code='Mixed Chocolates'
		row.qty =1
		row.rate = flt(source.total)

		items=source.get("items")
		for item in items:
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

		# if source.company_address:
		# 	target.update({'company_address': source.company_address})
		# else:
		# 	# set company address
		# 	target.update(get_company_address(target.company))

		if target.company_address:
			target.update(get_fetch_values("Sales Invoice", 'company_address', target.company_address))

		# set the redeem loyalty points if provided via shopping cart
		# if source.loyalty_points and source.order_type == "Shopping Cart":
		# 	target.redeem_loyalty_points = 1

	def update_item(source, target, source_parent):
		pass
		# target.item_code='Mixed Chocolates'
		# target.qty =1
		# target.rate = flt(source_parent.total)
		# target.amount = flt(source.amount) - flt(source.billed_amt)
		# target.base_amount = target.amount * flt(source_parent.conversion_rate)
		# target.qty = target.amount / flt(source.rate) if (source.rate and source.billed_amt) else source.qty - source.returned_qty

		# if source_parent.project:
		# 	target.cost_center = frappe.db.get_value("Project", source_parent.project, "cost_center")
		# if target.item_code:
		# 	item = get_item_defaults(target.item_code, source_parent.company)
		# 	item_group = get_item_group_defaults(target.item_code, source_parent.company)
		# 	cost_center = item.get("selling_cost_center") \
		# 		or item_group.get("selling_cost_center")

		# 	if cost_center:
		# 		target.cost_center = cost_center
	doclist = get_mapped_doc("Client Request CT", source_name, {
		"Client Request CT": {
			"doctype": "Sales Invoice",
			"field_map": {
				"party_account_currency": "party_account_currency",
				"payment_terms_template": "payment_terms_template"
			},
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Client Request CT Item": {
			"doctype": "Sales Invoice Item",
			"postprocess": update_item,
		},
		"Sales Taxes and Charges": {
			"doctype": "Sales Taxes and Charges",
			"add_if_empty": True
		},
		"Sales Team": {
			"doctype": "Sales Team",
			"add_if_empty": True
		}
	}, target_doc, postprocess, ignore_permissions=ignore_permissions)

	#change due to siwari	
	doclist.save()
	frappe.db.set_value('Client Request CT', source_name, 'sales_invoice', doclist.name)
	frappe.db.set_value('Client Request CT', source_name, 'status', 'Delivered')
	return doclist	
	

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
		# pe.append("references", {
		# 	'reference_doctype': 'Sales Invoice',
		# 	'reference_name': doc.get("sales_invoice"),
		# 	"bill_no": doc.get("bill_no"),
		# 	"due_date": doc.get("due_date"),
		# 	'total_amount': grand_total,
		# 	'outstanding_amount': outstanding_amount,
		# 	'allocated_amount': outstanding_amount
		# })

	pe.setup_party_account_field()
	pe.set_missing_values()
	if party_account and bank:
		pe.set_exchange_rate()
		pe.set_amounts()
	return pe