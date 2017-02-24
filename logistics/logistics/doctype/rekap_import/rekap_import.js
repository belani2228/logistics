// Copyright (c) 2016, Abcgroups and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rekap Import', {
	refresh: function(frm) {
		var me = this;
		if (frm.doc.docstatus == '1' && frm.doc.status != "Closed") {
			// close
			//cur_frm.add_custom_button(__('Close'), this.close_rekap_import, __("Status"))
			cur_frm.add_custom_button(__('Close'), cur_frm.cscript['Close'], __("Status"));
			cur_frm.page.set_inner_btn_group_as_primary(__("Status"));
		}
		if (frm.doc.docstatus == '1' && frm.doc.status == "Closed") {
			cur_frm.add_custom_button(__('Re-Open'), cur_frm.cscript['Open Rekap Import'], __("Status"));
			cur_frm.page.set_inner_btn_group_as_primary(__("Status"));
		}
		if(!frm.doc.__islocal && frm.doc.status != "Closed") {
			cur_frm.add_custom_button(__('Sales Invoice'), cur_frm.cscript['Sales Invoice'], __("Make"));
			cur_frm.page.set_inner_btn_group_as_primary(__("Make"));
		}
	},
});
cur_frm.cscript['Close'] = function() {
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
cur_frm.cscript['Open Rekap Import'] = function() {
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
/*
cur_frm.set_query("shipper",  function (frm) {
		return {
        filters: {
					'supplier_type': 'shipper'
        }
		}
});
*/
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
frappe.ui.form.on("Rekap Import Item", "container_no", function(frm, cdt, cdn) {
	child = locals[cdt][cdn];
	child.size = cur_frm.doc.size_cont;
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
