# 🎥 AI Video Meeting Assistant

An AI-powered Video Meeting Assistant that transcribes videos, generates intelligent summaries, extracts action items, identifies key decisions, answers questions using Retrieval-Augmented Generation (RAG), and supports both English and Hinglish videos.

Built using **Python, Streamlit, Whisper, LangChain, ChromaDB, Mistral AI, and Sarvam AI**.

---

## 🚀 Live Demo

🔗 **Live App:** https://ai-video-agent-lgrtgpxpdkc3xapgjadphk.streamlit.app/

🔗 **GitHub Repository:** https://github.com/Shrutirowlo/AI-Video-Agent

---

# ✨ Features

### 🎙️ Speech-to-Text
- Transcribes English videos using OpenAI Whisper.
- Supports Hinglish/Hindi videos using Sarvam AI Speech-to-Text Translation API.

### 📑 AI Meeting Summary
- Generates concise meeting summaries.
- Uses LangChain Map-Reduce summarization.
- Handles long transcripts efficiently.

### 📝 Meeting Title Generation
- Automatically creates a professional meeting title.

### ✅ Action Item Extraction
Extracts:
- Task description
- Responsible person (Owner)
- Deadline (if available)

### 🔑 Key Decision Extraction
Identifies important decisions taken during the meeting.

### ❓ Open Questions
Extracts unanswered questions and follow-up items.

### 💬 Chat with Meeting (RAG)
Ask natural language questions such as:

- What was the main discussion?
- What decisions were taken?
- Who is responsible for the deployment?
- What are the action items?

Uses:
- ChromaDB Vector Database
- Sentence Transformers
- LangChain Retrieval
- Mistral AI

### 🌐 User-Friendly Interface
- Upload audio/video files
- Paste YouTube links
- View transcript
- View summary
- Chat with meeting

---

# 🛠️ Tech Stack

## Frontend
- Streamlit

## Backend
- Python

## AI Models
- OpenAI Whisper
- Sarvam AI
- Mistral AI

## LLM Framework
- LangChain

## Vector Database
- ChromaDB

## Embedding Model
- all-MiniLM-L6-v2

## Libraries
- Whisper
- Pydub
- yt-dlp
- Requests
- Transformers
- Sentence Transformers
- HuggingFace Embeddings

---

# 📂 Project Structure

```
AI-Video-Agent/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
│
├── core/
│   ├── transcriber.py
│   ├── summaries.py
│   ├── extractor.py
│   ├── rag_engine.py
│   └── vector_store.py
│
├── utils/
│   └── audio_processor.py
│
├── vector_db/
│
└── temp_audio/
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/Shrutirowlo/AI-Video-Agent.git

cd AI-Video-Agent
```

---

## Create Virtual Environment

Windows

```bash
python -m venv .venv
```

Activate

```bash
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Create .env File

```
MISTRAL_API_KEY=YOUR_MISTRAL_API_KEY

SARVAM_API_KEY=YOUR_SARVAM_API_KEY

WHISPER_MODEL=small
```

---

## Run Application

```bash
streamlit run app.py
```

---

# 📌 Workflow

```
User Input
     │
     ▼
YouTube URL / Audio File
     │
     ▼
Audio Processing
     │
     ▼
Whisper / Sarvam AI
     │
     ▼
Transcript
     │
     ├──────────────► Meeting Title
     │
     ├──────────────► Summary
     │
     ├──────────────► Action Items
     │
     ├──────────────► Key Decisions
     │
     ├──────────────► Open Questions
     │
     ▼
Vector Database
(ChromaDB)
     │
     ▼
Embeddings
     │
     ▼
Retriever
     │
     ▼
Mistral AI
     │
     ▼
Chat with Meeting
```

---

# 📸 Screenshots

## Home Page

(Add Screenshot)

---

## Generated Summary

(Add Screenshot)

---

## Chat with Meeting

(Add Screenshot)

---

# Example Questions

- Summarize this meeting.
- What are the key decisions?
- List all action items.
- Who is responsible for deployment?
- What questions are still open?
- What was discussed about AI?

---

# Future Improvements

- Speaker Diarization
- Multi-language Support
- Meeting Timeline
- PDF Report Generation
- Email Summary
- Meeting Analytics Dashboard
- Cloud Storage Integration
- Speaker-wise Summary
- Real-Time Meeting Transcription

---

# Learning Outcomes

Through this project I learned:

- Retrieval-Augmented Generation (RAG)
- LangChain Pipelines
- ChromaDB Vector Store
- Whisper Speech Recognition
- Mistral AI Integration
- Prompt Engineering
- Embedding Models
- Streamlit Deployment
- API Integration
- Building End-to-End AI Applications

---

# Author

**Shruti Rowlo**

GitHub:
https://github.com/Shrutirowlo

LinkedIn:
 https://www.linkedin.com/in/shruti-rowlo/

---

# License

This project is licensed under the MIT License.

---

## ⭐ If you found this project useful, please consider giving it a Star!
