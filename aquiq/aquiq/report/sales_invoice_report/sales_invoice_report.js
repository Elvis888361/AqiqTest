// Copyright (c) 2023, Aquiq and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Invoice Report"] = {
	"filters": [
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
		// {
		//   fieldname: "item_name",
		//   label: ("Item"),
		//   fieldtype: "Link",
		//   options: "Item",
		//   width: 100,
		//   reqd: 0
		// //   "get_query": function() {
		// // 	return {
		// // 	  "filters": {
		// // 		"item_group": ["=", "Waste Fraction"]
		// // 	  }
		// // 	};
		// //   }
		// },
	 
	  ]
};
