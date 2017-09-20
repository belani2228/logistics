// Copyright (c) 2016, Abcgroups and contributors
// For license information, please see license.txt

frappe.query_reports["Activity User"] = {
	"filters": [
		{
			"fieldname":"user",
			"label": __("User"),
			"fieldtype": "Link",
			"width": "80",
			"options": "User",
			"reqd": 1
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": frappe.datetime.get_today(),
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
