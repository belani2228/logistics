# -*- coding: utf-8 -*-
# Copyright (c) 2015, Abcgroups and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class RekapImport(Document):
	def validate(self):
		self.set_daftar_container()
		self.update_tgl_receive_copy_doc()
		self.update_tgl_receive_ori_doc()
		self.update_response()
		self.container_party()
		self.trucking_price()

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
		count2 = 0
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
		if count2 >= 0:
			self.party = ', '.join(qg)

	def trucking_price(self):
		tp = 0
		for t in self.get('items'):
			if t.type and t.size_cont and t.vendor_trucking and t.region:
				cek_price_list = frappe.db.get_value("Trucking Price List", {"wilayah": t.region, "vendor": t.vendor_trucking, "customer":self.customer}, "name")
				if cek_price_list:
					cpd = frappe.db.get_value("Trucking Price List Item", {"parent":cek_price_list, "size_cont":t.size_cont, "type":t.type}, ["name", "buying"], as_dict=1)
					if cpd:
						t.trucking_price_list = cek_price_list
						t.trucking_price_list_item = cpd.name
						t.trucking_price_list_item_buying = cpd.buying
					else:
						t.trucking_price_list = None
						t.trucking_price_list_item = None
						t.trucking_price_list_item_buying = None
				else:
					cek_price_list_all = frappe.db.sql("""select name from `tabTrucking Price List` where wilayah = %s and vendor = %s and customer is null""", (t.region, t.vendor_trucking))
					if cek_price_list_all:
						cpd = frappe.db.get_value("Trucking Price List Item", {"parent":cek_price_list_all[0][0], "size_cont":t.size_cont, "type":t.type}, ["name", "buying"], as_dict=1)
						if cpd:
							t.trucking_price_list = cek_price_list_all[0][0]
							t.trucking_price_list_item = cpd.name
							t.trucking_price_list_item_buying = cpd.buying
						else:
							t.trucking_price_list = None
							t.trucking_price_list_item = None
							t.trucking_price_list_item_buying = None
					else:
						t.trucking_price_list = None
						t.trucking_price_list_item = None
						t.trucking_price_list_item_buying = None
			else:
				t.trucking_price_list = None
				t.trucking_price_list_item = None
				t.trucking_price_list_item_buying = None

	def on_update(self):
		self.update_job_cost()
		self.update_vendor_trucking()
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
		if self.party:
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

	def update_vendor_trucking(self):
		period = self.period
		against_acc = []
		for v1 in self.get('items'):
			if v1.trucking_price_list and v1.trucking_price_list_item and v1.vendor_trucking not in against_acc:
				cek_vendor = frappe.db.get_value("Vendor Trucking", {"period": period, "vendor": v1.vendor_trucking}, "name")
				if not cek_vendor:
					cari_supp = frappe.db.get_value("Supplier", v1.vendor_trucking, "supplier_name")
					vt = frappe.get_doc({
						"doctype": "Vendor Trucking",
						"vendor": v1.vendor_trucking,
						"vendor_name": cari_supp,
						"period": period
					})
					vt.insert()
					against_acc.append(v1.vendor_trucking)
		delete = frappe.db.sql("""DELETE FROM `tabVendor Trucking Item` WHERE no_job = %s AND purchase_invoice IS NULL""", self.name)
		for v in self.get('items'):
			if v.trucking_price_list and v.trucking_price_list_item:
				cek_vendor = frappe.db.get_value("Vendor Trucking", {"period": period, "vendor": v.vendor_trucking}, "name")
				cek_vendor_det = frappe.db.get_value("Vendor Trucking Item", {"parent":cek_vendor, "rekap_item": v.name}, "name")
				if cek_vendor_det:
					vti = frappe.get_doc("Vendor Trucking Item", cek_vendor_det)
					vti.jenis_rekap = "Rekap Import"
					vti.no_job = self.name
					vti.container_no = v.container_no
					vti.job_date = self.date
					vti.region = v.region
					vti.rekap_item = v.name
					vti.buying_amount = v.trucking_price_list_item_buying
					vti.save()
				else:
					vti = frappe.get_doc({
						"doctype": "Vendor Trucking Item",
						"parent": cek_vendor,
						"parentfield": "items",
						"parenttype": "Vendor Trucking",
						"jenis_rekap": "Rekap Import",
						"no_job": self.name,
						"container_no": v.container_no,
						"job_date": self.date,
						"region": v.region,
						"rekap_item": v.name,
						"buying_amount": v.trucking_price_list_item_buying
					})
					vti.insert()

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
