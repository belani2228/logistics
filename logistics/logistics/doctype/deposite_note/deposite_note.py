# -*- coding: utf-8 -*-
# Copyright (c) 2015, Abcgroups and contributors
# For license information, please see license.txt
# Gunakan bahasa indonesia saja ya

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class DepositeNote(Document):
	def validate(self):
		self.set_count_item()

	def set_count_item(self):
		count1 = 0;
		for d in self.get('items'):
			count1 = count1+1
		self.count_item = count1

	def get_template_item(self):
		komponen = frappe.db.sql("""SELECT b1.item_code, b1.item_name, b1.qty, b1.uom,
			b1.buying_rate, b1.buying_amount,
			b1.expense, b1.cost_center
			FROM `tabTemplate Biaya Item` b1, `tabTemplate Biaya` b2
			WHERE b1.parent = b2.name AND b1.parent = %s
			ORDER by b1.idx ASC""", self.template_biaya, as_dict=1)

		self.set('items', [])

		for d in komponen:
			nl = self.append('items', {})
			nl.item_code = d.item_code
			nl.item_name = d.item_name
			nl.qty = d.qty
			nl.uom = d.uom
			nl.rate = d.buying_rate
			nl.amount = d.buying_amount
			nl.expense_account = d.expense
			nl.cost_center = d.cost_center

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
				"total_claim": "paid_amount",
				"vendor": "supplier",
				"name": "remarks",
			},
			"validation": {
				"docstatus": ["=", 1],
			},
		},
		"Deposite Note Item": {
			"doctype": "Purchase Invoice Item",
			"field_map": {
				"rate": "rate",
				"name": "deposite_note_detail"
			},
			"condition":lambda doc: doc.pi_no is None
		},
	}, target_doc, set_missing_values)

	return doc

@frappe.whitelist()
def get_template_item2(source_name, target_doc=None):
	#frappe.throw(_("Source Name: {0}").format(source_name))
	def set_missing_values(source, target):
		target.expense_account = ""
		#target.credit_to = "Cash"
		target.run_method("set_missing_values")

	tb = get_mapped_doc("Template Biaya", source_name, {
			"Template Biaya": {
				"doctype": "Sales Invoice",
				"validation": {
					"docstatus": ["!=", 2]
				},
				"field_map": {
					"total_selling": "total"
				},
			},
			"Template Biaya Item": {
				"doctype": "Sales Invoice Item",
				"field_map": {
					"item_name": "description",
					"uom": "stock_uom",
					"selling_rate": "rate",
					"selling_amount": "amount",
					"income": "income_account"
				},
			},
		}, target_doc, set_missing_values)

	return tb

# sudah tidak dipakai, krn sekarang tarik items dari Purchase Invoice
@frappe.whitelist()
def get_items_dn(source_name, target_doc=None):
	if target_doc:
		if isinstance(target_doc, basestring):
			import json
			target_doc = frappe.get_doc(json.loads(target_doc))

	def set_missing_values(source, target):
		#target.expense_account = ""
		#target.credit_to = "Cash"
		target.run_method("set_missing_values")

	query = frappe.db.sql_list("""SELECT dn.`name`
		FROM `tabDeposite Note` dn
		WHERE dn.no_job = %s ORDER BY dn.`name` ASC""", source_name)

	for q in query:
		dn = get_mapped_doc("Deposite Note", q, {
				"Deposite Note": {
					"doctype": "Sales Invoice",
				},
				"Deposite Note Item": {
					"doctype": "Sales Invoice Item",
					"field_map": {
					},
				},
			}, target_doc, set_missing_values)

	return dn
