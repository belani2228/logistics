// Copyright (c) 2016, Abcgroups and contributors
// For license information, please see license.txt

frappe.query_reports["Purchase Invoice Monthly"] = {
	"filters": [
		/*
		{
			"fieldname":"year",
			"label": __("Year"),
			"fieldtype": "Link",
			"options": "Fiscal Year",
			"width": "80",
			"reqd": 1
		},
		*/
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.defaults.get_user_default("year_start_date"),
			"width": "80",
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"width": "80",
			"reqd": 1
		},
		/*
		{
			"fieldname": "monty",
			"label": __("Monty"),
			"width": "80",
			"fieldtype": "Select",
			"options": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
			"reqd": 1
		},
		*/
	],
	"formatter":function (row, cell, value, columnDef, dataContext, default_formatter) {
		value = default_formatter(row, cell, value, columnDef, dataContext);
		if(columnDef.id == "Sales Invoice" || columnDef.id == "SI Date"){
			if(dataContext["SI Date"]){
				var s = dataContext["SI Date"];
				var fields = s.split('-');
				var tb1 = fields[0]+"-"+fields[1];
				var p = dataContext["PI Date"];
				var pf = p.split('-');
				var tb2 = pf[0]+"-"+pf[1];
				if(tb1 != tb2) {
						value = "<span style='color:blue !important; font-weight:bold'>" + value + "</span>";
				}
			}
		}
		return value;
	}
}
