from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, flt
from frappe import msgprint, _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

def update_doctype_related_with_sinv(doc, method):
	sinv = doc.name
	no_job = frappe.db.get_value("Sales Invoice", sinv, "no_job")
	if no_job:
		jc = frappe.db.get_value("Job Cost", {"no_job": no_job}, "name")
		if jc:
			update_pi_from_sinv(sinv)
#			update_jc_item_from_sinv(sinv, jc)
#			update_jc_tax_from_sinv(sinv, jc)
#			update_jc_from_sinv(sinv, jc)

def update_pi_from_sinv(sinv):
	sii = frappe.db.sql("""select purchase_invoice, purchase_invoice_item from `tabSales Invoice Item` where parent = %s""", sinv, as_dict=1)
	for row in sii:
		if row.purchase_invoice:
			pii = frappe.get_doc("Purchase Invoice Item", row.purchase_invoice_item)
			pii.sales_invoice = sinv
			pii.save()

def update_jc_item_from_sinv(sinv, jc):
	sinv_items = frappe.db.sql("""select * from `tabSales Invoice Item` where parent = %s order by idx asc""", sinv, as_dict=1)
	for row in sinv_items:
		jci = frappe.db.get_value("Job Cost Item", {"parent": jc, "item_code": row.item_code}, "name")
		if jci:
			sell = frappe.db.get_value("Job Cost Item", jci, "selling")
			job_cost_item = frappe.get_doc("Job Cost Item", jci)
			sell = sell + row.amount
			job_cost_item.selling = sell
			job_cost_item.save()
		else:
			job_cost_item = frappe.get_doc({
				"doctype": "Job Cost Item",
				"parent": jc,
				"parentfield": "items",
				"parenttype": "Job Cost",
				"item_code": row.item_code,
				"item_name": row.item_name,
				"description": row.description,
				"selling": row.amount
			})
			job_cost_item.insert()

def update_jc_tax_from_sinv(sinv, jc):
	sinv_taxes = frappe.db.sql("""select * from `tabSales Taxes and Charges` where parent = %s order by idx asc""", sinv, as_dict=1)
	for tax in sinv_taxes:
		jct = frappe.db.get_value("Job Cost Tax", {"parent": jc, "account_head": tax.account_head}, "name")
		if jct:
			tax_sell = frappe.db.get_value("Job Cost Tax", jct, "selling_tax_amount")
			job_cost_tax = frappe.get_doc("Job Cost Tax", jct)
			tax_sell = tax_sell + tax.tax_amount
			job_cost_tax.selling_tax_amount = tax_sell
			job_cost_tax.save()
		else:
			job_cost_tax = frappe.get_doc({
				"doctype": "Job Cost Tax",
				"parent": jc,
				"parentfield": "taxes",
				"parenttype": "Job Cost",
				"account_head": tax.account_head,
				"description": tax.description,
				"selling_tax_amount": tax.tax_amount
			})
			job_cost_tax.insert()

def update_jc_from_sinv(sinv, jc):
	sum_sell_item = frappe.db.sql("""select sum(`selling`) from `tabJob Cost Item` where parent = %s""", jc)[0][0]
	sum_sell_tax = frappe.db.sql("""select sum(`selling_tax_amount`) from `tabJob Cost Tax` where parent = %s""", jc)[0][0]
	sum_buy_item = frappe.db.sql("""select sum(`cost`) from `tabJob Cost Item` where parent = %s""", jc)[0][0]
	sum_buy_tax = frappe.db.sql("""select sum(`cost_tax_amount`) from `tabJob Cost Tax` where parent = %s""", jc)[0][0]
	total_selling = flt(sum_sell_item) + flt(sum_sell_tax)
	total_buying = flt(sum_buy_item) + flt(sum_buy_tax)
	profit = flt(total_selling) - flt(total_buying)
	job_cost = frappe.get_doc("Job Cost", jc)
	job_cost.total_selling = total_selling
	job_cost.profit_loss = profit
	job_cost.save()

def cancel_doctype_related_with_sinv(doc, method):
	sinv = doc.name
	no_job = frappe.db.get_value("Sales Invoice", sinv, "no_job")
	if no_job:
		jc = frappe.db.get_value("Job Cost", {"no_job": no_job}, "name")
		if jc:
			cancel_pi_from_sinv(sinv)
#			cancel_jc_item_from_sinv(sinv, jc)
#			cancel_jc_tax_from_sinv(sinv, jc)
#			update_jc_from_sinv(sinv, jc)
#			delete_job_cost(jc)

def cancel_pi_from_sinv(sinv):
	sii = frappe.db.sql("""select * from `tabSales Invoice Item` where parent = %s""", sinv, as_dict=1)
	for row in sii:
		if row.purchase_invoice:
			pii = frappe.get_doc("Purchase Invoice Item", row.purchase_invoice_item)
			pii.sales_invoice = None
			pii.save()

