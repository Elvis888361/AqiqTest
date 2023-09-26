// Copyright (c) 2023, Aquiq and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gmail Contacts', {
	// refresh: function(frm) {

	// }
	
	get_contacts:function(frm){
		frappe.call({
			method: 'aquiq.aquiq.doctype.gmail_contacts.gmail_contacts.get_contact',
			args: {
				
			},
			callback: function(r) {
			
			}
		});
		
	}
});
