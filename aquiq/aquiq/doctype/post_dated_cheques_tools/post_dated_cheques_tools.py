# Copyright (c) 2023, Aquiq and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import get_doc

class PostDatedChequesTools(Document):
	pass

@frappe.whitelist()
def fetch_data(fromDate,toDate,company,cost_center,department):
    sql_query = f"""
        SELECT 
        	* 
        FROM 
        	`tabPosted Dated Cheques` 
        WHERE 
        	pdc_status = 'Pending' 
        AND 
        	reference_date >= '{fromDate}' 
        AND 
        	reference_date <= '{toDate}'
        AND 
        	company = '{company}'
        AND 
        	cost_center = '{cost_center}'
        AND 
        	department = '{department}'
    """
    datas = frappe.db.sql(sql_query, as_dict=True)
    return datas
@frappe.whitelist()
def automate_data(name,bank):
    filters = {
        'doctype': 'Posted Dated Cheques',
        'name': name
    }
    doc = frappe.get_doc(filters)
    if doc:
        doc.reload()
        doc.pdc_status = "Payment Entry Created"
        doc.save()
        sql_query=f"""
            SELECT 
                * 
            FROM 
                `tabPosted Dated Cheques` 
            WHERE 
                name='{name}'
        """
        datas=frappe.db.sql(sql_query,as_dict=True)
        for data in datas:
            insert_payment_entry = frappe.get_doc({
                "doctype": "Payment Entry",
                "payment_type": data.get('payment_type'),
                "posting_date": data.get('posting_date'),
                "company": data.get('company'),
                "mode_of_payment": data.get('mode_of_payment'),
                "party_type": data.get('party_type'),
                "party": data.get('party'),
                "bank_account": bank,
                "party_balance": data.get('party_balance'),
                "paid_from_account_currency": data.get('paid_from_account_currency'),
                "paid_from_account_balance": data.get('paid_from_account_balance'),
                "project": data.get('project'),
                "paid_amount":data.get('amount'),
                "received_amount":data.get('amount'),
                "target_exchange_rate":data.get('target_exchange_rate'),
                "paid_to":"Cash - AS",
                "paid_to_account_currency":data.get('currency'),
                "reference_no":data.get('reference_no'),
                "reference_no":data.get('reference_date'),
                "cost_center":data.get("division")
            })
            insert_payment_entry.insert(ignore_permissions=True)
        
        frappe.db.commit()
    else:
        print("Document not found or does not meet the filter criteria")

