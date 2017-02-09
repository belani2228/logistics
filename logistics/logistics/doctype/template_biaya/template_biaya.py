# -*- coding: utf-8 -*-
# Copyright (c) 2015, Abcgroups and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class TemplateBiaya(Document):
	pass

@frappe.whitelist()
def get_items_from_template(source_name, target_doc=None):
	#frappe.throw(_("Source Name: {0}").format(source_name))
	def set_missing_values(source, target):
		target.run_method("set_missing_values")

	doc = get_mapped_doc("Template Biaya", source_name, {
		"Template Biaya": {
			"doctype": "Sales Order",
		},
		"Template Biaya Item": {
			"doctype": "Sales Order Item",
			"field_map": {
				"selling_rate": "rate",
				"selling_amount": "amount"
			}
		},
	}, target_doc, set_missing_values)

	return doc
