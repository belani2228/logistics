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
			]
		},
		{
			"label": _("Tools"),
			"items": [
				{
					"type": "doctype",
					"name": "Carrier",
					"description": _("Carrier")
				},
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
					"name": "Trucking",
					"description": _("Trucking")
				},
			]
		},
		{
			"label": _("Setup"),
			"items": [
				{
					"type": "doctype",
					"name": "Rekam Jejak",
					"description": _("Rekam Jejak")
				},
			]
		}
	]
