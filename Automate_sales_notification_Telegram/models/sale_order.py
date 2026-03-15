# requests is a Python library that allows you to send HTTP requests easily.
# In this code, it’s used to communicate with the WhatsApp Cloud API, which is a web service endpoint hosted by Meta (Facebook) to send WhatsApp messages programmatically.
import requests   
# #Base64 is a way of converting binary data (like PDFs) into a string of text.
# WhatsApp’s API requires file attachments to be sent as Base64-encoded strings rather than raw binary files.
# Real-life analogy: Imagine trying to send a paper document over the internet; Base64 is like scanning it into a format that email systems or WhatsApp can safely transmit.      # For HTTP requests to WhatsApp API
import base64            # For encoding PDF files into Base64

#Logging is crucial in production software to track errors, warnings, or information messages.
# _logger is used to write messages to Odoo’s log system, helping the developer or business understand what happened (success/failure).
# Real-life analogy: Think of this as a diary for your system, noting every attempt to send a WhatsApp message.
import logging           # For logging errors

# models is used to define new Odoo models or extend existing ones.
# api provides decorators for Odoo’s methods (@api.model, @api.multi, etc.), helping Odoo understand how the function interacts with data.
# _ is used for translation; it marks strings to be translated in multi-language setups.

#models is a module provided by Odoo that allows you to define new models (tables) or extend existing
#Each model corresponds to a table in the database, and fields in that model are the columns.
#api provides decorators to tell Odoo how a method should behave with respect to records. 
# example @@api.depends('pages') pages is a field in the model, and this decorator tells Odoo to recompute the function whenever the pages field changes.
#example @api.depends('pages')
#self here refers to the number of books, its a set of books records.
# def _compute_reading_time(self):
# for book in self:
# when a book comes, its reading time is calculated based on its pages. we divide pages by 50 to get hours.
# book.reading_time = book.pages / 50 # assume 50 pages/hour 
from odoo import models, api, fields  # Odoo model and API decorators


from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

# Extend res.partner to add Telegram chat ID
class ResPartner(models.Model):
    _inherit = "res.partner"
    telegram_id = fields.Char("Telegram Chat ID")


# Extend sale.order to send Telegram messages
class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        """
        Confirm the sale order and send Telegram message.
        """
        res = super().action_confirm()
        self.action_send_telegram_sale()
        return res

    def action_send_telegram_sale(self):
        """
        Sends Telegram message for confirmed sale orders.
        """
        TELEGRAM_BOT_TOKEN = self.env['ir.config_parameter'].sudo().get_param('telegram_bot_token') 

        for order in self:
            try:
                chat_id = getattr(order.partner_id, 'telegram_id', False)
                if not chat_id:
                    _logger.warning("No Telegram chat ID for customer %s", order.partner_id.name)
                    continue

                message = (
                    f"Hello {order.partner_id.name},\n"
                    f"Your Sales Order {order.name} has been confirmed.\n"
                    f"Total Amount: {order.amount_total}"
                )

                telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                payload = {"chat_id": chat_id, "text": message}

                response = requests.post(telegram_url, json=payload, timeout=10)

                if response.status_code == 200:
                    _logger.info("Telegram message sent to %s for order %s", chat_id, order.name)
                else:
                    _logger.error("Telegram failed for %s | Status=%s | Response=%s",
                                  order.name, response.status_code, response.text)

            except Exception as e:
                _logger.exception("Unexpected error while sending Telegram for order %s", order.name)
