// Copyright (c) 2016, Abcgroups and contributors
// For license information, please see license.txt
// Pake bahasa indonesia saja jika mau komentar

frappe.ui.form.on('Deposite Note', {
	refresh: function(frm) {
		var me = this;
		calculate_total_claim(frm);
		/*

		if(frm.doc.docstatus==1) {
			cur_frm.add_custom_button(__('Make Purchase Invoice'), cur_frm.cscript['Purchase Invoice'], "icon-exclamation", "btn-default");
		};
		*/
		if(frm.doc.docstatus==1) {
			cur_frm.add_custom_button(__('Purchase Invoice'), cur_frm.cscript['Purchase Invoice'], __("Make"));
			cur_frm.add_custom_button(__('Journal Voucher'), cur_frm.cscript['Journal Voucher'], __("Make"));
			cur_frm.page.set_inner_btn_group_as_primary(__("Make"));
		}
	},
});
cur_frm.cscript['Purchase Invoice'] = function() {
	frappe.model.open_mapped_doc({
		method: "logistics.logistics.doctype.deposite_note.deposite_note.make_purchase_invoice",
		frm: cur_frm
	})
}

cur_frm.set_query("account_paid_to",  function (frm) {
		return {
        filters: [
            ['root_type', '=', 'Asset'],
						['account_type', 'in', 'Bank, Cash'],
						['is_group', '=', 0]
        ]
		}
});
cur_frm.add_fetch("deposite_amount", "difference")
cur_frm.set_query("item_code", "items",  function (doc, cdt, cdn) {
	var c_doc= locals[cdt][cdn];
    return {
        filters: {
            'item_group': 'Services'
        }
    }
});
cur_frm.set_query("cost_center", "items",  function (doc, cdt, cdn) {
	var c_doc= locals[cdt][cdn];
    return {
        filters: [
						['is_group', '=', 0]
				]
    }
});
frappe.ui.form.on("Deposite Note Item", "item_code", function(frm, cdt, cdn) {
    row = locals[cdt][cdn];
    frappe.call({
        method: "frappe.client.get",
        args: {
            doctype: "Item",
						name: row.item_code
        },
        callback: function (data) {
            frappe.model.set_value(cdt, cdn, "expense_account", data.message.expense_account);
						frappe.model.set_value(cdt, cdn, "qty", "1");
						frappe.model.set_value(cdt, cdn, "cost_center", data.message.buying_cost_center);
				}
    })
});
cur_frm.set_query("expense_account", "items",  function (doc, cdt, cdn) {
	var c_doc= locals[cdt][cdn];
    return {
        filters: {
            'root_type': 'Expense',
			'is_group': 0
        }
	}
});

cur_frm.cscript.qty = function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];
		d.claim_amount = flt(d.qty) * flt(d.rate);

		refresh_field('claim_amount', d.name, 'items');
}
cur_frm.cscript.rate = cur_frm.cscript.qty;

var calculate_total_claim = function(frm) {
    var total_claim = frappe.utils.sum(
        (frm.doc.items || []).map(function(i) {
			return (i.qty * i.rate);
		})
    );
    frm.set_value("total_claim", total_claim);
}
frappe.ui.form.on("Deposite Note Item", "claim_amount", function(frm, cdt, cdn) {
    calculate_total_claim(frm, cdt, cdn);
})
frappe.ui.form.on("Deposite Note Item", "qty", function(frm, cdt, cdn) {
    calculate_total_claim(frm, cdt, cdn);
})
frappe.ui.form.on("Deposite Note Item", "rate", function(frm, cdt, cdn) {
    calculate_total_claim(frm, cdt, cdn);
})

var calculate_sisa = function(frm) {
	var sisa = flt(frm.doc.deposite_amount) - flt(frm.doc.total_claim);
	frm.set_value("difference", sisa);
}
frappe.ui.form.on("Deposite Note", "deposite_amount", function(frm) {
	calculate_sisa(frm);
})
frappe.ui.form.on("Deposite Note", "total_claim", function(frm) {
	calculate_sisa(frm);
})
