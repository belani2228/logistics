# -*- coding: utf-8 -*-
# Copyright (c) 2015, Abcgroups and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class RekapExport(Document):
	def validate(self):
		self.set_daftar_container()
		self.update_tgl_kite()
		self.container_party()
		self.pic_container()

	def set_daftar_container(self):
		against_acc = []
		if self.daily_report != 'MULIA':
			for d in self.get('items'):
				if d.container_no not in against_acc:
					against_acc.append(d.container_no)
			self.daftar_container = ', '.join(against_acc)
		else:
			for d in self.get('empty_items'):
				if d.container_no not in against_acc:
					against_acc.append(d.container_no)
			self.daftar_container = ', '.join(against_acc)

	def update_tgl_kite(self):
		tgl_awal = ""
		for t in self.get("kite_document"):
			if t.document_date > tgl_awal:
				tgl_awal = t.document_date
		self.tgl_akhir_date = tgl_awal

	def container_party(self):
		qty_group = []
		qg = []
		if self.daily_report != 'MULIA':
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
		else:
			for p in self.get('empty_items'):
				if p.party_empty not in qty_group:
					qty_group.append(p.party_empty)
					qq = 0
					for q in self.get('empty_items'):
						if q.party_empty == p.party_empty:
							qq = qq+1
					if p.size_cont_empty == '-' and qq == 1:
						qg.append(p.party_empty)
					else:
						qg.append(str(qq)+'X'+p.party_empty)
			self.party = ', '.join(qg)

	def pic_container(self):
		tbm = ""
		tbm_pic = ""
		pu1 = ""
		pu2 = ""
		pu3 = ""
		ckk1 = ""
		ckk2 = ""
		g1 = ""
		g2 = ""
		g3 = ""
		if self.daily_report != "MULIA":
			paket = self.get("items")
		else:
			paket = self.get("empty_items")
		for c in paket:
			if c.tebus_bon_muat:
				tbm = c.tebus_bon_muat
			else:
				c.tebus_bon_muat = tbm
			if c.pic_tebus_bon:
				tbm_pic = c.pic_tebus_bon
			else:
				c.pic_tebus_bon = tbm_pic
			if c.pick_up_start:
				pu1 = c.pick_up_start
			else:
				c.pick_up_start = pu1
			if c.pick_up_done:
				pu2 = c.pick_up_done
			else:
				c.pick_up_done = pu2
			if c.pic_pick_up:
				pu3 = c.pic_pick_up
			else:
				c.pic_pick_up = pu3
			if c.cetak_kartu_kuning:
				ckk1 = c.cetak_kartu_kuning
			else:
				c.cetak_kartu_kuning = ckk1
			if c.pic_cetak_kartu:
				ckk2 = c.pic_cetak_kartu
			else:
				c.pic_cetak_kartu = ckk2
			if c.gate_in:
				g1 = c.gate_in
			else:
				c.gate_in = g1
			if c.status_container:
				g2 = c.status_container
			else:
				c.status_container = g2
			if c.pic_gate_in:
				g3 = c.pic_gate_in
			else:
				c.pic_gate_in = g3

	def on_update(self):
		self.update_item_mulia()
#		self.update_job_cost()
		frappe.db.sql("""DELETE FROM `tabCommunication` WHERE reference_name = %s AND comment_type = 'Updated'""", self.name)
		kom = frappe.get_doc({
			"doctype": "Communication",
			"subject": "From "+self.customer_name,
			"reference_doctype": "Rekap Export",
			"reference_name": self.name,
			"comment_type": "Updated",
			"communication_type": "Comment"
		}).insert()

	def update_item_mulia(self):
		if self.daily_report == "MULIA":
			frappe.db.sql("""DELETE FROM `tabRekap Export Item` WHERE parent = %s""", self.name)
			for m in self.get("empty_items"):
				ins = frappe.get_doc({
					"doctype": "Rekap Export Item",
					"container_no": m.container_no,
					"parent": self.name,
					"parentfield": "items",
					"parenttype": "Rekap Export",
					"idx": m.idx,
					"no_seal": m.no_seal,
					"license_plate": m.license_plate,
					"weight": m.weight,
					"type": m.type_empty,
					"size_cont": m.size_cont_empty,
					"custom_size": m.custom_size,
					"party": m.party_empty,
					"vendor_trucking": m.vendor_trucking,
					"tebus_bon_muat": m.tebus_bon_muat,
					"pic_tebus_bon": m.pic_tebus_bon,
					"pick_up_start": m.pick_up_start,
					"pick_up_done": m.pick_up_done,
					"pic_pick_up": m.pic_pick_up,
					"cetak_kartu_kuning": m.cetak_kartu_kuning,
					"pic_cetak_kartu": m.pic_cetak_kartu,
					"gate_in": m.gate_in,
					"status_container": m.status_container,
					"pic_gate_in": m.pic_gate_in
				}).insert()
		else:
			pass

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
				"jenis_rekap": "Rekap Export",
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

@frappe.whitelist()
def get_items_from_empty_container(source_name, target_doc=None):
	ec = get_mapped_doc("Rekap Export", source_name, {
		"Rekap Export": {
			"doctype": "Rekap Export",
		},
		"Rekap Export Mulia Empty": {
			"doctype": "Rekap Export Mulia Full",
			"field_map": {
				"type_empty":"type",
				"size_cont_empty": "size_cont",
				"party_empty": "party"
			},
		},
	}, target_doc)
	return ec
