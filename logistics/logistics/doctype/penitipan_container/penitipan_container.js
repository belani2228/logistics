// Copyright (c) 2016, Abcgroups and contributors
// For license information, please see license.txt

frappe.ui.form.on('Penitipan Container', {
	refresh: function(frm) {
		var me = this;
	}
});

frappe.ui.form.on("Penitipan Container", "no_job", function(frm, cdt, cdn) {
	if(cur_frm.doc.no_job){
	    frappe.call({
	        method: "frappe.client.get",
	        args: {
	            doctype: "Rekap Export",
							filters:{
								name: cur_frm.doc.no_job
							}
	        },
	        callback: function (data) {
							frappe.model.set_value(cdt, cdn, "shipping_insturction", data.message.shipping_instruction);
							frappe.model.set_value(cdt, cdn, "do", data.message.no_do);
	            frappe.model.set_value(cdt, cdn, "carrier", data.message.carrier);
							frappe.model.set_value(cdt, cdn, "vessel", data.message.vessel);
							frappe.model.set_value(cdt, cdn, "party", data.message.party);
							frappe.model.set_value(cdt, cdn, "pod", data.message.pod);
							frappe.model.set_value(cdt, cdn, "open_cy", data.message.open_cy);
							frappe.model.set_value(cdt, cdn, "clossing_cy", data.message.clossing_cy);
					}
	    })
	}
});
frappe.ui.form.on("Penitipan Container", "get_container_list", function(frm) {
	erpnext.utils.map_current_doc({
			method: "logistics.logistics.doctype.penitipan_container.penitipan_container.get_container",
			source_name: cur_frm.doc.no_job,
	});
})
cur_frm.cscript.gate_in_date = function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];
		if(d.gate_out_date){
			d.waktu_penitipan = frappe.datetime.get_day_diff(d.gate_out_date, d.gate_in_date);
			d.total_storage = d.waktu_penitipan * d.storage;
			d.total_penitipan = d.total_storage + d.lolo + d.admin;

			refresh_field('waktu_penitipan', d.name, 'items');
			refresh_field('total_storage', d.name, 'items');
			refresh_field('total_penitipan', d.name, 'items');
		}
}
cur_frm.cscript.lolo=cur_frm.cscript.admin=cur_frm.cscript.storage=cur_frm.cscript.gate_out_date=cur_frm.cscript.gate_in_date;
