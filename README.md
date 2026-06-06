# 🤖 Multi-Agent AI Research System

An AI-powered research assistant built using **LangChain**, **LangGraph**, **Streamlit**, and **OpenRouter**. The system uses multiple specialized agents that collaborate to search the web, extract information, generate reports, fact-check results, and provide constructive feedback.

---

## 🚀 Features

* 🔎 **Search Agent**

  * Finds recent and reliable information using Tavily Search.

* 📖 **Reader Agent**

  * Scrapes webpages using BeautifulSoup.
  * Extracts and summarizes useful content.

* ✍️ **Writer Chain**

  * Generates structured and comprehensive reports.

* ✅ **Fact Checker**

  * Reviews generated reports and identifies questionable claims.

* ⭐ **Critic Chain**

  * Evaluates report quality and provides improvement suggestions.

* 📊 Execution time tracking

* 📄 Markdown export

* 📑 PDF report export

* 📚 Research history

* 🌐 Interactive Streamlit UI

---

# 🏗 Architecture

```text
User Query
     ↓
🔎 Search Agent (Tavily)
     ↓
📖 Reader Agent (BeautifulSoup)
     ↓
✍️ Writer Chain
     ↓
✅ Fact Checker
     ↓
⭐ Critic Chain
     ↓
Final Research Report
```

---

# 🛠 Tech Stack

### LLM Framework

* LangChain
* LangGraph

### Models

* OpenRouter
* Google Gemini
* Qwen
* Mistral

### Search

* Tavily Search API

### Web Scraping

* BeautifulSoup
* Requests

### UI

* Streamlit

### Utilities

* python-dotenv
* Rich
* FPDF

---

# 📂 Project Structure

```text
multi-agent-research-system/

│
├── app.py                  # Streamlit UI
├── pipeline.py             # Multi-agent pipeline
├── agents.py               # Search and reader agents + chains
├── tools.py                # Tavily and BeautifulSoup tools
├── utils.py                # PDF generation
├── requirements.txt
├── .env
├── README.md
└── assets/
```

---

# ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/multi-agent-research-system.git

cd multi-agent-research-system
```

### Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

Windows:

```bash
.venv\Scripts\activate
```

Linux/Mac:

```bash
source .venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file:

```env
OPENROUTER_API_KEY=your_key

TAVILY_API_KEY=your_key

OPENAI_MODEL=google/gemini-3.1-flash-lite
```

---

# ▶ Running the Application

```bash
streamlit run app.py
```

---

# 📋 Example Workflow

### Input

```text
Future of Quantum Computing
```

### Pipeline

```text
Search Agent
↓
Reader Agent
↓
Writer Chain
↓
Fact Checker
↓
Critic Chain
```

### Output

* Detailed report
* Fact-check analysis
* Critic feedback
* Downloadable Markdown/PDF report

---

# Example UI

### Main Interface

* Topic Input
* Progress Tracking
* Execution Metrics

### Sections

* 🔎 Search Results
* 📖 Scraped Content
* 📝 Final Report
* ✅ Fact Check
* ⭐ Critic Feedback

---

# Future Improvements

* [ ] Convert pipeline into LangGraph StateGraph
* [ ] Multi-URL reading
* [ ] Conversational memory
* [ ] Vector Database support
* [ ] RAG integration
* [ ] LangSmith tracing
* [ ] Deployment on Streamlit Cloud
* [ ] Docker support

---

# Skills Demonstrated

* Multi-Agent Systems
* LangChain
* LangGraph
* Prompt Engineering
* Tool Calling
* ReAct Agents
* Web Scraping
* Streamlit
* LLM Pipelines
* Fact Checking
* AI Application Development

---

# Author

**Divyanshu Chaubey**

Computer Science Engineering Student

Interested in AI Engineering, Agentic AI, LLMs, and Machine Learning.

---

⭐ If you found this project useful, consider giving the repository a star.
