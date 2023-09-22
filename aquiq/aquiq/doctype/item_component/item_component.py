# Copyright (c) 2023, Aquiq and contributors
# For license information, please see license.txt

from bs4 import ResultSet
import frappe
from frappe.model.document import Document

class ItemComponent(Document):
	pass
@frappe.whitelist()
def get_child_data(item_codes):
    result = []

    name = frappe.db.get_value('Item', {'item_code': item_codes}, 'name')

    if name:
        data = frappe.db.sql(f"""SELECT * FROM `tabItem Component` WHERE parent ='{name}'""", as_dict=True)
        
        for item in data:
            item_code = item['component_name']

            price_data = frappe.db.sql(f"""SELECT price_list_rate FROM `tabItem Price` WHERE item_name = '{item_code}'""", as_dict=True)
            
            result.append({
                'data': item,
                'price_data': price_data
            })
    return result
@frappe.whitelist()
def get_child_data_after(item_codes):
    results=[]
    name = frappe.db.get_value('Item', {'item_code': item_codes}, 'name')

    if name:
        data = frappe.db.sql(f"""SELECT * FROM `tabItem Component` WHERE parent ='{name}'""", as_dict=True)
        
        for item in data:
            item_code = item['component_name']

            price_data = frappe.db.sql(f"""SELECT price_list_rate FROM `tabItem Price` WHERE item_name = '{item_code}'""", as_dict=True)
            
            results.append({
                'data': item,
                'price_data': price_data
            })
    return results