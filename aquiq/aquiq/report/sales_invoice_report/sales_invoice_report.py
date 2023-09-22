# Copyright (c) 2023, Aquiq and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = get_columns()
    columns = get_columns()
    if filters.get('parent_item_group'):
        data = get_data(filters)
        tree_data = parent(data)
    # elif filters.get('sub_item_group'):
    #     data = get_data(filters)
    #     tree_data = sub(data)
    else:
        data = get_data(filters)
        tree_data = build_tree(data)
    return columns, tree_data


def get_data(filters):
    filter_condition_str, filter_values = build_filter_conditions(filters)
    
    SQL1 = f"""
        SELECT
            ig1.item_group_name AS sub_item_group,
            ig2.item_group_name AS parent_item_group,
            sii.item_name,
            sii.qty,
            sii.rate,
            sii.amount
        FROM 
            `tabItem Group` ig1
        JOIN 
            `tabItem Group` ig2 
        ON 
            ig1.parent_item_group = ig2.item_group_name
        JOIN   
            `tabSales Invoice Item` sii 
        ON 
            ig1.item_group_name = sii.item_group
        WHERE 
            {filter_condition_str}
        ORDER BY 
            ig2.item_group_name, ig1.item_group_name, sii.item_name;
    """

    data = frappe.db.sql(SQL1, filter_values, as_dict=True)
    return data

def build_filter_conditions(filters):
    filter_conditions = []
    filter_values = {}

    if filters.get('item_name'):
        filter_conditions.append("sii.item_name = %(item_name)s")
        filter_values['item_name'] = filters['item_name']
    if filters.get('parent_item_group'):
        filter_conditions.append("ig2.item_group_name = %(parent_item_group)s")
        filter_values['parent_item_group'] = filters['parent_item_group']
    if filters.get('sub_item_group'):
        filter_conditions.append("ig1.item_group_name = %(sub_item_group)s")
        filter_values['sub_item_group'] = filters['sub_item_group']
    if filters.get('amount'):
        filter_conditions.append("sii.amount >= %(amount)s")
        filter_values['amount'] = filters['amount']

    filter_condition_str = " AND ".join(filter_conditions) if filter_conditions else "1=1"

    return filter_condition_str, filter_values


def build_tree(data):
    tree_data = []
    current_parent = None
    current_sub = None
    current_item = None
    level = 0
    amount_sum = 0
    qty_sum = 0
    rate_sum = 0

    for row in data:
        parent_group = row['parent_item_group']
        sub_group = row['sub_item_group']
        item_name = row['item_name']
        qty = row['qty']
        rate = row['rate']
        amount = row['amount']

        if parent_group != current_parent:
            if current_parent is not None:
                tree_data.append({"parent_item_group": "", "sub_item_group": "", "item_name": "Total", "qty": qty_sum, "rate": rate_sum, "amount": amount_sum, "level": level})
                amount_sum = 0
                qty_sum = 0
                rate_sum = 0

            current_parent = parent_group
            current_sub = None
            current_item = None
            level = 0
            tree_data.append({"parent_item_group": parent_group, "sub_item_group": "", "item_name": "", "qty": "", "rate": "", "amount": "", "level": level})

        if sub_group != current_sub:
            current_sub = sub_group
            current_item = None
            level += 1
            tree_data.append({"parent_item_group": "", "sub_item_group": sub_group, "item_name": "", "qty": "", "rate": "", "amount": "", "level": level})

        if item_name != current_item:
            current_item = item_name
            amount_sum += amount
            qty_sum += qty
            rate_sum += rate
            tree_data.append({"parent_item_group": "", "sub_item_group": "", "item_name": item_name, "qty": qty, "rate": rate, "amount": amount, "level": level})

    if current_parent is not None:
        tree_data.append({"parent_item_group": "", "sub_item_group": "", "item_name": "Total", "qty": qty_sum, "rate": rate_sum, "amount": amount_sum, "level": level})

    return tree_data


