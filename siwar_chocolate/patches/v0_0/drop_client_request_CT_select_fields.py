import frappe

def execute():
  if frappe.db.exists("DocType", "Client Request CT"):

    frappe.reload_doc("siwar_chocolate", "doctype", "client_request_ct")
    frappe.delete_doc_if_exists("Client Request CT", "client_request_type")
    frappe.delete_doc_if_exists("Custom Field", "Client Request CT-client_request_type")  

    frappe.reload_doc("siwar_chocolate", "doctype", "client_request_ct")
    frappe.delete_doc_if_exists("Client Request CT", "shipment_type")
    frappe.delete_doc_if_exists("Custom Field", "Client Request CT-shipment_type")   

    frappe.reload_doc("siwar_chocolate", "doctype", "client_request_ct")
    frappe.delete_doc_if_exists("Client Request CT", "supervision_status")
    frappe.delete_doc_if_exists("Custom Field", "Client Request CT-supervision_status")       