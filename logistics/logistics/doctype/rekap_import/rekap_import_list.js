frappe.listview_settings['Rekap Import'] = {
	add_fields: ["name", "status"],
  filters:[["status","=", "Draft"]],
  colwidths: {"name": 2, "status": 1},
  get_indicator: function(doc) {
		if(doc.status==="Draft") {
			return [__("New"), "green", "status,=," + doc.status];
		}else if(doc.status==="Closed") {
			return [__("Closed"), "orange", "status,=," + doc.status];
    }else if(doc.status==="Cancelled") {
			return [__("Cancelled"), "orange", "status,=," + doc.status];
    }
	}
};
