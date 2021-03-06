frappe.pages['volume-export'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Volume Export',
		single_column: true
	});
	new erpnext.VolumeExport(wrapper);
	frappe.breadcrumbs.add("Logistics")
};

erpnext.VolumeExport = frappe.views.TreeGridReport.extend({
	init: function(wrapper) {
		this._super({
			title: __("Volume Export"),
			page: wrapper,
			parent: $(wrapper).find('.layout-main'),
			page: wrapper.page,
			doctypes: ["Item", "Customer", "Customer Group", "Company",
				"Rekap Export", "Rekap Export Item"],
			tree_grid: { show: true }
		});

		this.tree_grids = {
			"Customer Group": {
				label: __("Customer Group / Customer"),
				show: true,
				item_key: "customer",
				parent_field: "parent_customer_group",
				formatter: function(item) { return item.customer_name || item.name; }
			},
			"Customer": {
				label: __("Customer"),
				show: false,
				item_key: "customer",
				formatter: function(item) {
					return item.customer_name || item.name;
				}
			}
		}
	},
	setup_columns: function() {
		this.tree_grid = this.tree_grids[this.tree_type];

		var std_columns = [
			{id: "check", name: "Plot", field: "check", width: 30,
				formatter: this.check_formatter},
			{id: "name", name: this.tree_grid.label, field: "name", width: 300,
				formatter: this.tree_formatter},
			{id: "total", name: "Total", field: "total", plot: false,
				formatter: this.currency_formatter}
		];

		this.make_date_range_columns();
		this.columns = std_columns.concat(this.columns);
	},
	filters: [
		{fieldtype:"Select", fieldname: "tree_type", label: __("Tree Type"), options:["Customer Group", "Customer"]},
		{fieldtype:"Select", fieldname: "based_on", label: __("Based On"), options:["Rekap Export"]},
		{fieldtype:"Select", fieldname: "value_or_qty", label:  __("Value or Qty"),
			options:[{label: __("Quantity"), value: "Quantity"}]},
		{fieldtype:"Date", fieldname: "from_date", label: __("From Date")},
		{fieldtype:"Label", fieldname: "to", label: __("To")},
		{fieldtype:"Date", fieldname: "to_date", label: __("To Date")},
		{fieldtype:"Select", fieldname: "company", label: __("Company"), link:"Company",
			default_value: __("Select Company...")},
		{fieldtype:"Select", label: __("Range"), fieldname: "range",
			options:[{label: __("Daily"), value: "Daily"}, {label: __("Weekly"), value: "Weekly"},
				{label: __("Monthly"), value: "Monthly"}, {label: __("Quarterly"), value: "Quarterly"},
				{label: __("Yearly"), value: "Yearly"}]}
	],
	setup_filters: function() {
		var me = this;
		this._super();

		this.trigger_refresh_on_change(["value_or_qty", "tree_type", "based_on", "company"]);

		this.show_zero_check()
		this.setup_chart_check();
	},
	init_filter_values: function() {
		this._super();
		this.filter_inputs.range.val('Monthly');
	},
	prepare_data: function() {
		var me = this;
		if (!this.tl) {
			// add 'Not Set' Customer & Item
			// (Customer / Item are not mandatory!!)
			frappe.report_dump.data["Customer"].push({
				name: "Not Set",
				parent_customer_group: "All Customer Groups",
				parent_territory: "All Territories",
				id: "Not Set",
			});

			frappe.report_dump.data["Item"].push({
				name: "Not Set",
				parent_item_group: "All Item Groups",
				id: "Not Set",
			});
		}

		if (!this.tl || !this.tl[this.based_on]) {
			this.make_transaction_list(this.based_on, this.based_on + " Item");
		}

		if(!this.data || me.item_type != me.tree_type) {
			if(me.tree_type=='Customer') {
				var items = frappe.report_dump.data["Customer"];
			} if(me.tree_type=='Customer Group') {
				var items = this.prepare_tree("Customer", "Customer Group");
			}

			me.item_type = me.tree_type
			me.parent_map = {};
			me.item_by_name = {};
			me.data = [];

			$.each(items, function(i, v) {
				var d = copy_dict(v);

				me.data.push(d);
				me.item_by_name[d.name] = d;
				if(d[me.tree_grid.parent_field]) {
					me.parent_map[d.name] = d[me.tree_grid.parent_field];
				}
				me.reset_item_values(d);
			});

			this.set_indent();

		} else {
			// otherwise, only reset values
			$.each(this.data, function(i, d) {
				me.reset_item_values(d);
			});
		}

		this.prepare_balances();
		if(me.tree_grid.show) {
			this.set_totals(false);
			this.update_groups();
		} else {
			this.set_totals(true);
		}

	},
	prepare_balances: function() {
		var me = this;
		var from_date = dateutil.str_to_obj(this.from_date);
		var to_date = dateutil.str_to_obj(this.to_date);
		var is_val = this.value_or_qty == 'Value';

		$.each(this.tl[this.based_on], function(i, tl) {
			if (me.is_default('company') ? true : tl.company === me.company) {
				var posting_date = dateutil.str_to_obj(tl.date);
				var ukuran = this.size;
				if (posting_date >= from_date && posting_date <= to_date) {
					var item = me.item_by_name[tl[me.tree_grid.item_key]] ||
						me.item_by_name['Not Set'];
					if(item){
						item[me.column_map[tl.date].field] += (is_val ? tl.base_net_amount : tl.qty);
					}
				}
			}
		});
	},
	update_groups: function() {
		var me = this;

		$.each(this.data, function(i, item) {
			var parent = me.parent_map[item.name];
			while(parent) {
				parent_group = me.item_by_name[parent];

				$.each(me.columns, function(c, col) {
					if (col.formatter == me.currency_formatter) {
						parent_group[col.field] =
							flt(parent_group[col.field])
							+ flt(item[col.field]);
					}
				});
				parent = me.parent_map[parent];
			}
		});
	},
	set_totals: function(sort) {
		var me = this;
		var checked = false;
		$.each(this.data, function(i, d) {
			d.total = 0.0;
			$.each(me.columns, function(i, col) {
				if(col.formatter==me.currency_formatter && !col.hidden && col.field!="total")
					d.total += d[col.field];
				if(d.checked) checked = true;
			})
		});

		if(sort)this.data = this.data.sort(function(a, b) { return a.total < b.total; });

		if(!this.checked) {
			this.data[0].checked = true;
		}
	}
});
