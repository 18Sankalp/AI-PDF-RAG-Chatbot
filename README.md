# 📄 AI-PDF-RAG-Chatbot

An AI-powered PDF Question Answering application built using **Retrieval-Augmented Generation (RAG)**. Upload any PDF document, ask questions in natural language, and receive context-aware answers generated using **Google Gemini API** and **Sentence Transformers**.

---

## 🚀 Features

* 📂 Upload PDF documents
* 📑 Automatic text extraction from PDFs
* ✂️ Intelligent text chunking
* 🔍 Semantic search using embeddings
* 📈 Cosine similarity-based document retrieval
* 🤖 AI-generated answers using Google Gemini
* 💬 Interactive Streamlit web interface
* ⚡ Fast and lightweight RAG pipeline

---

## 🛠️ Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### AI & NLP

* Google Gemini API
* Sentence Transformers
* all-MiniLM-L6-v2

### Libraries

* PyMuPDF (fitz)
* NumPy
* scikit-learn
* python-dotenv

---

## 📂 Project Structure

```text
AI-PDF-RAG-Chatbot/
│
├── app.py
├── streamlit_app.py
├── config.py
├── requirements.txt
├── .env
│
├── utils/
│   ├── pdf_reader.py
│   ├── chunking.py
│   ├── embedding.py
│   ├── retrieval.py
│   └── llm.py
│
├── data/
│
├── screenshots/
│
└── README.md
```

---

## ⚙️ Installation

### Clone the Repository

```bash
git clone https://github.com/18Sankalp/AI-PDF-RAG-Chatbot.git
```

```bash
cd AI-PDF-RAG-Chatbot
```

---

### Create Virtual Environment

Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Configure Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

## ▶️ Run the Application

```bash
streamlit run streamlit_app.py
```

The application will open in your browser.

---

## 🔄 RAG Workflow

1. Upload a PDF document.
2. Extract text using PyMuPDF.
3. Split the text into manageable chunks.
4. Generate embeddings using Sentence Transformers.
5. Retrieve the most relevant chunks based on the user's query.
6. Send the retrieved context and question to Google Gemini.
7. Display the generated answer in Streamlit.

---

## 📸 Screenshots

Add screenshots of:

* Home Page
* PDF Upload
* Question Answering
* Retrieved Context

Example:

```
screenshots/
    home.png
    upload.png
    answer.png
```

---

## 📊 Future Enhancements

* Multiple PDF support
* FAISS vector database
* Chat history
* Source citations
* Document summarization
* OCR support for scanned PDFs
* User authentication
* Docker deployment

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push the branch
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Sankalp Deore**

* GitHub: https://github.com/18Sankalp
* LinkedIn: *(Add your LinkedIn profile here)*

---

⭐ If you found this project useful, please consider giving it a Star on GitHub.
