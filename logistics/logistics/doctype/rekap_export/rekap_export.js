// Copyright (c) 2016, Abcgroups and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rekap Export', {
	refresh: function(frm) {
		var me = this;
		if(frm.doc.docstatus==0 && !frm.doc.__islocal) {
			cur_frm.add_custom_button(__('Sales Invoice'), cur_frm.cscript['Sales Invoice'], __("Make"));
			cur_frm.page.set_inner_btn_group_as_primary(__("Make"));
		}
	}
});
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
//hitung selisih hari
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
