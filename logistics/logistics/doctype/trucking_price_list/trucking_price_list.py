# -*- coding: utf-8 -*-
# Copyright (c) 2015, Abcgroups and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _
from frappe.model.document import Document

class TruckingPriceList(Document):
	def validate(self):
		if self.is_active:
			self.update_if_active()

	def update_if_active(self):
		if self.customer:
			if self.get('__islocal'):
				cek = frappe.db.get_value("Trucking Price List", {"customer": self.customer, "vendor": self.vendor, "wilayah": self.wilayah, "docstatus": ["!=", 2]}, "name")
				if cek:
					for row in cek:
						tpl = frappe.get_doc("Trucking Price List", row)
						tpl.is_active = 0
						tpl.save()
