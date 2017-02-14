// Copyright (c) 2016, Abcgroups and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rekap Import', {
	refresh: function(frm) {

	}
});
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
