# 17-Odoo-Telegram-Integration for Automating Sales Notification


This module automatically sends a **Telegram notification** to customers when a Sales Order is confirmed.

The module extends Odoo's Sales workflow and integrates with the **Telegram Bot API** to notify customers in real time.

---

# Features

• Extend partner model with Telegram Chat ID  
• Automatic Telegram notification on Sales Order confirmation  
• External API integration using Telegram Bot API  
• Logging and error handling for message delivery  

---

# How It Works

1. A Telegram Chat ID is stored on the customer record.
2. When a Sales Order is confirmed, the system triggers a notification.
3. The system calls the Telegram Bot API.
4. The customer receives a confirmation message.

---

# Architecture

```
Sales Order Confirmation
        │
        ▼
action_confirm() Override
        │
        ▼
Fetch Partner Telegram ID
        │
        ▼
Send Message via Telegram Bot API
```

---

# Technologies Used

• Python  
• Odoo ORM  
• XML View Inheritance  
• Telegram Bot API  
• HTTP Requests  

---

# Configuration

1. Create a Telegram Bot using **BotFather**
2. Get your Bot Token
3. Add system parameter in Odoo:

```
telegram_bot_token
```

---

# Example Notification

```
Hello John,

Your Sales Order SO023 has been confirmed.

Total Amount: $450
```

---

# Author

Hamza Ahmed  
Odoo Developer
