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
					"name": "Penitipan Container",
					"doctype": "Rekap Export",
					"is_query_report": True
				},
			]
		},
	]
