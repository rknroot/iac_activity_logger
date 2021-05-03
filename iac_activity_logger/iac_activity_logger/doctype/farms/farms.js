// Copyright (c) 2021, Eco Data & IAC and contributors
// For license information, please see license.txt

frappe.ui.form.on('Farms', {
        setup: function(frm) {
                frm.set_query("supervisor", function() {
                        return {
                                filters: {'role_profile_name': "farm supervisor"}
                        }
                });
                frm.set_query("admin", function() {
                        return {
                                filters: {'role_profile_name': "farm admin"}
                        }
                });
        }
});
