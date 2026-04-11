# Washman AI

![Washman](static/images/washman_logo.png)

**Washman AI** is a demo AI assistant for Walton Washing Machines. It uses Retrieval-Augmented Generation (RAG) and LLMs to answer user queries, troubleshoot issues, and provide usage advice through a web interface.

> **Project Credits:**  
> This project is a demonstration and was primarily developed with the help of ChatGPT for backend, frontend, and image generation. Manual fine-tuning was applied where needed.  
> The frontend layout is inspired by a web page shown in Bob Ziroll's React course.  
> All code, images, and design are either AI-generated or adapted with respect to original sources.

---

## Features

- **PDF & TXT Document Processing**: Extracts and analyzes information from washing machine manuals and guides in the `data/` folder.
- **Vector Search (RAG)**: Uses vector embeddings and [ChromaDB](https://www.trychroma.com/) for fast, context-aware document retrieval.
- **AI-Powered Responses**: Integrates with Hugging Face LLMs for natural language answers.
- **Web Interface**: User-friendly FastAPI app with support for speech-to-text input and streaming responses via Server-Sent Events (SSE).

---

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository_url>
cd Washman_AI
```

### 2. Install Dependencies

Make sure you have Python 3.13+ and `uv` installed. Install dependencies using [pyproject.toml](pyproject.toml):

```bash
uv sync
```

### 3. Set Up Environment Variables

Create a `.env` file in the root directory and add your Hugging Face API key:

```
HUGGINGFACE_API_KEY=your_hugging_face_key
```

### 4. Add Data Files

Place washing machine manuals and guides (PDF/TXT) in the `data/` folder. Example:

```
data/
    washing_machine_manual.pdf
    web_data.txt
    ...
```

### 5. Generate Vector Embeddings

Run [vectorizer.py](vectorizer.py) to process documents and build the ChromaDB vector store:

```bash
uv run vectorizer.py
```
Or:
```bash
python3 vectorizer.py
```

### 6. Start the Web Application

Launch the FastAPI server ([main.py](main.py)):

```bash
uv run fastapi dev main.py
```
or,

```bash
fastapi dev main.py
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## Project Structure

- [main.py](main.py): FastAPI web server.
- [washman.py](washman.py): AI assistant logic and Hugging Face integration.
- [vectorizer.py](vectorizer.py): Document chunking and vector embedding.
- [pdf_processor.py](pdf_processor.py): PDF text extraction and OCR.
- [txt_file_processor.py](txt_file_processor.py): TXT file extraction and processing.
- `templates/`: HTML templates.
- `static/`: CSS, JS, and images.
- `data/`: Place your PDF and TXT manuals here.
- `chroma_db/`: ChromaDB vector database files.

---

## License

This project is licensed under the MIT License.

---

Enjoy using Washman AI!