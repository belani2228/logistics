// Copyright (c) 2016, Abcgroups and contributors
// For license information, please see license.txt

frappe.query_reports["Penitipan Container"] = {
	"filters": [
		{
			"fieldname":"no_rekap",
			"label": __("No Rekap"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Rekap Export",
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": sys_defaults.year_start_date,
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
	]
}
