import frappe
from frappe.utils import flt

def execute():
    log_pe_with_issue=[]
    client_request_list = frappe.db.get_all('Client Request CT',
                                            filters = {'client_request_date' : ['>=', '2024-01-01']},
                                            fields = ['name','final_total','outstanding_amount'],
                                            order_by = 'creation')
    for doc in client_request_list:
        client_request_ct = doc.name
        final_total = doc.final_total
        # fetch connected PE for CR
        pe_list = frappe.db.get_all('Payment Entry',filters = {
            'client_request_ct': ['=' , client_request_ct],
            'docstatus':1},
            fields = ['name'],
            order_by  = 'creation')
        
        if len(pe_list)>0:
            to_be_allocated = flt(doc.final_total,2)
            for pe in pe_list:
                pe_doc=frappe.get_doc('Payment Entry',pe.name)
                row = pe_doc.append('cr_reference_payment_ct',{})
                row.reference_client_request_ct = client_request_ct
                if doc.outstanding_amount<0:
                    log_pe_with_issue.append({'pe':pe.name,'cr':client_request_ct})
                    break
                row.final_total = flt(final_total,2)
                row.to_be_paid = flt(to_be_allocated,2)
                row.allocated_amount = flt(pe_doc.paid_amount,2)
                row.outstanding_amount = flt((row.to_be_paid - row.allocated_amount),2)
                # pe_doc.flags.ignore_validate = True
                # pe_doc.flags.ignore_validate_update_after_submit = True
                pe_doc.save(ignore_permissions=True)
                frappe.db.set_value('Payment Entry',pe_doc.name,'client_request_ct',None)
                to_be_allocated = flt((to_be_allocated - row.allocated_amount),2)
	
    frappe.log_error(message=log_pe_with_issue, title="Error in migration of CR data")
    print("Add new row in exsiting payment entry's child table !! ")