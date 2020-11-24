# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _


def get_data():
            config =  [
                {
                    "label": _("Documents"),
                    "items": [
                    
                        {
                            "type": "doctype",
                            "name": "Client Request CT",
                            "label": _("Client Request"),
                        }
                        
                    ]
                },
                {
                    "label": _("Reports"),
                    "items": [
                                {
                                        "type": "report",
                                        "name": "Siwar Sales",
                                        "is_query_report": True,
                                        "doctype": "File"
                                }
                        ]
                }
                
            ]
            return config


