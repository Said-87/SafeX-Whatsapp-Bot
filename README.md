# 🤖 SafeX WhatsApp Auto Reply Bot

A modular **WhatsApp Business Auto Reply Bot** developed using **Python**, **Flask**, **HTML**, **CSS**, and **JavaScript**. The chatbot automates customer support by answering frequently asked questions, capturing customer leads, maintaining analytics, and escalating unknown queries to a human representative.

---

# 📖 Project Overview

The SafeX WhatsApp Auto Reply Bot is designed to automate customer interactions for businesses. Instead of manually responding to repetitive customer questions, the chatbot provides instant responses using an FAQ knowledge base, collects customer information for business inquiries, and stores leads in a simple CRM.

The project demonstrates business automation concepts using a rule-based conversational system with modular architecture.

---

# ✨ Features

- 💬 Automated FAQ Responses
- 🌐 English & Urdu Language Detection
- 🧠 Smart Keyword & Synonym Matching
- 📊 Analytics Logging
- 📋 Lead Capture Workflow
- 👤 Human Agent Escalation
- 💾 CSV-based CRM
- 📱 Modern WhatsApp-inspired Dashboard
- 🔍 Confidence-based Response Matching
- 📝 Input Validation
- ⚡ Modular Flask Backend

---

# 🏗️ System Architecture

```
                    User
                      │
                      ▼
         WhatsApp Business Dashboard
                      │
                      ▼
               Flask Backend (app.py)
                      │
      ┌───────────────┼────────────────┐
      ▼               ▼                ▼
 Reply Engine   Conversation Flow   Support Modules
      │               │                │
      ▼               ▼                ▼
 FAQ Loader      Lead Capture     Analytics
 FAQ Matcher     CRM Storage      Language Detection
 Responses       CSV Database     Escalation
```

---

# 📂 Project Structure

```
SafeX-Whatsapp-Bot/

│
├── app.py
├── config.py
├── requirements.txt
│
├── reply_engine/
│   ├── faq_loader.py
│   ├── matcher.py
│   └── responses.py
│
├── conversation/
│   ├── flow.py
│   ├── crm.py
│   └── lead_capture.py
│
├── support/
│   ├── analytics.py
│   ├── escalation.py
│   └── language.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── images/
│
├── data/
│   ├── faq.csv
│   ├── analytics.csv
│   └── leads.csv
│
└── README.md
```

---

# ⚙️ Technologies Used

### Backend

- Python
- Flask

### Frontend

- HTML5
- CSS3
- JavaScript

### Database

- CSV Files

### Libraries

- Pandas
- Regex (re)
- difflib
- CSV
- Flask Session

---

# 🚀 How It Works

1. User enters a message in the chat interface.
2. Flask receives the request through the `/chat` endpoint.
3. The user's language is detected.
4. The FAQ Matcher searches the knowledge base.
5. If a suitable answer is found:
   - The chatbot replies immediately.
6. If the customer wants a service:
   - Lead capture begins.
   - Name
   - Phone
   - Email
   - Interest
7. The lead is stored in the CRM.
8. Analytics are updated.
9. Unknown questions are escalated to a human representative.

---

# 💬 Chatbot Capabilities

The chatbot can answer questions about:

- Company Information
- Services
- AI Solutions
- Machine Learning
- Web Development
- Mobile App Development
- Business Automation
- Pricing
- Internships
- Contact Information
- Technologies
- Working Hours
- Support
- Greetings
- Thank You / Goodbye

---

# 📊 Analytics

The analytics module records:

- Total Conversations
- Successful Replies
- Escalated Conversations
- Lead Captures

These statistics are displayed in the Analytics Dashboard.

---

# 📋 Lead Capture Process

When a customer requests a quotation or service, the chatbot automatically collects:

- Full Name
- Phone Number
- Email Address
- Area of Interest

The collected information is stored in:

```
data/leads.csv
```

---

# 📸 Screenshots

## Home Dashboard

![Home](screenshots/home.png)

---

## Chat Interface

![Chat](screenshots/chat.png)

---

## Analytics Dashboard

![Analytics](screenshots/analytics.png)

---

## Leads Dashboard

![Leads](screenshots/leads.png)

---

# ▶️ Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/SafeX-Whatsapp-Bot.git
```

Navigate to the project:

```bash
cd SafeX-Whatsapp-Bot
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open your browser:

```
http://127.0.0.1:5000
```

---

# 📌 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Project Status |
| GET | `/health` | Health Check |
| POST | `/chat` | Chatbot Response |
| GET | `/welcome` | Welcome Message |
| GET | `/goodbye` | Goodbye Message |
| GET | `/analytics` | Analytics Data |
| GET | `/leads` | Customer Leads |

---

# 🎯 Future Improvements

- WhatsApp Cloud API Integration
- OpenAI / LLM Integration
- MongoDB or MySQL Database
- User Authentication
- Voice Messages
- File Sharing
- Admin Dashboard
- Real-Time Notifications
- Deployment on Cloud Platforms

---

# 👨‍💻 Author

**Nasir Sajjad**

Computer Science Student

SafeX Solutions Internship Project

GitHub: https://github.com/YOUR_USERNAME

---

# 📄 License

This project was developed for educational and research purposes as part of an internship/business automation prototype.
<img width="1916" height="598" alt="Screenshot 2026-07-17 015122" src="https://github.com/user-attachments/assets/cb5d23c5-b438-449d-8dd7-eb14a8958ada" />
<img width="1912" height="942" alt="Screenshot 2026-07-17 015111" src="https://github.com/user-attachments/assets/ad83c502-5520-4947-b589-efed8c9f9007" />
