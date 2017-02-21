from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

def reset_series():
	frappe.db.sql("UPDATE `tabSeries` SET current = 0 WHERE `name` = 'IMP/PTI'")
