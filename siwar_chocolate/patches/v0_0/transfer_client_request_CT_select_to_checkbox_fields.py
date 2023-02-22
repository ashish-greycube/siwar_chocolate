import frappe

def execute():
  if frappe.db.exists("DocType", "Client Request CT"):
    frappe.reload_doc("siwar_chocolate", "doctype", "client_request_ct")
    
    frappe.db.sql("""UPDATE `tabClient Request CT` SET showroom_crt = 1 where client_request_type = 'عميل عادي R.C'""")
    frappe.db.sql("""UPDATE `tabClient Request CT` SET occasion_section_crt = 1 where client_request_type in ('مناسبه Occasion','Occasion Department','عميل مناسبه Occasion')""")
    frappe.db.sql("""UPDATE `tabClient Request CT` SET customer_service_crt = 1 where client_request_type = 'خدمة العملاء C.S'""")
    frappe.db.sql("""UPDATE `tabClient Request CT` SET in_call_crt = 1 where client_request_type = 'in Call'""")    
    frappe.db.sql("""UPDATE `tabClient Request CT` SET not_confirmed_crt = 1 where client_request_type = 'طلب غير مؤكد ×××Not Confirmed Order×××'""")


    frappe.db.sql("""UPDATE `tabClient Request CT` SET pickup = 1 where shipment_type = 'PickUp'""")    
    frappe.db.sql("""UPDATE `tabClient Request CT` SET delivery = 1 where shipment_type = 'Delivery'""")     
 

    frappe.db.sql("""UPDATE `tabClient Request CT` SET no_supervision = 1 where supervision_status = 'No supervision'""")      
    frappe.db.sql("""UPDATE `tabClient Request CT` SET supervision = 1 where supervision_status = 'with supervision'""")    
  

    frappe.db.sql("""UPDATE `tabClient Request CT` SET 5_to_7_30_pm = 1 where `أوقات_التوصيل` = 'من الساعة 5:00 حتى الساعة 7:30 مساءً' """)      
    frappe.db.sql("""UPDATE `tabClient Request CT` SET 4_pm = 1 where `أوقات_التوصيل` = 'الساعة 4 مساءً' """) 
    frappe.db.sql("""UPDATE `tabClient Request CT` SET 5_pm = 1 where `أوقات_التوصيل` = 'الساعة 5 مساءً' """)  
    # if frappe.db.has_column("Client Request CT", "أوقات_التوصيل"):                 
    #   frappe.db.sql_ddl("ALTER table `tabClient Request CT` DROP COLUMN أوقات_التوصيل")    

    frappe.db.sql("""UPDATE `tabClient Request CT` SET riyadh = 1 where customer_city_cf = 'الرياض Riyadh'""")    
    frappe.db.sql("""UPDATE `tabClient Request CT` SET jadda = 1 where customer_city_cf = 'جدة jadda'""") 
    frappe.db.sql("""UPDATE `tabClient Request CT` SET dammam_city = 1 where customer_city_cf = 'الدمام Dammam'""") 
    frappe.db.sql("""UPDATE `tabClient Request CT` SET al_medina = 1 where customer_city_cf = 'المدينة المنورة Al-Medina'""")    
    # if frappe.db.has_column("Client Request CT", "customer_city_cf"):                 
    #   frappe.db.sql_ddl("ALTER table `tabClient Request CT` DROP COLUMN customer_city_cf")