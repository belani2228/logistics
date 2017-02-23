// Copyright (c) 2016, Abcgroups and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rekap Import', {
	refresh: function(frm) {
		var me = this;
		if(!frm.doc.__islocal) {
			cur_frm.add_custom_button(__('Sales Invoice'), cur_frm.cscript['Sales Invoice'], __("Make"));
			cur_frm.page.set_inner_btn_group_as_primary(__("Make"));
		}
	},
});
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
cur_frm.set_query("vendor_trucking", "container_list",  function (doc, cdt, cdn) {
	var c_doc= locals[cdt][cdn];
    return {
        filters: {
            'supplier_type': 'Trucking'
        }
    }
});
cur_frm.set_query("template_trucking", "container_list",  function (doc, cdt, cdn) {
	var c_doc= locals[cdt][cdn];
    return {
        filters: {
            'supplier': c_doc.vendor_trucking,
						'jenis': 'Trucking'
        }
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
