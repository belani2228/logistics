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
cur_frm.cscript.type = function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];
	if (d.type == "CBM" || d.type == "KGS"){
		d.party = flt(d.custom_size)+" "+d.type;
	}else{
		d.party = d.size_cont+""+d.type;
	}
	refresh_field('party', d.name, 'items');
}
cur_frm.cscript.custom_size = cur_frm.cscript.size_cont = cur_frm.cscript.type;

var date_for_series = function(frm){
    var tgl = frm.doc.date;
    var thn = tgl.substring(0,4);
    frm.set_value("period", thn);
}
frappe.ui.form.on("Rekap Export", "validate", function(frm) {
	date_for_series(frm);
})

//MULIA
cur_frm.cscript.size_cont_empty = function(doc, cdt, cdn) {
	var e = locals[cdt][cdn];
	if (e.size_cont_empty == "-"){
		e.party_empty = flt(e.custom_size)+" "+e.type_empty;
	}else{
		e.party_empty = e.size_cont_empty+""+e.type_empty;
	}
	refresh_field('party_empty', e.name, 'empty_items');
}
cur_frm.cscript.custom_size = cur_frm.cscript.type_empty = cur_frm.cscript.size_cont_empty;


frappe.ui.form.on("Rekap Export", "get_items_from_empty_container", function(frm) {
	if(!cur_frm.doc.__islocal){
			erpnext.utils.map_current_doc({
				method: "logistics.logistics.doctype.rekap_export.rekap_export.get_items_from_empty_container",
				source_name: cur_frm.doc.name,
			});
	}else{
		msgprint("You must save this document")
	}
	})

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
