// Copyright (c) 2016, Abcgroups and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rekap Export', {
	refresh: function(frm) {
		var me = this;
		if (frm.doc.docstatus == '1' && frm.doc.status != "Closed") {
			cur_frm.add_custom_button(__('Close'), this.close_rekap_export, __("Status"))
		}
		if (frm.doc.docstatus == '1' && frm.doc.status == "Closed") {
			cur_frm.add_custom_button(__('Re-Open'), this.open_rekap_export, __("Status"))
		}
		if(!frm.doc.__islocal && frm.doc.status != "Closed") {
			cur_frm.add_custom_button(__('Sales Invoice'), cur_frm.cscript['Sales Invoice'], __("Make"));
			cur_frm.page.set_inner_btn_group_as_primary(__("Make"));
		}
	}
});
close_rekap_export = function() {
	var doc = cur_frm.doc;
	frappe.ui.form.is_saving = true;
	frappe.call({
		method: "logistics.logistics.doctype.rekap_export.rekap_export.close_rekap_export",
		args: {status: status, name: doc.name},
		callback: function(r){
			cur_frm.reload_doc();
		},
	})
}
open_rekap_export = function() {
	var doc = cur_frm.doc;
	frappe.ui.form.is_saving = true;
	frappe.call({
		method: "logistics.logistics.doctype.rekap_export.rekap_export.open_rekap_export",
		args: {status: status, name: doc.name},
		callback: function(r){
			cur_frm.reload_doc();
		},
	})
}

cur_frm.cscript['Sales Invoice'] = function() {
	frappe.model.open_mapped_doc({
		method: "logistics.logistics.doctype.rekap_export.rekap_export.make_sales_invoice",
		frm: cur_frm
	})
}

cur_frm.set_query("carrier",  function (frm) {
		return {
        filters: {
					'supplier_type': 'Carrier'
        }
		}
});
cur_frm.set_query("vendor_trucking", "items",  function (doc, cdt, cdn) {
	var c_doc= locals[cdt][cdn];
    return {
        filters: {
            'supplier_type': 'Trucking'
        }
    }
});
cur_frm.set_query("template_trucking", "items",  function (doc, cdt, cdn) {
	var c_doc= locals[cdt][cdn];
    return {
        filters: {
            'supplier': c_doc.vendor_trucking,
						'jenis': 'Trucking'
        }
    }
});

cur_frm.cscript.size_cont = function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];
	if (d.size_cont == "-"){
		d.party = flt(d.custom_size)+" "+d.type;
	}else{
		d.party = d.size_cont+""+d.type;
	}
	refresh_field('party', d.name, 'items');
}
cur_frm.cscript.custom_size = cur_frm.cscript.type = cur_frm.cscript.size_cont;

//hitung selisih hari
/*
frappe.ui.form.on("Container List", "gate_in", function(frm, cdt, cdn) {
	var z = locals[cdt][cdn];

	if(z.gate_in && z.gate_out) {
		total_time = frappe.datetime.get_day_diff(z.gate_out, z.gate_in);
		frappe.model.set_value(cdt, cdn, "within_days", total_time);
	}
});
frappe.ui.form.on("Container List", "gate_out", function(frm, cdt, cdn) {
	var z = locals[cdt][cdn];

	if(z.gate_in && z.gate_out) {
		total_time = frappe.datetime.get_day_diff(z.gate_out, z.gate_in);
		frappe.model.set_value(cdt, cdn, "within_days", total_time);
	}
});
*/
