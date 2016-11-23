# -*- coding: utf-8 -*-
# Copyright (c) 2015, Abcgroups and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class DepositeNote(Document):
	pass
	
@frappe.whitelist()
def make_purchase_invoice(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.is_paid = 1
		#target.credit_to = "Cash"
		target.run_method("set_missing_values")

	doc = get_mapped_doc("Deposite Note", source_name, {
		"Deposite Note": {
			"doctype": "Purchase Invoice",
			"field_map": {
				"posting_date": "due_date",
				"account_paid_to": "cash_bank_account",
				"total_claim": "paid_amount"
			},
			"validation": {
				"docstatus": ["=", 1],
			},
		},
		"Deposite Note Item": {
			"doctype": "Purchase Invoice Item",
			"field_map": {
				"stock_uom": "uom",
				"claim_amount": "rate"
			}
		},
	}, target_doc, set_missing_values)
	
	return doc