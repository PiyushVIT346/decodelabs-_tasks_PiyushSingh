# Week 1 project
---
# 🤖 AI Chatbot with Persistent Memory & Storage Inspector

A full-stack AI chatbot built with **Flask**, **LangChain**, **Google Gemini**, and **SQLite** that provides persistent conversation memory, secure user authentication, and real-time database activity monitoring.

Unlike a traditional chatbot, this project stores every conversation in a SQLite database using LangChain's `SQLChatMessageHistory`, allowing users to continue conversations with contextual memory across sessions. It also includes a **Storage Inspector** that visualizes database statistics and storage events in real time.

---

# ✨ Features

* 🔐 User Registration & Login Authentication
* 🤖 AI-powered chatbot using Google Gemini
* 🧠 Persistent conversation memory using LangChain
* 💾 SQLite database for user accounts and chat history
* 📜 Automatic storage event logging (ledger)
* 📊 Real-time Storage Inspector
* 📚 Conversation history retrieval
* 🔒 Password hashing using Werkzeug
* 🎯 Modular Flask architecture

---

# 🏗️ Project Architecture

```
                User
                  │
                  ▼
            Flask (app.py)
                  │
     ┌────────────┴─────────────┐
     │                          │
Authentication              Chat API
     │                          │
     ▼                          ▼
 storage.py                chain.py
     │                          │
     │                 LangChain Pipeline
     │                          │
     │               Google Gemini LLM
     │                          │
     └──────────────┬───────────┘
                    ▼
              SQLite Database
       (Users + Chat History + Ledger)
```

---

# 📂 Project Structure

```
project/
│
├── app.py               # Flask application & routes
├── chain.py             # LangChain pipeline
├── storage.py           # Database operations
│
├── templates/
│   ├── login.html
│   ├── register.html
│   └── chat.html
│
├── static/
│   ├── css/
│   └── js/
│
├── app_data.db          # SQLite database
│
├── requirements.txt
└── README.md
```

---

# ⚙️ Technologies Used

| Technology            | Purpose               |
| --------------------- | --------------------- |
| Python                | Backend               |
| Flask                 | Web framework         |
| LangChain             | Conversation pipeline |
| Google Gemini         | Large Language Model  |
| SQLite                | Persistent storage    |
| SQLChatMessageHistory | Conversation memory   |
| Werkzeug              | Password hashing      |
| HTML/CSS/JavaScript   | Frontend              |

---

# 🔄 Application Workflow

1. User registers an account.
2. Password is securely hashed and stored.
3. User logs in.
4. Flask creates a session.
5. User sends a message.
6. LangChain loads previous conversation history.
7. Gemini generates a contextual response.
8. Both user and AI messages are stored in SQLite.
9. Storage events are recorded in the audit ledger.
10. Storage Inspector updates with new database statistics.

---

# 🧠 Conversation Memory

Instead of storing messages temporarily, the chatbot uses LangChain's `SQLChatMessageHistory`.

Each authenticated user receives a unique session ID:

```
session_default_user_<username>
```

This enables:

* Persistent chat history
* Context-aware responses
* Conversation continuity after page refresh
* Multiple independent user conversations

---

# 🔐 Authentication

The application provides secure authentication using Flask sessions.

### Registration

* Username normalization
* Password hashing
* Duplicate username prevention

### Login

* Password verification
* Session creation
* Secure authentication flow

Passwords are never stored in plaintext.

---

# 🤖 AI Chat Pipeline

The chatbot pipeline is built using LangChain.

```
User Input
      │
      ▼
Prompt Template
      │
      ▼
Conversation History
      │
      ▼
Gemini 2.5 Flash
      │
      ▼
Output Parser
      │
      ▼
Response
```

The prompt consists of:

* System instruction
* Previous conversation history
* Current user message

This allows the model to generate context-aware responses.

---

# 💾 Database Design

## Users Table

Stores authentication information.

| Column        | Description            |
| ------------- | ---------------------- |
| username      | Primary Key            |
| password_hash | Hashed password        |
| created_at    | Registration timestamp |

---

## Message Store

Managed automatically by LangChain.

Stores:

* User messages
* AI responses
* Session IDs
* Conversation history

---

## Storage Ledger

Maintains an audit log of application events.

Examples include:

* User registration
* Successful login
* Failed login
* User message insertion
* AI response insertion

---

# 📊 Storage Inspector

A unique feature of this project.

The Storage Inspector displays:

* Database file size
* Database name
* Table row counts
* Session message count
* Recent storage activity
* Storage event timeline

This makes it easy to visualize how the application interacts with persistent storage.

---

# 🌐 API Endpoints

| Endpoint       | Method   | Description                   |
| -------------- | -------- | ----------------------------- |
| `/`            | GET      | Redirects user                |
| `/register`    | GET/POST | Register new user             |
| `/login`       | GET/POST | Login                         |
| `/logout`      | GET      | Logout                        |
| `/chat`        | GET      | Chat interface                |
| `/api/chat`    | POST     | Send chat message             |
| `/api/history` | GET      | Retrieve conversation history |
| `/api/storage` | GET      | Retrieve storage statistics   |

---

# 🔒 Security Features

* Password hashing using Werkzeug
* Session-based authentication
* Login protection with decorators
* SQL parameterized queries
* No plaintext password storage
* Server-side session management

---

# 🚀 Installation

```bash
git clone <repository-url>

cd project

pip install -r requirements
```

Create a `.env` file (or export the environment variables) with:

```env
GOOGLE_API_KEY=your_google_api_key
FLASK_SECRET_KEY=your_secret_key
```

Run the application:

```bash
python app.py
```

Open:

```
http://localhost:5000
```

---

