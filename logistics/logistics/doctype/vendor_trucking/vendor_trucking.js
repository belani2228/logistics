// Copyright (c) 2016, Abcgroups and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vendor Trucking', {
	refresh: function(frm) {
		if(frm.doc.docstatus!=2) {
			cur_frm.add_custom_button(__('Purchase Invoice'), cur_frm.cscript['Purchase Invoice'], __("Make"));
			cur_frm.page.set_inner_btn_group_as_primary(__("Make"));
		}
	}
});
cur_frm.cscript['Purchase Invoice'] = function() {
	frappe.model.open_mapped_doc({
		method: "logistics.logistics.doctype.vendor_trucking.vendor_trucking.make_purchase_invoice",
		frm: cur_frm
	})
}

frappe.ui.form.on("Vendor Trucking", "onload", function(frm, cdt, cdn) {
//	row = locals[cdt][cdn];
//	if(row.purchase_invoice){
//		frm.set_df_property("for_print", "read_only", d.purchase_invoice ? 0 : 1);
//  frm.set_read_only(row.for_print)
//	var df = frappe.meta.get_docfield("Vendor Trucking Item","for_print", cur_frm.doc.name);
//	df.read_only = 1;
//	}
});
/*
cur_frm.cscript.custom_refresh = function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];
    cur_frm.set_df_property("for_print", "read_only", d.purchase_invoice == "PINV-00029");
}
cur_frm.cscript.custom_refresh = function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];
		if(d.purchase_invoice == 'PINV-00029'){
			d.for_print = 1
		}else{
			d.for_print = 0
		}

		refresh_field('for_print', d.name, 'items');
}
*/
