import frappe
@frappe.whitelist()
def get_price(item_code):
    price_data = frappe.db.sql(f"""SELECT price_list_rate FROM `tabItem Price` WHERE item_name = '{item_code}'""", as_dict=True)[0]
    
    return price_data,item_code

@frappe.whitelist()
def delete_items(unique_id):
    
    delete_item=frappe.db.sql(f"""DELETE FROM `tabSales Order Item` WHERE unique_id='{unique_id}';""");
    
@frappe.whitelist()
def get_item_component_fields(unique_id):
    # Fetch 'Item Component' fields and return as JSON
    item_component_fields = frappe.get_meta('Item Component').fields
    get_data=frappe.db.sql(f"""SELECT * FROM `tabItem Component` WHERE unique_id ='{unique_id}'""", as_dict=True)
    return get_data
    
@frappe.whitelist()
def get_item_code(unique_id):
    item_code=frappe.db.sql(f"""SELECT item_code FROM `tabSales Order Item` WHERE unique_id ='{unique_id}'""", as_dict=True)
    return item_code
       
# def insert_pieces(unique_id,qty):
#     print(qty)
#     update=frappe.db.sql(f"""UPDATE `tabSales Order Item` SET pieces = '{qty}' WHERE unique_id='{unique_id}'""")
#     return update
    

# @frappe.whitelist()
# def set_quantity(pieces):
#     print(pieces)
#     update=frappe.db.sql(f"""UPDATE `tabSales Order Item` SET pieces = '{qty}' WHERE unique_id='{unique_id}'""")