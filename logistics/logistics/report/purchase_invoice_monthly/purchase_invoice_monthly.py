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
		data.append([ri.pi_doc,
			ri.pi_date,
			ri.si_doc,
			ri.si_date,
			ri.item_code,
			ri.expense_account,
			ri.je_doc,
			ri.je_date,
			ri.re_doc,
			ri.re_date
	])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("Purchase Invoice")+":Link/Purchase Invoice:120",
		_("PI Date")+":Date:100",
		_("Sales Invoice")+":Link/Sales Invoice:110",
		_("SI Date")+":Date:100",
		_("Item Code")+":Data:150",
		_("Expense Account")+":Data:170",
		_("Journal Entry")+":Link/Journal Entry:110",
		_("JE Date")+":Date:100",
		_("Reversing Entry")+":Link/Journal Entry:110",
		_("RE Date")+":Date:100",
	]

	return columns

def get_conditions(filters):
	conditions = ""
	if filters.get("from_date"):
		conditions += " and a.posting_date >= '%s'" % frappe.db.escape(filters["from_date"])
	if filters.get("to_date"):
		conditions += " and a.posting_date <= '%s'" % frappe.db.escape(filters["to_date"])

	return conditions

def get_entries(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""SELECT a.`name` as pi_doc, a.posting_date as pi_date, b.item_code, b.`name` as pi_name,
	b.journal_entry as je_doc, c.posting_date as je_date, b.reversing_entry as re_doc, d.posting_date as re_date,
	b.sales_invoice as si_doc, b.expense_account, e.posting_date as si_date
	FROM `tabPurchase Invoice` a INNER JOIN `tabPurchase Invoice Item` b ON a.`name` = b.parent
	LEFT JOIN `tabJournal Entry` c ON c.`name` = b.journal_entry
	LEFT JOIN `tabJournal Entry` d ON d.`name` = b.reversing_entry
	LEFT JOIN `tabSales Invoice` e ON e.`name` = b.sales_invoice
	WHERE a.docstatus != '2' %s
	ORDER BY a.`name` ASC""" %
		conditions, as_dict=1)
