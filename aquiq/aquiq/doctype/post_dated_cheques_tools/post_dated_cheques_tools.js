// Copyright (c) 2023, Aquiq and contributors
// For license information, please see license.txt

frappe.ui.form.on('Post Dated Cheques Tools', {
	// refresh: function(frm) {

	// }
	get_posted_dated_cheques:function(frm){
		var parentDocType = 'Postes Dated Cheques';
		var fromDate=frm.doc.from_date;
		var toDate=frm.doc.to_date;
		var company=frm.doc.company;
		var cost_center=frm.doc.cost_center;
		var department=frm.doc.department;
		frappe.call({
			method: 'aquiq.aquiq.doctype.post_dated_cheques_tools.post_dated_cheques_tools.fetch_data',
			args: {
				"fromDate":fromDate,
				"toDate":toDate,
				"company":company,
				"cost_center":cost_center,
				"department":department
			},
			callback: function(r) {
				if (r.message) {
					var data = r.message;
					var childTableFieldname = 'details';
					frm.doc[childTableFieldname] = [];
					data.forEach(function(item) {
						var childRow = frappe.model.add_child(frm.doc, 'Post Cheque Detail', childTableFieldname);
						childRow.posted_dated_cheques = item.name;
						childRow.company = item.company;
						childRow.cost_center=item.cost_center;
						childRow.department=item.department;
						childRow.project=item.project;
						childRow.posting_date=item.posting_date;
						childRow.mode_of_payment=item.mode_of_payment;
						childRow.payment_type=item.payment_type;
						childRow.payment_type=item.payment_type;
						childRow.reference_no=item.reference_no;
						childRow.reference_date=item.reference_date;
						childRow.party_type=item.party_type;
						childRow.party=item.party;
						childRow.currency=item.currency;
						childRow.amount=item.amount;
						childRow.company_currency=item.currency;
					});
					frm.refresh_field(childTableFieldname);
				}
			}
		});
	},
	apply_bank: function (frm) {
		var bankAccount = frm.doc.default_bank_account;
		var childTableFieldname = 'details';
		var childTable = frm.fields_dict[childTableFieldname].grid;
		var selectedRows = childTable.get_selected_children();

		if (selectedRows && selectedRows.length > 0) {
			for (var i = 0; i < selectedRows.length; i++) {
				selectedRows[i].bank_account = bankAccount;
			}
			childTable.refresh();
		} else {
			frappe.msgprint(__('No rows are selected.'));
		}
	},
	on_submit:function(frm){
		var childTableFieldname = 'details';
		if (frm.doc[childTableFieldname] && frm.doc[childTableFieldname].length > 0) {
			frm.doc[childTableFieldname].forEach(function(childRow) {
				var name=childRow.posted_dated_cheques;
				var bank=childRow.bank_account
				if (childRow.bank_account) {
					frappe.call({
						method: 'aquiq.aquiq.doctype.post_dated_cheques_tools.post_dated_cheques_tools.automate_data',
						args: {
							'name': name,
							'bank':bank
						},
						callback: function(r) {
						}
					});
				} else {
					frappe.msgprint("Bank Account is missing in one or more rows.");
				}			
			});
		}
	},
	validate: function (frm) {
		var childTableFieldname = 'details';
		var childTable = frm.doc[childTableFieldname];
		if (childTable && childTable.length > 0) {
			var rowsToRemove = [];
			for (var i = childTable.length - 1; i >= 0; i--) {
				var row = childTable[i];
				var bankAccountValue = row.bank_account;
				if (!bankAccountValue) {
					rowsToRemove.push(i);
				}
			}
			for (var j = 0; j < rowsToRemove.length; j++) {
				childTable.splice(rowsToRemove[j], 1);
			}
			frm.refresh_field(childTableFieldname);
		}
	}  
});
