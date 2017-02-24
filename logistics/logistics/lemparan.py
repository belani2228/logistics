from __future__ import unicode_literals
import frappe
from frappe import msgprint, _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

def reset_series():
	frappe.db.sql("""UPDATE `tabSeries` SET current = 0 WHERE `name` = 'IMP/PTI'""")

def update_deposite_note_detail(doc, method):
	args = doc.deposite_note
	name = doc.name
	for row in doc.items:
		if row.deposite_note_detail:
			doc = frappe.db.sql("""UPDATE `tabDeposite Note Item` SET pi_no = %s
			WHERE `name` = %s""", (name, row.deposite_note_detail))

	return update_deposite_note(args)

def update_deposite_note_cancel(doc, method):
	args = doc.deposite_note
	for row in doc.items:
		if row.deposite_note_detail:
			doc = frappe.db.sql("""UPDATE `tabDeposite Note Item` SET pi_no = NULL
			WHERE `name` = %s""", (row.deposite_note_detail))

	return update_deposite_note(args)

def update_deposite_note(args):
	a2 = frappe.db.sql_list("""SELECT COUNT(`name`) FROM `tabDeposite Note Item`
		WHERE parent = %s AND pi_no IS NOT NULL""", args)

	frappe.db.sql("""UPDATE `tabDeposite Note` SET terpakai = %s WHERE `name` = %s""", (a2, args))

@frappe.whitelist()
def get_items_from_pi(source_name, target_doc=None):
	no_job,rekap = source_name.split("|")

	if target_doc:
		if isinstance(target_doc, basestring):
			import json
			target_doc = frappe.get_doc(json.loads(target_doc))

	def set_missing_values(source, target):
		target.update_stock = 1
		target.run_method("set_missing_values")

	query = frappe.db.sql_list("""SELECT dn.`name`
		FROM `tabPurchase Invoice` dn
		WHERE dn.no_job = %s AND dn.docstatus != '2' ORDER BY dn.`name` ASC""", no_job)

	si = get_mapped_doc(rekap, no_job, {
		rekap: {
			"doctype": "Sales Invoice",
		},
	}, target_doc)
	for q in query:
		si = get_mapped_doc("Purchase Invoice", q, {
				"Purchase Invoice": {
					"doctype": "Sales Invoice",
					"field_no_map": [
						"base_total", "base_net_total", "net_total", "total",
						"base_grand_total", "grand_total"
					],
				},
				"Purchase Invoice Item": {
					"doctype": "Sales Invoice Item",
					"field_map": {
					},
				},
			}, target_doc, set_missing_values)

	return si

def coba_doang():
	tampung = []
	query = frappe.get_all("Purchase Invoice",
		fields=["name"],
		filters=[["docstatus", "!=", 2]],
		order_by='name asc')

	for q in query:
		tampung.append(q["name"])

	temp = ', '.join(tampung)
	frappe.throw(temp)