def cancel_jc_item_from_sinv(sinv, jc):
	sinv_items = frappe.db.sql("""select * from `tabSales Invoice Item` where parent = %s order by idx asc""", sinv, as_dict=1)
	for row in sinv_items:
		jci = frappe.db.get_value("Job Cost Item", {"parent": jc, "item_code": row.item_code}, "name")
		if jci:
			sell = frappe.db.get_value("Job Cost Item", jci, "selling")
			job_cost_item = frappe.get_doc("Job Cost Item", jci)
			sell = sell - row.amount
			job_cost_item.selling = sell
			job_cost_item.save()

def cancel_jc_tax_from_sinv(sinv, jc):
	sinv_taxes = frappe.db.sql("""select * from `tabSales Taxes and Charges` where parent = %s order by idx asc""", sinv, as_dict=1)
	for tax in sinv_taxes:
		jct = frappe.db.get_value("Job Cost Tax", {"parent": jc, "account_head": tax.account_head}, "name")
		if jct:
			tax_sell = frappe.db.get_value("Job Cost Tax", jct, "selling_tax_amount")
			job_cost_tax = frappe.get_doc("Job Cost Tax", jct)
			tax_sell = tax_sell - tax.tax_amount
			job_cost_tax.selling_tax_amount = tax_sell
			job_cost_tax.save()

def delete_job_cost(jc):
	jc_items = frappe.db.sql("""select * from `tabJob Cost Item` where parent = %s order by idx asc""", jc, as_dict=1)
	for row in jc_items:
		if row.cost <= 0 and row.selling <= 0:
			job_cost_item = frappe.get_doc("Job Cost Item", row.name)
			job_cost_item.delete()
	jc_tax = frappe.db.sql("""select * from `tabJob Cost Tax` where parent = %s order by idx asc""", jc, as_dict=1)
	for rt in jc_tax:
		if rt.cost_tax_amount <= 0 and rt.selling_tax_amount <= 0:
			job_cost_tax = frappe.get_doc("Job Cost Tax", rt.name)
			job_cost_tax.delete()

# Semua yang berhubungan dengan Purchase Invoice
def update_doctype_related_with_pinv(doc, method):
	pinv = doc.name
	no_job = frappe.db.get_value("Purchase Invoice", pinv, "no_job")
	if no_job:
		jc = frappe.db.get_value("Job Cost", {"no_job": no_job}, "name")
		if jc:
			update_dni_from_pinv(pinv)
			update_dn_from_pinv(pinv)
			update_jc_item_from_pinv(pinv, jc)
			update_jc_tax_from_pinv(pinv, jc)
			update_jc_from_pinv(pinv, jc)
			update_vt_from_pinv(pinv)

def update_dni_from_pinv(pinv):
	pii = frappe.db.sql("""select * from `tabPurchase Invoice Item` where parent = %s order by idx asc""", pinv, as_dict=1)
	for row in pii:
		if row.deposite_note_detail:
			dni = frappe.get_doc("Deposite Note Item", row.deposite_note_detail)
			dni.pi_no = pinv
			dni.save()

def update_dn_from_pinv(pinv):
	dn = frappe.db.get_value("Purchase Invoice", pinv, "deposite_note")
	if dn:
		count = frappe.db.sql("""select count(*) from `tabDeposite Note Item` where parent = %s and pi_no is not null""", dn)[0][0]
		if cstr(count) != 0:
			deposite_note = frappe.get_doc("Deposite Note", dn)
			deposite_note.terpakai = count
			deposite_note.save()

def update_jc_item_from_pinv(pinv, jc):
	pinv_items = frappe.db.sql("""select * from `tabPurchase Invoice Item` where parent = %s order by idx asc""", pinv, as_dict=1)
	for row in pinv_items:
		jci = frappe.db.get_value("Job Cost Item", {"parent": jc, "item_code": row.item_code}, "name")
		if jci:
			cost = frappe.db.get_value("Job Cost Item", jci, "cost")
			job_cost_item = frappe.get_doc("Job Cost Item", jci)
			cost = cost + row.amount
			job_cost_item.cost = cost
			job_cost_item.save()
		else:
			job_cost_item = frappe.get_doc({
				"doctype": "Job Cost Item",
				"parent": jc,
				"parentfield": "items",
				"parenttype": "Job Cost",
				"item_code": row.item_code,
				"item_name": row.item_name,
				"description": row.description,
				"cost": row.amount
			})
			job_cost_item.insert()

def update_jc_tax_from_pinv(pinv, jc):
	pinv_taxes = frappe.db.sql("""select * from `tabPurchase Taxes and Charges` where parent = %s order by idx asc""", pinv, as_dict=1)
	for tax in pinv_taxes:
		jct = frappe.db.get_value("Job Cost Tax", {"parent": jc, "account_head": tax.account_head}, "name")
		if jct:
			tax_buy = frappe.db.get_value("Job Cost Tax", jct, "cost_tax_amount")
			job_cost_tax = frappe.get_doc("Job Cost Tax", jct)
			tax_sell = tax_buy + tax.tax_amount
			job_cost_tax.cost_tax_amount = tax_sell
			job_cost_tax.save()
		else:
			job_cost_tax = frappe.get_doc({
				"doctype": "Job Cost Tax",
				"parent": jc,
				"parentfield": "taxes",
				"parenttype": "Job Cost",
				"account_head": tax.account_head,
				"description": tax.description,
				"cost_tax_amount": tax.tax_amount
			})
			job_cost_tax.insert()

