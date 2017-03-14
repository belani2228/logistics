from frappe import _

def get_data():
	return {
		'fieldname': 'no_job',
		'transactions': [
			{
				'label': _('Related'),
				'items': ['Deposite Note', 'Purchase Invoice', 'Sales Invoice', 'Penitipan Container']
			},
		]
	}
