// Copyright (c) 2016, Abcgroups and contributors
// For license information, please see license.txt

frappe.query_reports["Laporan Price List Trucking"] = {
	"filters": [
		{
			"fieldname":"vendor",
			"label": __("Vendor"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Supplier",
			"get_query": function() {
					return {
						filters: {"supplier_type": "Trucking"}
					}
				}
		},
		{
			"fieldname":"region",
			"label": __("Wilayah"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Region"
		},
		{
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Customer"
		},
	]
}
