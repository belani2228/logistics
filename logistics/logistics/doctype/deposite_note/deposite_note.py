# -*- coding: utf-8 -*-
# Copyright (c) 2015, Abcgroups and contributors
# For license information, please see license.txt
# Gunakan bahasa indonesia saja ya

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, flt
from frappe import msgprint, _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class DepositeNote(Document):
	def validate(self):
		self.set_count_item()
		self.check_double_item()

	def on_submit(self):
		if self.jenis_rekap == "Rekap Import":
			frappe.db.sql("""update `tabRekap Import` set linked_doc = %s where `name` = %s""", (self.name, self.no_job))
		else:
			frappe.db.sql("""update `tabRekap Export` set linked_doc = %s where `name` = %s""", (self.name, self.no_job))

	def on_cancel(self):
		if self.jenis_rekap == "Rekap Import":
			lain = frappe.db.sql("""select `name` from `tabDeposite Note` where docstatus = '1' and `no_job` = %s and `name` != %s limit 1""", (self.no_job, self.name))
			if lain:
				frappe.db.sql("""update `tabRekap Import` set linked_doc = %s where `name` = %s""", (lain, self.no_job))
			else:
				frappe.db.sql("""update `tabRekap Import` set linked_doc = null where `name` = %s""", self.no_job)
		else:
			lain = frappe.db.sql("""select `name` from `tabDeposite Note` where docstatus = '1' and `no_job` = %s and `name` != %s limit 1""", (self.no_job, self.name))
			if lain:
				frappe.db.sql("""update `tabRekap Export` set linked_doc = %s where `name` = %s""", (lain, self.no_job))
			else:
				frappe.db.sql("""update `tabRekap Export` set linked_doc = null where `name` = %s""", self.no_job)

	def set_count_item(self):
		count1 = 0;
		for d in self.get('items'):
			count1 = count1+1
		self.count_item = count1

	def check_double_item(self):
		error = []
		for d in self.get('items'):
			check_item = frappe.db.sql("""select a.`name` from `tabDeposite Note Item` a
				inner join `tabDeposite Note` b on b.`name` = a.parent
				where a.docstatus != '2' and b.no_job = %s and b.posting_date = %s and a.item_code = %s and b.`name` != %s""",
				(self.no_job, self.posting_date, d.item_code, self.name))
			if check_item:
				error.append(d.item_code)
		if len(error) != 0:
			frappe.throw("Item "+', '.join(error)+" double input")

	def on_update(self):
		frappe.db.sql("""DELETE FROM `tabCommunication` WHERE reference_name = %s AND comment_type = 'Updated'""", self.name)
		kom = frappe.get_doc({
			"doctype": "Communication",
			"subject": "No Job "+self.no_job+" | "+self.customer,
			"reference_doctype": "Deposite Note",
			"reference_name": self.name,
			"comment_type": "Updated",
			"communication_type": "Comment"
		}).insert()

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
		if str(source.difference) <= 0:
			target.write_off_amount = source.difference
		else:
			target.write_off_amount = source.difference * -1
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
				"account_paid_to": "cash_bank_account",
				"deposite_amount": "paid_amount"
			},
			"validation": {
				"docstatus": ["=", 1],
			},
		},
		"Deposite Note Item": {
			"doctype": "Purchase Invoice Item",
			"field_map": {
				"rate": "rate",
				"name": "deposite_note_detail",
				"rate": "selling_rate"
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
