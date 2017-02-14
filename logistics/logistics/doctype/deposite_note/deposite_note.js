// Copyright (c) 2016, Abcgroups and contributors
// For license information, please see license.txt

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
			//cur_frm.add_custom_button(__('Journal Voucher'), cur_frm.cscript['Journal Voucher'], __("Make"));
			cur_frm.page.set_inner_btn_group_as_primary(__("Make"));
		}
	},
	get_items_from_template: function(frm) {
		return frappe.call({
			method: "get_template_item",
			doc: frm.doc,
			callback: function(r, rt) {
				frm.refresh()
			}
		});
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
frappe.ui.form.on("Deposite Note", "no_job", function(frm, cdt, cdn) {
    frappe.call({
        method: "frappe.client.get",
        args: {
            doctype: cur_frm.doc.jenis_rekap,
						name: cur_frm.doc.no_job
        },
        callback: function (data) {
						frappe.model.set_value(cdt, cdn, "aju", data.message.aju);
						frappe.model.set_value(cdt, cdn, "no_bl", data.message.bl_number);
            frappe.model.set_value(cdt, cdn, "qty", data.message.qty);

				}
    })
});
frappe.ui.form.on("Deposite Note", "no_job", function(frm, cdt, cdn) {
    frappe.call({
        method: "frappe.client.get",
        args: {
            doctype: cur_frm.doc.jenis_rekap,
						name: cur_frm.doc.no_job
        },
        callback: function (data) {
					if(cur_frm.doc.jenis_rekap == "Rekap Import"){
						frappe.model.set_value(cdt, cdn, "customer", data.message.customer);
						frappe.model.set_value(cdt, cdn, "carrier", data.message.carrier);
						frappe.model.set_value(cdt, cdn, "size_cont", data.message.size_cont);
					}else{
						frappe.model.set_value(cdt, cdn, "customer", data.message.customer_name);
						frappe.model.set_value(cdt, cdn, "carrier", data.message.carrier);
						frappe.model.set_value(cdt, cdn, "size_cont", data.message.size_cont);
					}
				}
    })
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
			filters: [
					['account_type', 'in', 'Expense Account, Cost of Goods Sold'],
					['is_group', '=', 0]
			]
	}
});

cur_frm.cscript.qty = function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];
		d.amount = flt(d.qty) * flt(d.rate);

		refresh_field('amount', d.name, 'items');
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
frappe.ui.form.on("Deposite Note Item", "amount", function(frm, cdt, cdn) {
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

var kembalian = function(frm) {
	var sisa_kembalian = flt(frm.doc.difference) - flt(frm.doc.pengembalian_kasbon);
	frm.set_value("sisa", sisa_kembalian);
}
frappe.ui.form.on("Deposite Note", "difference", function(frm) {
	kembalian(frm);
})
frappe.ui.form.on("Deposite Note", "pengembalian_kasbon", function(frm) {
	kembalian(frm);
})

//test ubah currency
cur_frm.cscript.onload = function(doc, cdt, cdn) {
	cur_frm.fields_dict.deposite_amount.set_label('Deposite Amount ('+doc.currency+')');
	cur_frm.fields_dict.difference.set_label('Difference (' + doc.currency + ')');
	cur_frm.fields_dict.total_claim.set_label('Total Claim (' + doc.currency + ')');
	cur_frm.fields_dict.pengembalian_kasbon.set_label('Pengembalian Kasbon (' + doc.currency + ')');
	cur_frm.fields_dict.sisa.set_label('Sisa (' + doc.currency + ')');
}
frappe.ui.form.on("Deposite Note", "currency", function(frm) {
	frappe.call({
		"method": "frappe.client.get",
		args: {
			doctype: "Currency",
			name: cur_frm.doc.currency
		},
		callback: function (data) {
			cur_frm.fields_dict.deposite_amount.set_label('Deposite Amount ('+data.message.name+')');
			cur_frm.fields_dict.difference.set_label('Difference ('+data.message.name+')');
			cur_frm.fields_dict.total_claim.set_label('Total Claim ('+data.message.name+')');
		}
	})
})
/*
frappe.ui.form.on("Deposite Note", "onload", function(frm) {
	$('input[data-fieldtype="Currency"]').css("text-align","right")
});
*/
/*
frappe.ui.form.on("Deposite Note", "currency", function(frm, cdt, cdn) {
	frappe.call({
		"method": "frappe.client.get",
		args: {
			doctype: "Currency Exchange",
			filters:{
				from_currency: cur_frm.doc.currency
			}
		},
		callback: function (data) {
				frappe.model.set_value(cdt, cdn, "conversion_rate", data.message.exchange_rate);
		}
	})
})
*/
