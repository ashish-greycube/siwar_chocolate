import frappe
# make below fields via Edit Doctype and remove them from Custom Fields
def execute():
  if frappe.db.exists("DocType", "Client Request CT Item"):
    frappe.reload_doc("siwar_chocolate", "doctype", "client_request_ct_item")

    frappe.delete_doc_if_exists("Custom Field", "Client Request CT Item-description")  
    frappe.delete_doc_if_exists("Custom Field", "Client Request CT Item-remarks")

def execute():
  if frappe.db.exists("DocType", "Client Request CT"):
    frappe.reload_doc("siwar_chocolate", "doctype", "client_request_ct")

    frappe.delete_doc_if_exists("Custom Field", "Client Request CT-ملاحظات")    
    frappe.delete_doc_if_exists("Custom Field", "Client Request CT-column_break_21") 
    frappe.delete_doc_if_exists("Custom Field", "Client Request CT-section_break_9") 
    frappe.delete_doc_if_exists("Custom Field", "Client Request CT-صواني_تابعه_للعميل") 
    frappe.delete_doc_if_exists("Custom Field", "Client Request CT-صواني_vip") 
    frappe.delete_doc_if_exists("Custom Field", "Client Request CT-صواني_المالح") 
    frappe.delete_doc_if_exists("Custom Field", "Client Request CT-صواني_تشوكلت") 
    frappe.delete_doc_if_exists("Custom Field", "Client Request CT-phone_no2")      
    frappe.delete_doc_if_exists("Custom Field", "Client Request CT-أوقات_التوصيل") 
    frappe.delete_doc_if_exists("Custom Field", "Client Request CT-customer_district_cf") 
    frappe.delete_doc_if_exists("Custom Field", "Client Request CT-customer_city_cf")     
    frappe.delete_doc_if_exists("Custom Field", "Client Request CT-supervision_status")  