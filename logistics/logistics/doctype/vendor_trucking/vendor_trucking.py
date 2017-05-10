# -*- coding: utf-8 -*-
# Copyright (c) 2015, Abcgroups and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _
from frappe.utils import flt, comma_or, nowdate
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class VendorTrucking(Document):
	def validate(self):
		self.check_no_job()

	def check_no_job(self):
		tampung = []
		count = 0
		for i in self.get('items'):
			if i.for_print == 1 and i.purchase_invoice is None:
				if i.no_job not in tampung:
					tampung.append(i.no_job)
			if i.purchase_invoice is not None:
				i.for_print = 0
		hitung = len(tampung)
		if hitung >= 2:
			frappe.throw(_("You checked different No Job"))
		else:
			pass

	def on_update(self):
		self.update_urut()

	def update_urut(self):
		query = frappe.get_all("Vendor Trucking Item",
			fields=["name", "purchase_invoice"],
			filters={"parent":self.name},
			order_by='creation asc')
		urut = 0
		uu = []
		for a1 in query:
			if a1.purchase_invoice is None:
				urut = urut+1
				burut = str(urut)
				vti = frappe.get_doc("Vendor Trucking Item", a1.name)
				vti.idx = burut
				vti.save()
		for a2 in query:
			if a2.purchase_invoice is not None:
				urut = urut+1
				burut = str(urut)
				vti = frappe.get_doc("Vendor Trucking Item", a2.name)
				vti.idx = burut
				vti.save()

@frappe.whitelist()
def make_purchase_invoice(source_name, target_doc=None):
	no_doc = source_name
	item_code = frappe.db.get_value("Vendor Trucking", no_doc, "item_code")
	cek = frappe.db.get_value("Vendor Trucking Item", {"for_print":1, "parent":no_doc}, ["name"])
	if cek:
		def set_missing_values(source, target):
			rekap = frappe.db.get_value("Vendor Trucking Item", {"for_print":1, "parent":no_doc}, ["jenis_rekap", "no_job"], as_dict=1)
			target.posting_date = nowdate()
			target.jenis_rekap = rekap.jenis_rekap
			target.no_job = rekap.no_job
			target.run_method("set_missing_values")
		def update_item(source, target, source_parent):
			target.item_code = item_code
			target.qty = 1
		doc = get_mapped_doc("Vendor Trucking", source_name, {
			"Vendor Trucking": {
				"doctype": "Purchase Invoice",
				"field_map": {
					"vendor": "supplier"
				},
				"validation": {
					"docstatus": ["=", 0],
				},
			},
			"Vendor Trucking Item": {
				"doctype": "Purchase Invoice Item",
				"field_map": {
					"buying_amount": "rate",
					"name": "vendor_trucking_item"
				},
				"postprocess": update_item,
				"condition":lambda doc: doc.purchase_invoice is None and doc.for_print == 1
			},
		}, target_doc, set_missing_values)
		return doc
	else:
		frappe.throw(_("You have to fill out the check that there is no purchase invoice yet"))
