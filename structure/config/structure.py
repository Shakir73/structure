from __future__ import unicode_literals
from frappe import _

def get_data():
    return [
      {
        "label":_("Initialization"),
        "icon": "octicon octicon-briefcase",
        "items": [
            {
              "type": "doctype",
              "name": "Company",
              "label": _("Company"),
              "description": _("Articles which members issue and return."),
            },

            {
              "type": "doctype",
              "name": "Naming Series",
              "label": _("Naming Series"),
              "description": _("Articles which members issue and return."),
            },

          ]
      }
  ]
