# -*- coding: utf-8 -*-
# Copyright (c) 2015, Abcgroups and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _
from frappe.model.document import Document

class TruckingPriceList(Document):
	def validate(self):
		self.vendor_truck()

	def vendor_truck(self):
		pass