def parent(data):
    tree_data = []
    current_parent = None
    current_sub = None
    current_item = None
    level = 0
    amount_sum = 0
    rate_sum = 0

    for row in data:
        parent_group = row['parent_item_group']
        sub_group = row['sub_item_group']
        item_name = row['item_name']
        qty = row['qty']
        rate = row['rate']
        amount = row['amount']

        if parent_group != current_parent:
            if current_parent is not None:
                # Insert the total row for amount and rate
                tree_data.append({
                    "parent_item_group": current_parent,
                    "sub_item_group": "",
                    "item_name": "Total",
                    "qty": qty_sum,
                    "rate": rate_sum,
                    "amount": amount_sum,
                    "level": level
                })

            current_parent = parent_group
            current_sub = None
            current_item = None
            level = 0
            amount_sum = 0
            rate_sum = 0
            qty_sum=0

        if parent_group == 'Total':
            continue

        if sub_group != current_sub:
            current_sub = sub_group
            current_item = None
            level += 1

        if item_name != current_item:
            current_item = item_name
            amount_sum += amount
            rate_sum += rate
            qty_sum +=qty
            

    if current_parent is not None:
        tree_data.append({
            "parent_item_group": current_parent,
            "sub_item_group": "",
            "item_name": "Total",
            "qty": qty_sum,
            "rate": rate_sum,
            "amount": amount_sum,
            "level": level
        })

    return tree_data

# def sub(data):
#     tree_data = []
#     current_parent = None
#     current_sub = None
#     current_item = None
#     level = 0
#     amount_sum = 0
#     rate_sum = 0

#     for row in data:
#         parent_group = row['parent_item_group']
#         sub_group = row['sub_item_group']
#         item_name = row['item_name']
#         qty = row['qty']
#         rate = row['rate']
#         amount = row['amount']

#         if parent_group != current_parent:
#             if current_parent is not None:
#                 # Insert the total row for amount and rate
#                 tree_data.append({
#                     "parent_item_group": current_parent,
#                     "sub_item_group": "",
#                     "item_name": "Total",
#                     "qty": "",
#                     "rate": rate_sum,
#                     "amount": amount_sum,
#                     "level": level
#                 })

#             current_parent = parent_group
#             current_sub = None
#             current_item = None
#             level = 0
#             amount_sum = 0
#             rate_sum = 0

#         if parent_group == 'Total':
#             # If parent_group is 'Total', skip the data rows
#             continue

#         if sub_group != current_sub:
#             current_sub = sub_group
#             current_item = None
#             level += 1

#         if item_name != current_item:
#             current_item = item_name
#             amount_sum += amount
#             rate_sum += rate

#     if current_parent is not None:
#         # Insert the total row for the last parent group
#         tree_data.append({
#             "parent_item_group": current_parent,
#             "sub_item_group": "",
#             "item_name": "Total",
#             "qty": "",
#             "rate": rate_sum,
#             "amount": amount_sum,
#             "level": level
#         })

#     return tree_data

def get_columns():
    return [
        {"fieldname": "parent_item_group", "label": "Item Group", "fieldtype": "Link", "options": "Item Group", "width": 170, "align": "left"},
        {"fieldname": "sub_item_group", "label": "Sub Item Group", "fieldtype": "Link", "options": "Item Group", "width": 170, "align": "left"},
        {"fieldname": "item_name", "label": "Item", "fieldtype": "Link", "options": "Item", "width": 170, "align": "left"},
        {"fieldname": "qty", "label": "Quality", "fieldtype": "Data", "width": 200, "align": "left"},
        {"fieldname": "rate", "label": "Rate", "fieldtype": "Float", "options": "", "width": 140, "align": "left", "precision": 1},
        {"fieldname": "amount", "label": "Amount", "fieldtype": "Float", "options": "", "width": 150, "align": "left"}
    ]