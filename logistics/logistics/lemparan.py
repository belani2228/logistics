from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

def reset_series():
	frappe.db.sql("UPDATE `tabSeries` SET current = 0 WHERE `name` = 'IMP/PTI'")

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
