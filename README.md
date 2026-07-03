# Week 1 project

![Project Demo](https://raw.githubusercontent.com/PiyushVIT346/decodelabs-_tasks_PiyushSingh/main/week1/demo.jpg)
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
git clone https://github.com/PiyushVIT346/decodelabs-_tasks_PiyushSingh.git

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

# Week 2 Project
## 📸 Sample Outputs

| LinkedIn Output | Email Output |
|-----------------|--------------|
| <img src="https://raw.githubusercontent.com/PiyushVIT346/decodelabs-_tasks_PiyushSingh/main/week2/linkedin_output.jpg" alt="LinkedIn Output" width="450"> | <img src="https://raw.githubusercontent.com/PiyushVIT346/decodelabs-_tasks_PiyushSingh/main/week2/email_output.jpg" alt="Email Output" width="450"> |
# 🚀 AI Marketing Copy Generator

An AI-powered web application that generates platform-specific marketing content using **Google Gemini**, **Flask**, and **Python**. Users can provide a product name and description, choose a target platform, and instantly receive professionally formatted marketing copy tailored to that platform.

The application automatically adapts the tone and writing style for different platforms such as **LinkedIn**, **Instagram**, and **Email**, making it easy to create engaging marketing content in seconds.

---

## ✨ Features

* 🤖 AI-powered marketing copy generation using Google Gemini
* 🌐 Flask-based web application
* 🎯 Platform-specific content generation
* ✍️ Automatic tone adaptation
* 📝 Markdown-formatted output
* ⚙️ Adjustable AI parameters (Temperature & Top-P)
* ✅ Input validation with user-friendly error messages
* 🔄 Automatic retry with exponential backoff for API failures
* 🏗️ Modular and maintainable architecture

---

## 🏗️ Project Architecture

```text
                    User
                      │
                      ▼
              Flask Web Interface
                  (app.py)
                      │
                      ▼
          Request Validation Layer
                      │
                      ▼
        Marketing Copy Generator
              (generator.py)
                      │
        ┌─────────────┴─────────────┐
        │                           │
 Prompt Construction         Generation Config
        │                           │
        └─────────────┬─────────────┘
                      ▼
         Google Gemini 2.5 Flash API
                      │
                      ▼
          Markdown Marketing Copy
                      │
                      ▼
              JSON Response
```

---

## 📂 Project Structure

```text
AI-Marketing-Copy-Generator/
│
├── app.py                  # Flask application and API routes
├── generator.py            # Gemini integration and prompt generation
├── templates/
│   └── index.html          # Frontend interface
├── static/
│   ├── css/
│   └── js/
├── requirements.txt
└── README.md
```

---

## 🛠️ Technologies Used

| Technology              | Purpose                |
| ----------------------- | ---------------------- |
| Python                  | Backend development    |
| Flask                   | Web framework          |
| Google Gemini 2.5 Flash | AI text generation     |
| Google GenAI SDK        | Gemini API integration |
| HTML                    | User interface         |
| CSS                     | Styling                |
| JavaScript              | Frontend interactions  |
| Markdown                | AI response formatting |

---

## ⚙️ How It Works

1. User enters a product name.
2. User provides a product description.
3. User selects the target platform.
4. User adjusts AI parameters (Temperature and Top-P).
5. Flask validates the input.
6. A platform-specific prompt is generated.
7. Google Gemini generates tailored marketing content.
8. The generated Markdown is returned to the frontend and displayed to the user.

---

## 🎯 Supported Platforms

The application currently supports customized content generation for:

| Platform  | Writing Style                                       |
| --------- | --------------------------------------------------- |
| LinkedIn  | Professional, business-oriented, thought leadership |
| Instagram | Trendy, engaging, lifestyle-focused                 |
| Email     | Persuasive, direct, conversion-focused              |

Adding new platforms only requires extending the `PLATFORM_TONES` dictionary in `generator.py`.

---

## 🧠 Prompt Engineering

The application dynamically constructs prompts containing:

* Product name
* Product description
* Target platform
* Platform-specific tone
* Formatting instructions
* Markdown output requirements

This ensures the generated content is optimized for the selected platform while maintaining consistent formatting.

---

## ⚙️ AI Generation Parameters

Users can customize the AI generation behavior through:

### Temperature

Controls creativity.

| Value | Effect               |
| ----- | -------------------- |
| 0.0   | Highly deterministic |
| 0.5   | Balanced responses   |
| 1.0+  | More creative        |
| 2.0   | Maximum creativity   |

---

### Top-P

Controls response diversity.

| Value | Effect                    |
| ----- | ------------------------- |
| 0.1   | Conservative responses    |
| 0.5   | Moderate diversity        |
| 0.9   | Natural and varied output |
| 1.0   | Maximum diversity         |

---

## 🔄 Error Handling

The application includes robust validation and recovery mechanisms:

* Missing product name validation
* Missing description validation
* Invalid platform detection
* Temperature range validation
* Top-P range validation
* API error handling
* Automatic retry on rate limits (429)
* Automatic retry on temporary server errors (503)
* Exponential backoff (1s → 2s → 4s)

---

## 🌐 API Endpoints

### Home Page

```http
GET /
```

Returns the web interface.

---

### Generate Marketing Copy

```http
POST /generate
```

### Request

```json
{
  "product_name": "ErgoChair",
  "description": "An ergonomic office chair with adjustable lumbar support.",
  "platform": "LinkedIn",
  "temperature": 0.7,
  "top_p": 0.9
}
```

### Successful Response

```json
{
  "markdown": "# Introducing ErgoChair\n\n..."
}
```

### Error Response

```json
{
  "error": "Product name and description are required."
}
```

---

## 🚀 Installation


### Clone the repository

```bash
git clone https://github.com/PiyushVIT346/decodelabs-_tasks_PiyushSingh.git
cd AI-Marketing-Copy-Generator
```

### Install dependencies

```bash
pip install -r requirements
```

### Set the Gemini API Key

**Windows**

```cmd
set GEMINI_API_KEY=your_api_key
```

**Linux / macOS**

```bash
export GEMINI_API_KEY=your_api_key
```

Alternatively, update the API key initialization in `generator.py`.

---

### Run the application

```bash
python app.py
```

Open your browser and visit:

```text
http://localhost:5000
```

---

## 📈 Example Workflow

```text
User Input
     │
     ▼
Product Information
     │
     ▼
Platform Selection
     │
     ▼
Prompt Generation
     │
     ▼
Google Gemini API
     │
     ▼
Markdown Marketing Copy
     │
     ▼
Displayed in Browser
```
---
# Week 3 Project
---
## 📸 Generated Image

![Generated Image](https://raw.githubusercontent.com/PiyushVIT346/decodelabs-_tasks_PiyushSingh/main/week3/image.jpg)
# 🎨 AI Image Generation Studio

An AI-powered web application built with **Flask** that generates high-quality images from text prompts using the **Pollinations AI Image API**. Users can customize image generation by selecting different AI models, aspect ratios, resolutions, random seeds, and enhancement options through an intuitive web interface.

The application follows a modular architecture by separating the Flask API layer from the image generation service, making it easy to maintain, test, and extend.

---

# ✨ Features

* 🎨 Generate AI images from text prompts
* 🤖 Multiple AI image generation models
* 📐 Select different aspect ratios
* 🖼️ Standard and high-resolution image generation
* 🎲 Custom or random seed support
* ⚡ Automatic retry for transient API failures
* 🛡️ Robust error handling and validation
* 🔄 Base64 image delivery for instant browser rendering
* 🏗️ Modular Flask architecture

---

# 🏗️ Project Architecture

```text
                    User
                      │
                      ▼
             Web Interface (HTML)
                      │
                      ▼
              Flask Backend (app.py)
                      │
          JSON Request Validation
                      │
                      ▼
          Image Service (image_service.py)
                      │
        ┌─────────────┴─────────────┐
        │                           │
 Parameter Processing       Dimension Resolution
        │                           │
        └─────────────┬─────────────┘
                      ▼
            Pollinations Image API
                      │
                      ▼
              PNG Image Response
                      │
                      ▼
           Base64 Image Encoding
                      │
                      ▼
              Browser Rendering
```

---

# 📂 Project Structure

```text
AI-Image-Generation-Studio/
│
├── app.py                 # Flask application and API routes
├── image_service.py       # Image generation service
├── templates/
│   └── index.html         # Frontend interface
├── static/
│   ├── css/
│   └── js/
├── requirements.txt
└── README.md
```

---

# 🛠️ Technologies Used

| Technology      | Purpose                 |
| --------------- | ----------------------- |
| Python          | Backend development     |
| Flask           | Web framework           |
| Pollinations AI | Image generation API    |
| Requests        | HTTP communication      |
| HTML            | User interface          |
| CSS             | Styling                 |
| JavaScript      | Frontend interactions   |
| Base64 Encoding | Browser image rendering |

---

# ⚙️ How It Works

1. User enters a text prompt.
2. User selects generation settings.
3. Flask validates the request.
4. The image generation service processes the parameters.
5. A request is sent to the Pollinations Image API.
6. The generated PNG image is received.
7. The image is encoded into Base64.
8. The frontend displays the generated image instantly.

---

# 🎛️ Supported Models

The application currently supports the following AI image models:

| Model        | Description                      |
| ------------ | -------------------------------- |
| flux         | General-purpose image generation |
| flux-realism | Realistic images                 |
| flux-anime   | Anime-style artwork              |
| flux-3d      | 3D rendered illustrations        |
| turbo        | Faster image generation          |

New models can be added by extending the `SUPPORTED_MODELS` list in `image_service.py`.

---

# 📐 Supported Aspect Ratios

| Aspect Ratio | Common Use                         |
| ------------ | ---------------------------------- |
| 1:1          | Square social media posts          |
| 16:9         | Landscape images and presentations |
| 9:16         | Mobile wallpapers and stories      |
| 4:3          | Standard photography               |

---

# 🖼️ Resolution Options

| Option   | Base Resolution |
| -------- | --------------- |
| Standard | 768 px          |
| High     | 1024 px         |

The final image dimensions are automatically calculated based on the selected aspect ratio.

---

# 🎲 Seed Support

The application supports deterministic image generation.

* **Custom Seed** – Reproduce the same image consistently.
* **Random Seed** – Automatically generates a random seed for unique outputs.

This is useful for experimentation and reproducibility.

---

# 🌐 API Endpoint

## Generate Image

```http
POST /api/generate
```

### Request

```json
{
  "prompt": "A futuristic cyberpunk city at sunset",
  "aspect_ratio": "16:9",
  "resolution_scale": "high",
  "seed": 12345,
  "model": "flux",
  "enhance": true,
  "nologo": true,
  "private": true
}
```

### Successful Response

```json
{
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUg..."
}
```

### Error Response

```json
{
  "error": "Prompt cannot be empty."
}
```

---

# 🔄 Error Handling

The application includes comprehensive validation and recovery mechanisms.

### Input Validation

* Empty prompt detection
* Invalid parameter handling
* Invalid seed validation
* Unsupported model fallback

### Network Reliability

* Automatic retry (up to 3 attempts)
* Exponential backoff
* Connection timeout handling
* HTTP error handling
* Response validation

---

# 🚀 Installation

## Clone the repository

```bash
git clone https://github.com/PiyushVIT346/decodelabs-_tasks_PiyushSingh.git

cd AI-Image-Generation-Studio
```

## Install dependencies

```bash
pip install -r requirements
```

## Run the application

```bash
python app.py
```

Open your browser and visit:

```text
http://localhost:5000
```

---

# 📈 Image Generation Workflow

```text
User Prompt
     │
     ▼
Flask API
     │
     ▼
Input Validation
     │
     ▼
Dimension Calculation
     │
     ▼
Pollinations API Request
     │
     ▼
PNG Image
     │
     ▼
Base64 Encoding
     │
     ▼
Browser Display
```

---

# 🔒 Reliability Features

* Modular application design
* Automatic retry with backoff
* Timeout protection
* Robust exception handling
* Clean separation of concerns
* Reusable image service
* Input validation
* Safe API parameter processing

---

# 🔮 Future Improvements

* Image history
* Prompt templates
* Negative prompt support
* Batch image generation
* Image download button
* User authentication
* Favorite prompts
* Image gallery
* Additional AI providers (Stable Diffusion, OpenAI, etc.)
* Image editing and variation generation
* Prompt enhancement using AI

---



