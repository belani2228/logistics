// Copyright (c) 2016, Abcgroups and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rekap Import', {
	refresh: function(frm) {
		var me = this;
		if (frm.doc.docstatus == '1' && frm.doc.status != "Closed") {
			cur_frm.add_custom_button(__('Close'), this.close_rekap_import, __("Status"))
		}
		if (frm.doc.docstatus == '1' && frm.doc.status == "Closed") {
			cur_frm.add_custom_button(__('Re-Open'), this.open_rekap_import, __("Status"))
		}
		if(!frm.doc.__islocal && frm.doc.status != "Closed") {
			cur_frm.add_custom_button(__('Sales Invoice'), cur_frm.cscript['Sales Invoice'], __("Make"));
			cur_frm.page.set_inner_btn_group_as_primary(__("Make"));
		}
	},
});
close_rekap_import = function() {
	var doc = cur_frm.doc;
	frappe.ui.form.is_saving = true;
	frappe.call({
		method: "logistics.logistics.doctype.rekap_import.rekap_import.close_rekap_import",
		args: {status: status, name: doc.name},
		callback: function(r){
			cur_frm.reload_doc();
		},
	})
}
open_rekap_import = function() {
	var doc = cur_frm.doc;
	frappe.ui.form.is_saving = true;
	frappe.call({
		method: "logistics.logistics.doctype.rekap_import.rekap_import.open_rekap_import",
		args: {status: status, name: doc.name},
		callback: function(r){
			cur_frm.reload_doc();
		},
	})
}

cur_frm.cscript['Sales Invoice'] = function() {
	frappe.model.open_mapped_doc({
		method: "logistics.logistics.doctype.rekap_import.rekap_import.make_sales_invoice",
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
var date_for_series = function(frm){
    var tgl = frm.doc.date;
    var thn = tgl.substring(0,4);
    frm.set_value("period", thn);
}
frappe.ui.form.on("Rekap Import", "validate", function(frm) {
	date_for_series(frm);
})
frappe.ui.form.on("Rekap Import", "refresh", function(frm) {
	if (cur_frm.doc.linked_doc != null && !cur_frm.doc.__islocal){
		var df1 = frappe.meta.get_docfield("Rekap Import", "customer", cur_frm.doc.name);
		df1.read_only = 1;
	}
});
/*
frappe.ui.form.on("Rekap Import", "validate", function(frm) {
	if(cur_frm.doc.aju == '1'){
		cur_frm.doc.naming_series = 'IMP/PTI-.###./.MM./.YY'
	}else{
		cur_frm.doc.naming_series = 'IMP-PTI-.###./.MM./.YY'
	}
})

frappe.ui.form.on("Rekap Import", "validate", function(frm) {
	if(cur_frm.doc.aju == '1' && cur_frm.doc.naming_series != 'IMP/PTI-.###./.MM./.YY'){
		msgprint("Series not match bro");
		validated = false;
	}else if(cur_frm.doc.aju != '1' && cur_frm.doc.naming_series != 'IMP-PTI-.###./.MM./.YY'){
		msgprint("Series not match coy");
		validated = false;
	}
})
*/