def update_jc_from_pinv(pinv, jc):
	sum_sell_item = frappe.db.sql("""select sum(`selling`) from `tabJob Cost Item` where parent = %s""", jc)[0][0]
	sum_sell_tax = frappe.db.sql("""select sum(`selling_tax_amount`) from `tabJob Cost Tax` where parent = %s""", jc)[0][0]
	sum_buy_item = frappe.db.sql("""select sum(`cost`) from `tabJob Cost Item` where parent = %s""", jc)[0][0]
	sum_buy_tax = frappe.db.sql("""select sum(`cost_tax_amount`) from `tabJob Cost Tax` where parent = %s""", jc)[0][0]
	total_selling = flt(sum_sell_item) + flt(sum_sell_tax)
	total_buying = flt(sum_buy_item) + flt(sum_buy_tax)
	profit = flt(total_selling) - flt(total_buying)
	job_cost = frappe.get_doc("Job Cost", jc)
	job_cost.total_cost = total_buying
	job_cost.profit_loss = profit
	job_cost.save()

def update_vt_from_pinv(pinv):
	pinv_items = frappe.db.sql("""select * from `tabPurchase Invoice Item` where parent = %s order by idx asc""", pinv, as_dict=1)
	for row in pinv_items:
		if row.vendor_trucking_item:
			vti = frappe.get_doc("Vendor Trucking Item", row.vendor_trucking_item)
			vti.purchase_invoice = pinv
			vti.save()

def cancel_doctype_related_with_pinv(doc, method):
	pinv = doc.name
	no_job = frappe.db.get_value("Purchase Invoice", pinv, "no_job")
	if no_job:
		jc = frappe.db.get_value("Job Cost", {"no_job": no_job}, "name")
		if jc:
			cancel_dni_from_pinv(pinv)
			cancel_dn_from_pinv(pinv)
			cancel_jc_item_from_pinv(pinv, jc)
			cancel_jc_tax_from_pinv(pinv, jc)
			update_jc_from_pinv(pinv, jc)
			cancel_vt_from_pinv(pinv)
			delete_job_cost(jc)

def cancel_dni_from_pinv(pinv):
	pii = frappe.db.sql("""select * from `tabPurchase Invoice Item` where parent = %s order by idx asc""", pinv, as_dict=1)
	for row in pii:
		if row.deposite_note_detail:
			dni = frappe.get_doc("Deposite Note Item", row.deposite_note_detail)
			dni.pi_no = None
			dni.save()

def cancel_dn_from_pinv(pinv):
	dn = frappe.db.get_value("Purchase Invoice", pinv, "deposite_note")
	if dn:
		count = frappe.db.sql("""select count(*) from `tabDeposite Note Item` where parent = %s and pi_no is not null""", dn)[0][0]
		if cstr(count) != 0:
			deposite_note = frappe.get_doc("Deposite Note", dn)
			deposite_note.terpakai = count
			deposite_note.save()

def cancel_jc_item_from_pinv(pinv, jc):
	pinv_items = frappe.db.sql("""select * from `tabPurchase Invoice Item` where parent = %s order by idx asc""", pinv, as_dict=1)
	for row in pinv_items:
		jci = frappe.db.get_value("Job Cost Item", {"parent": jc, "item_code": row.item_code}, "name")
		if jci:
			cost = frappe.db.get_value("Job Cost Item", jci, "cost")
			job_cost_item = frappe.get_doc("Job Cost Item", jci)
			cost = cost - row.amount
			job_cost_item.cost = cost
			job_cost_item.save()

def cancel_jc_tax_from_pinv(pinv, jc):
	pinv_taxes = frappe.db.sql("""select * from `tabPurchase Taxes and Charges` where parent = %s order by idx asc""", pinv, as_dict=1)
	for tax in pinv_taxes:
		jct = frappe.db.get_value("Job Cost Tax", {"parent": jc, "account_head": tax.account_head}, "name")
		if jct:
			tax_buy = frappe.db.get_value("Job Cost Tax", jct, "cost_tax_amount")
			job_cost_tax = frappe.get_doc("Job Cost Tax", jct)
			tax_sell = tax_buy - tax.tax_amount
			job_cost_tax.cost_tax_amount = tax_sell
			job_cost_tax.save()

def cancel_vt_from_pinv(pinv):
	pinv_items = frappe.db.sql("""select * from `tabPurchase Invoice Item` where parent = %s order by idx asc""", pinv, as_dict=1)
	for row in pinv_items:
		if row.vendor_trucking_item:
			vti = frappe.get_doc("Vendor Trucking Item", row.vendor_trucking_item)
			vti.purchase_invoice = None
			vti.save()
