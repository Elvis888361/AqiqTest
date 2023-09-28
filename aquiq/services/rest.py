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
    item_component_fields = frappe.get_meta('Item Component').fields
    get_data=frappe.db.sql(f"""SELECT * FROM `tabItem Component` WHERE unique_id ='{unique_id}'""", as_dict=True)
    return get_data
@frappe.whitelist()
def get_item_code(unique_id):
    item_code=frappe.db.sql(f"""SELECT item_code FROM `tabSales Order Item` WHERE unique_id ='{unique_id}'""", as_dict=True)
    return item_code
@frappe.whitelist()
def get_piece(order_name,purchase_order):
    custom_exists = frappe.db.get_value("Purchase Order Item", {"name": order_name},'custom_received_pieces')
    if custom_exists==None:
        pieces = frappe.db.get_value('Purchase Order Item', {'name': order_name}, 'custom_pieces')
        pieces = int(pieces)
        return order_name, pieces
    else:
        pieces = frappe.db.get_value('Purchase Order Item', {'name': order_name}, 'custom_pieces')
        custom_remainer_pieces = frappe.db.get_value("Purchase Order Item", {"name": order_name},'custom_remainer_pieces')
        return order_name, custom_remainer_pieces
@frappe.whitelist()
def get_piecess(order_name,pieces):
    custom_received_pieces = frappe.db.get_value("Purchase Order Item", {"name": order_name},'custom_received_pieces')
    parent = frappe.db.get_value("Purchase Order Item", {"name": order_name},'parent')
    piecesmodify = frappe.db.get_value('Purchase Order Item', {'name': order_name}, 'custom_pieces')
    if custom_received_pieces==None:
        calculation=0+int(pieces)
        remainer=int(piecesmodify)-calculation
        frappe.db.sql(f"""UPDATE `tabPurchase Order Item` SET custom_received_pieces='{calculation}' WHERE name= '{order_name}';""")
        frappe.db.sql(f"""UPDATE `tabPurchase Order Item` SET custom_remainer_pieces='{remainer}' WHERE name= '{order_name}';""")
        doc = frappe.get_doc("Purchase Order", parent)
        doc.reload()
    else:
        calculation=int(custom_received_pieces)+int(pieces)
        remainer=int(piecesmodify)-calculation
        frappe.db.sql(f"""UPDATE `tabPurchase Order Item` SET custom_received_pieces='{calculation}' WHERE name= '{order_name}';""")
        frappe.db.sql(f"""UPDATE `tabPurchase Order Item` SET custom_remainer_pieces='{remainer}' WHERE name= '{order_name}';""")
        doc = frappe.get_doc("Purchase Order", parent)
        doc.reload()
    
@frappe.whitelist()
def reload_target_doctype(order_name):
    parent = frappe.db.get_value("Purchase Order Item", {"name": order_name},'parent')
    doc = frappe.get_doc("Purchase Order", parent)
    doc.reload()
    frappe.reload_doc("Purchase Order", parent)