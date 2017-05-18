from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Documents"),
			"items": [
				{
					"type": "doctype",
					"name": "Rekap Import",
					"description": _("Rekap Import")
				},
				{
					"type": "doctype",
					"name": "Rekap Export",
					"description": _("Rekap Export")
				},
				{
					"type": "doctype",
					"name": "Deposite Note",
					"description": _("Deposite Note")
				},
				{
					"type": "doctype",
					"name": "Template Biaya",
					"description": _("Template Biaya")
				},
				{
					"type": "doctype",
					"name": "Penitipan Container",
					"description": _("Penitipan Container")
				},
				{
					"type": "doctype",
					"name": "Trucking Price List",
					"description": _("Daftar harga vendor trucking")
				},
			]
		},
		{
			"label": _("Integration"),
			"items": [
				{
					"type": "doctype",
					"name": "Job Cost",
					"description": _("Job Cost")
				},
				{
					"type": "doctype",
					"name": "Vendor Trucking",
					"description": _("Vendor Trucking")
				},
			]
		},
		{
			"label": _("Tools"),
			"items": [
				{
					"type": "doctype",
					"name": "Commodity",
					"description": _("Commodity")
				},
				{
					"type": "doctype",
					"name": "Port",
					"description": _("Port")
				},
				{
					"type": "doctype",
					"name": "Shipper",
					"description": _("Shipper")
				},
				{
					"type": "doctype",
					"name": "Region",
					"description": _("Wilayah")
				},
			]
		},
		{
			"label": _("Reports"),
			"items": [
				{
					"type": "report",
					"name": "Rekap Import Report",
					"doctype": "Rekap Import",
					"is_query_report": True
				},
				{
					"type": "report",
					"name": "Rekap Export Report",
					"doctype": "Rekap Export",
					"is_query_report": True
				},
				{
					"type": "report",
					"name": "Report Export Operational",
					"doctype": "Rekap Export",
					"is_query_report": True
				},
				{
					"type": "report",
					"name": "Performance Import",
					"doctype": "Rekap Import",
					"is_query_report": True
				},
				{
					"type": "report",
					"name": "Laporan Penitipan Container",
					"doctype": "Penitipan Container",
					"is_query_report": True
				},
				{
					"type": "report",
					"name": "Laporan Harian Per Customer",
					"doctype": "Rekap Import",
					"is_query_report": True
				},
				{
					"type": "report",
					"name": "Purchase Invoice Monthly",
					"doctype": "Purchase Invoice",
					"is_query_report": True
				},
			]
		},
	]
