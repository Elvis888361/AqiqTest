// Copyright (c) 2023, Aquiq and contributors
// For license information, please see license.txt

frappe.ui.form.on('Posted Dated Cheques', {
	refresh: function(frm) {
        if (frm.doc.pdc_status === 'Pending') {
            frm.page.set_indicator(__('Pending'), 'orange');
        }else if(frm.doc.pdc_status==='Payment Entry Created'){
			frm.page.set_indicator(__('Payment Entry Created'), 'blue');
		}else if(frm.doc.pdc_status==='Payment Entry Submitted'){
			frm.page.set_indicator(__('Payment Entry Submitted'), 'blue');
		}else if(frm.doc.pdc_status==='Cancelled'){
			frm.page.set_indicator(__('Cancelled'), 'blue');
		}else{
			frm.page.set_indicator(__('Draft'), 'blue');
		}
    },
	amount:function(frm){
		let amount=frm.doc.amount;
		let exchange_rate=frm.doc.target_exchange_rate;
		let sum=amount*exchange_rate;
		frm.set_value("base_amount",sum);
	},
	party:function(frm){
		frappe.call({
			method: 'aquiq.aquiq.doctype.posted_dated_cheques.posted_dated_cheques.get_exchange_rate',
			args: {
				'party':frm.doc.party
			},
			callback: function(r) {
				console.log(r.message)
				frm.set_value("currency",r.message[0])
				frm.set_value("target_exchange_rate",r.message[1].exchange_rate)
				frm.set_df_property("amount", "read_only", "0");
			}
		});
		
	},
	validate:function(frm){
		frm.set_value("pdc_status","Pending");
	}
});
