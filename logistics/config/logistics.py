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
			]
		},
		{
			"label": _("Tools"),
			"items": [
				{
					"type": "doctype",
					"name": "Port",
					"description": _("Pelabuhan")
				},
				{
					"type": "doctype",
					"name": "Carrier",
					"description": _("Carrier")
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
