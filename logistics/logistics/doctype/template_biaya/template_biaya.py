# -*- coding: utf-8 -*-
# Copyright (c) 2015, Abcgroups and contributors
# For license information, please see license.txt
# Gunakan bahasa indonesia saja ya

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

@frappe.whitelist()
def get_items_for_invoice(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.is_paid = 1
		#target.credit_to = "Cash"
		target.run_method("set_missing_values")

	pi = get_mapped_doc("Template Biaya", source_name, {
			"Template Biaya": {
				"doctype": "Purchase Invoice",
				"validation": {
					"docstatus": ["!=", 2]
				},
				"field_map": {
					"total_buying": "total"
				},
			},
			"Template Biaya Item": {
				"doctype": "Purchase Invoice Item",
				"field_map": {
					"item_name": "description",
					"buying_rate": "rate",
					"buying_amount": "amount",
					"income": "income_account"
				},
			},
		}, target_doc, set_missing_values)

	return pi
