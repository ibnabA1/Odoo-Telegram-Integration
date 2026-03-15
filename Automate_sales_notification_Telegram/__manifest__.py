{
    "name": "Telegram Sales Order Automation",
    "version": "1.0",
    "category": "Sales",
    "summary": "Telegram Sales Order Automation",
    "depends": ["sale", "mail"],  # Ensures Sales & Mail modules are installed
    "data": [
        "data/mail_template.xml",         # if exists, otherwise remove this line
        "views/res_partner_views.xml",    # XML view for Telegram field
    ],
    "installable": True,
    "application": True
}
