# Copyright (c) 2023, Aquiq and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PostedDatedCheques(Document):
	pass
@frappe.whitelist()
def get_exchange_rate(party):
    currency=frappe.db.get_value('Customer', {'name': party}, 'default_currency')
    sql_query = f"""
        SELECT 
        	exchange_rate
        FROM 
        	`tabCurrency Exchange` 
        WHERE 
        	from_currency = '{currency}'
    """
    exchange_rate = frappe.db.sql(sql_query, as_dict=True)[0]
    return currency,exchange_rate
    
    
    
    
