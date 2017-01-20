// Copyright (c) 2016, Abcgroups and contributors
// For license information, please see license.txt

frappe.ui.form.on('Template Biaya', {
	refresh: function(frm) {

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
        filters: {
            'root_type': 'Expense',
						'is_group': 0
        }
	}
});
cur_frm.set_query("income", "item_biaya",  function (doc, cdt, cdn) {
	var c_doc= locals[cdt][cdn];
    return {
        filters: {
            'root_type': 'Income',
						'is_group': 0
        }
	}
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
