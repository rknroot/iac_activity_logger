frappe.views.calendar["Tasks"] = {
	field_map: {
		// from_datetime and to_datetime don't exist as docfields but are used in onload
		"start": "from_datetime",
		"end": "to_datetime",
		"id": "name",
		"title": "task_title",
		"status": "status",
		"allDay": "allDay"
	},
	gantt: {
		"start": "from_datetime",
		"end": "to_datetime",
		"id": "name",
		"title": "task_title",
		"status": "status",
		"allDay": "allDay"
	},
	order_by: 'date',
	get_events_method: 'iac_activity_logger.iac_activity_logger.doctype.tasks.tasks.get_events'
}