# -*- coding: utf-8 -*-
# Copyright (c) 2015, Abcgroups and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc


class PenitipanContainer(Document):
	pass

	def on_update(self):
		frappe.db.sql("""DELETE FROM `tabCommunication` WHERE reference_name = %s AND comment_type = 'Updated'""", self.name)
		if self.shipping_instruction:
			subject = "No Job "+self.no_job+" | No SI "+self.shipping_instruction
		else:
			subject = "No Job "+self.no_job
		kom = frappe.get_doc({
			"doctype": "Communication",
			"subject": subject,
			"reference_doctype": "Penitipan Container",
			"reference_name": self.name,
			"comment_type": "Updated",
			"communication_type": "Comment"
		}).insert()

@frappe.whitelist()
def get_container(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.run_method("set_missing_values")

	si = get_mapped_doc("Rekap Export", source_name, {
		"Rekap Export": {
			"doctype": "Penitipan Container",
			"field_no_map": [
				"name", "title", "naming_series"
			],
		},
		"Rekap Export Item": {
			"doctype": "Penitipan Container Item",
			"condition":lambda doc: doc.status_container=="Storage",
			"field_map": {
				"name":"no_job"
			},
		},
	}, target_doc, set_missing_values)
	return si
