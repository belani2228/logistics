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
		self.update_tgl_receive_copy_doc()
		self.update_tgl_receive_ori_doc()
		self.update_response()
		self.container_party()

	def set_daftar_container(self):
		against_acc = []
		for d in self.get('items'):
			if d.container_no not in against_acc:
				against_acc.append(d.container_no)
		self.daftar_container = ', '.join(against_acc)

	def update_tgl_receive_copy_doc(self):
		tgl_awal = ""
		for t in self.get("copy_document"):
			if t.document_date > tgl_awal:
				tgl_awal = t.document_date
		self.receive_copy_document = tgl_awal

	def update_tgl_receive_ori_doc(self):
		tgl_awal = ""
		for t in self.get("original_document"):
			if t.document_date > tgl_awal:
				tgl_awal = t.document_date
		self.receive_ori_document = tgl_awal

	def update_response(self):
		if self.spjk >= self.spjm:
			response = self.spjk
		else:
			response = self.spjm
		self.response = response

	def container_party(self):
		qty_group = []
		qg = []
		for p in self.get('items'):
			if p.party not in qty_group:
				qty_group.append(p.party)
				qq = 0
				for q in self.get('items'):
					if q.party == p.party:
						qq = qq+1
				if p.size_cont == '-' and qq == 1:
					qg.append(p.party)
				else:
					qg.append(str(qq)+'X'+p.party)
		self.party = ', '.join(qg)

	def on_update(self):
#		self.update_job_cost()
		frappe.db.sql("""DELETE FROM `tabCommunication` WHERE reference_name = %s AND comment_type = 'Updated'""", self.name)
		kom = frappe.get_doc({
			"doctype": "Communication",
			"subject": "From "+self.customer_name,
			"reference_doctype": "Rekap Import",
			"reference_name": self.name,
			"comment_type": "Updated",
			"communication_type": "Comment"
		}).insert()

	def update_job_cost(self):
		cek = frappe.db.get_value("Job Cost", {"no_job": self.name}, "name")
		if cek:
			job_cost = frappe.get_doc("Job Cost", cek)
			job_cost.customer = self.customer
			job_cost.date = self.date
			job_cost.party = self.party
			job_cost.no_bl = self.bl_number
			job_cost.save()
		else:
			job_cost = frappe.get_doc({
				"doctype": "Job Cost",
				"no_job": self.name,
				"jenis_rekap": "Rekap Import",
				"customer": self.customer,
				"date": self.date,
				"no_bl": self.bl_number,
				"party": self.party
			})
			job_cost.insert()

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
