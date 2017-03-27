# -*- coding: utf-8 -*-
# Copyright (c) 2015, Abcgroups and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class RekapExport(Document):
	def validate(self):
		self.set_daftar_container()
#		self.update_party()
		self.update_tgl_kite()

	def set_daftar_container(self):
		against_acc = []
		for d in self.get('items'):
			if d.container_no not in against_acc:
				against_acc.append(d.container_no)
		self.daftar_container = ', '.join(against_acc)

	def update_party(self):
		masukin = []
		komponen = frappe.db.sql("""SELECT DISTINCT(r1.party) AS party, r1.size_cont,
		(SELECT COUNT(`name`) FROM `tabRekap Export Item` r2 WHERE r2.parent = %(nama)s AND r2.party = r1.party) AS jmlh
		FROM `tabRekap Export Item` r1
		WHERE r1.parent = %(nama)s""", {"nama":self.name}, as_dict=1)
		for p in komponen:
			if p.size_cont == "-":
				masukin.append(str(p.jmlh)+""+p.party)
			else:
				masukin.append(str(p.jmlh)+"X"+p.party)
		self.party = ', '.join(masukin)

	def update_tgl_kite(self):
		tgl_awal = ""
		for t in self.get("kite_document"):
			if t.document_date > tgl_awal:
				tgl_awal = t.document_date
		self.tgl_akhir_date = tgl_awal

	def on_update(self):
		frappe.db.sql("""DELETE FROM `tabCommunication` WHERE reference_name = %s AND comment_type = 'Updated'""", self.name)
		kom = frappe.get_doc({
			"doctype": "Communication",
			"subject": "From "+self.customer_name,
			"reference_doctype": "Rekap Export",
			"reference_name": self.name,
			"comment_type": "Updated",
			"communication_type": "Comment"
		}).insert()

	def on_submit(self):
		frappe.db.set(self, 'status', 'Submitted')
		self.update_party()

	def on_cancel(self):
		frappe.db.set(self, 'status', 'Cancelled')


@frappe.whitelist()
def close_rekap_export(status, name):
	frappe.db.sql("""UPDATE `tabRekap Export` SET status = 'Closed' WHERE `name` = %s""", name)

@frappe.whitelist()
def open_rekap_export(status, name):
	frappe.db.sql("""UPDATE `tabRekap Export` SET status = 'Submitted' WHERE `name` = %s""", name)

@frappe.whitelist()
def make_sales_invoice(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.jenis_rekap = "Rekap Export"
		target.update_stock = 1
		target.run_method("set_missing_values")

	si = get_mapped_doc("Rekap Export", source_name, {
		"Rekap Export": {
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
