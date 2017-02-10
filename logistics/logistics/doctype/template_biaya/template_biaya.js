// Copyright (c) 2016, Abcgroups and contributors
// For license information, please see license.txt

frappe.ui.form.on('Template Biaya', {
	refresh: function(frm) {

	}
});
cur_frm.set_query("supplier",  function (frm) {
		return {
        filters: [
            ['supplier_type', '=', 'Trucking']
        ]
		}
});
cur_frm.set_query("item_code", "item_biaya",  function (doc, cdt, cdn) {
	var c_doc= locals[cdt][cdn];
    return {
        filters: {
            'item_group': 'Services'
        }
    }
});
cur_frm.set_query("cost_center", "item_biaya",  function (doc, cdt, cdn) {
	var c_doc= locals[cdt][cdn];
    return {
        filters: [
						['is_group', '=', 0]
				]
    }
});
cur_frm.set_query("expense", "item_biaya",  function (doc, cdt, cdn) {
	var c_doc= locals[cdt][cdn];
    return {
			filters: [
					['account_type', '=', 'Expense Account'],
					['is_group', '=', 0]
			]
	}
});
cur_frm.set_query("income", "item_biaya",  function (doc, cdt, cdn) {
	var c_doc= locals[cdt][cdn];
    return {
			filters: [
					['account_type', '=', 'Income Account'],
					['is_group', '=', 0]
			]
	}
});
frappe.ui.form.on("Template Biaya", "jenis", function(frm, cdt, cdn) {
	frappe.model.set_value(cdt, cdn, "customer_name", "");
	if (frm.doc.jenis != "Trucking"){
		frappe.model.set_value(cdt, cdn, "supplier", "");
    frappe.model.set_value(cdt, cdn, "dari", "");
		frappe.model.set_value(cdt, cdn, "tujuan", "");
	}
});
frappe.ui.form.on("Template Biaya Item", "item_code", function(frm, cdt, cdn) {
    row = locals[cdt][cdn];
    frappe.call({
        method: "frappe.client.get",
        args: {
            doctype: "Item",
						name: row.item_code
        },
        callback: function (data) {
            frappe.model.set_value(cdt, cdn, "expense", data.message.expense_account);
						frappe.model.set_value(cdt, cdn, "income", data.message.income_account);
						frappe.model.set_value(cdt, cdn, "qty", "1");
						frappe.model.set_value(cdt, cdn, "cost_center", data.message.buying_cost_center);
				}
    })
});

cur_frm.cscript.qty = function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];
		d.buying_amount = flt(d.qty) * flt(d.buying_rate);
		d.selling_amount = flt(d.qty) * flt(d.selling_rate);

		refresh_field('buying_amount', d.name, 'item_biaya');
		refresh_field('selling_amount', d.name, 'item_biaya');
}
cur_frm.cscript.buying_rate = cur_frm.cscript.qty;
cur_frm.cscript.selling_rate = cur_frm.cscript.qty;

//hitung total buying
var calculate_total_buying = function(frm) {
    var total_buying = frappe.utils.sum(
        (frm.doc.item_biaya || []).map(function(i) {
			return (i.qty * i.buying_rate);
		})
    );
    frm.set_value("total_buying", total_buying);
}
frappe.ui.form.on("Template Biaya Item", "buying_amount", function(frm, cdt, cdn) {
    calculate_total_buying(frm, cdt, cdn);
})
frappe.ui.form.on("Template Biaya Item", "qty", function(frm, cdt, cdn) {
    calculate_total_buying(frm, cdt, cdn);
})
frappe.ui.form.on("Template Biaya Item", "buying_rate", function(frm, cdt, cdn) {
    calculate_total_buying(frm, cdt, cdn);
})

//hitung total selling
var calculate_total_selling = function(frm) {
    var total_selling = frappe.utils.sum(
        (frm.doc.item_biaya || []).map(function(i) {
			return (i.qty * i.selling_rate);
		})
    );
    frm.set_value("total_selling", total_selling);
}
frappe.ui.form.on("Template Biaya Item", "selling_amount", function(frm, cdt, cdn) {
    calculate_total_selling(frm, cdt, cdn);
})
frappe.ui.form.on("Template Biaya Item", "qty", function(frm, cdt, cdn) {
    calculate_total_selling(frm, cdt, cdn);
})
frappe.ui.form.on("Template Biaya Item", "selling_rate", function(frm, cdt, cdn) {
    calculate_total_selling(frm, cdt, cdn);
})
//validate
frappe.ui.form.on("Template Biaya", "validate", function(frm) {
	if (frm.doc.jenis == "Trucking" && (!frm.doc.supplier || !frm.doc.dari || !frm.doc.tujuan)) {
		msgprint(__("Vendor, Dari dan Tujuan wajib diisi"));
		validated = false;
	}else{
		if(frm.doc.jenis != "Trucking" && !frm.doc.customer_name){
			msgprint(__("Customer wajib diisi"));
			validated = false;
		}
	}
});
