// Copyright (c) 2016, Abcgroups and contributors
// For license information, please see license.txt

frappe.ui.form.on('Trucking Price List', {
	refresh: function(frm) {

	}
});
cur_frm.set_query("vendor", function (doc) {
  return {
    filters: {
      'supplier_type': 'Trucking'
    }
	}
});
