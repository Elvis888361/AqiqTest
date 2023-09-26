// Copyright (c) 2023, Aquiq and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Invoice Report"] = {
	"filters": [
		{
		  fieldname: "get_all_main_item",
		  label: ("Get All Main Item"),
		  fieldtype: "Button",
		  width: 100,
		  reqd: 0,
		  onclick: function() {
                // Your custom code to handle the button click
                // For example, you can display an alert message
                frappe.msgprint("Button clicked!");
            }
		},
		{
		  fieldname: "parent_item_group",
		  label: ("Item Group"),
		  fieldtype: "Link",
		  options: "Item Group",
		  width: 100,
		  reqd: 0,
		},
		{
			fieldname: "sub_item_group",
			label: ("Sub Item Group"),
			fieldtype: "Link",
			options: "Item Group",
			width: 100,
			reqd: 0,
		  },		
		
	 
	  ]
};
