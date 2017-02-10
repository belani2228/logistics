from frappe import _

def get_data():
	return {
		'fieldname': 'no_job',
		'transactions': [
			{
				'label': _('Related'),
				'items': ['Deposite Note', 'Sales Invoice', 'Purchase Invoice']
			},
		]
	}
