// Copyright (c) 2016, Abcgroups and contributors
// For license information, please see license.txt

frappe.query_reports["Performance Import"] = {
	"filters": [
		{
			"fieldname":"no_job",
			"label": __("No Job"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Rekap Import",
		},
		{
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Customer",
		},
	]
}
