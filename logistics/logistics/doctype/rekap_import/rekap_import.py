# -*- coding: utf-8 -*-
# Copyright (c) 2015, Abcgroups and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class RekapImport(Document):
	def validate(self):
		self.set_daftar_container()
		#self.size_in_items()
		self.update_party()

	def set_daftar_container(self):
		against_acc = []
		for d in self.get('items'):
			if d.container_no not in against_acc:
				against_acc.append(d.container_no)
		self.daftar_container = ', '.join(against_acc)

	def update_party(self):
		masukin = []
		komponen = frappe.db.sql("""SELECT DISTINCT(r1.party) AS party,
		(SELECT COUNT(`name`) FROM `tabRekap Import Item` r2 WHERE r2.parent = %(nama)s AND r2.party = r1.party) AS jmlh
		FROM `tabRekap Import Item` r1
		WHERE r1.parent = %(nama)s""", {"nama":self.name}, as_dict=1)
		for p in komponen:
			masukin.append(str(p.jmlh)+"X"+p.party)
		self.party = ', '.join(masukin)

	def on_submit(self):
		frappe.db.set(self, 'status', 'Submitted')

	def on_cancel(self):
		frappe.db.set(self, 'status', 'Cancelled')

@frappe.whitelist()
def close_rekap_import(status, name):
	frappe.db.sql("""UPDATE `tabRekap Import` SET status = 'Closed' WHERE `name` = %s""", name)

@frappe.whitelist()
def open_rekap_import(status, name):
	frappe.db.sql("""UPDATE `tabRekap Import` SET status = 'Submitted' WHERE `name` = %s""", name)

@frappe.whitelist()
def make_sales_invoice(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.jenis_rekap = "Rekap Import"
		target.update_stock = 1
		target.run_method("set_missing_values")

	si = get_mapped_doc("Rekap Import", source_name, {
		"Rekap Import": {
			"doctype": "Sales Invoice",
			"field_map": {
				"name":"no_job"
			},
			"field_no_map": [
				"due_date"
			],
		},
	}, target_doc, set_missing_values)
	return si
