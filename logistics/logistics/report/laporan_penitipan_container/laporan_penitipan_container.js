// Copyright (c) 2016, Abcgroups and contributors
// For license information, please see license.txt

frappe.query_reports["Laporan Penitipan Container"] = {
	"filters": [
		{
			"fieldname":"no_job",
			"label": __("No Job"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Rekap Export",
		},
	]
}
