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
