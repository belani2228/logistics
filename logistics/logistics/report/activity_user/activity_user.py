# Copyright (c) 2013, Abcgroups and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, getdate

def execute(filters=None):
	columns = get_columns()
	sl_entries = get_entries(filters)
	data = []

	for ri in sl_entries:
		data.append([ri.owner, ri.creation, ri.comment_type, ri.reference_doctype, ri.reference_name])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("Name")+":Link/User:180",
		_("Date")+":Date:120",
		_("Action")+"::100",
		_("Doctype")+"::150",
		_("Document")+"::130",
	]

	return columns

def get_conditions(filters):
	conditions = ""
	if filters.get("user"):
		conditions += " and `owner` = '%s'" % frappe.db.escape(filters["user"])
	if filters.get("from_date"):
		conditions += " and creation >= '%s'" % frappe.db.escape(filters["from_date"])
	if filters.get("to_date"):
		conditions += " and creation <= '%s'" % frappe.db.escape(filters["to_date"])
	return conditions

def get_entries(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""select `owner`, creation, comment_type, reference_doctype, reference_name from `tabCommunication` where docstatus != '2' %s order by creation asc""" % conditions, as_dict=1)
