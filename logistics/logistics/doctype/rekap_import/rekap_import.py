# -*- coding: utf-8 -*-
# Copyright (c) 2015, Abcgroups and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class RekapImport(Document):
	def validate(self):
		self.set_daftar_container()

	def set_daftar_container(self):
		against_acc = []
		for d in self.get('container_list'):
			if d.container_no not in against_acc:
				against_acc.append(d.container_no)
		self.daftar_container = ', '.join(against_acc)
