# 🤖 LLM Agents with Tool Execution (Custom ReAct + LangChain)

## 📌 Overview

This project implements a **dual AI agent system** that combines a **custom-built ReAct-style reasoning agent** with a **LangChain-based agent framework**. The system enables Large Language Models (LLMs) to autonomously solve multi-step tasks using external tools, memory, and caching for optimized performance.

It is designed for **learning, experimentation, and production-style agent architecture understanding**.

---

## 🚀 Key Features

### 🧠 Custom ReAct Agent (Built from Scratch)
- Implements a **ReAct reasoning loop (Thought → Action → Observation)**
- Supports multi-step decision making
- Dynamically selects and executes tools
- Iteratively reasons until reaching a final answer

---

### 🔧 Tool Execution System
Integrated tools include:
- 🌐 Wikipedia Search (knowledge retrieval)
- 💱 Currency Exchange API (real-time FX rates)
- ➕ Calculator (math operations)

Capabilities:
- Dynamic tool selection
- Argument parsing from LLM outputs
- Autonomous Python function execution

---

### ⚡ Multi-Model Fallback System
- Supports multiple Gemini models
- Automatically switches models on quota failure
- Ensures system reliability under API constraints

---

### 🧠 Memory System (FAISS Vector Store)
- Stores past observations and knowledge
- Uses SentenceTransformer embeddings
- Performs semantic similarity search
- Enables context-aware reasoning

---

### ⚡ LLM Caching Layer
- Reduces redundant API calls
- TTL-based caching system
- Improves latency for repeated queries

---

### 🔀 Dual Execution Modes

| Mode | Description |
|------|------------|
| `custom` | Fully custom-built ReAct agent |
| `langchain` | LangChain-based agent |

This allows direct comparison between:
- handcrafted agent design
- framework-based agent execution

---

## 🏗️ Architecture
User Query
│
├── Mode Selector (custom / langchain)
│
├── Custom Agent
│ ├── Gemini LLM
│ ├── ReAct Loop
│ ├── Tool Executor
│ ├── FAISS Memory
│ └── Cache Layer
│
└── LangChain Agent
├── Tool Wrappers
├── ChatGoogleGenerativeAI
└── ZERO_SHOT_REACT Agent


---

## ⚙️ Tech Stack

- Python 🐍
- Google Gemini API 🤖
- LangChain 🦜
- FAISS (Vector Memory)
- SentenceTransformers
- Wikipedia API
- Requests (REST APIs)

---

## 📦 Installation

```bash
git clone https://github.com/your-username/llm-agents-project.git
cd llm-agents-project

pip install -r requirements.txt
```

##🔑 API Setup
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

##▶️ Usage

Run Custom Agent
run(user_input, mode="custom")

Run LangChain Agent
run(user_input, mode="langchain")

##📊 Example

- Input
- Convert 300 USD to EGP
- Output (Custom Agent)
- sThought: Need exchange rate
- Action: currency_exchange(USD, EGP)
- Observation: 48.2
- Final Answer: 300 USD = 14460 EGP

##⚡ Performance Optimizations

LLM response caching (reduces API calls)
FAISS memory retrieval (semantic context)
Model fallback system (handles quota limits)
Prompt optimization for faster reasoning

##📈 CV Highlights

- Built LLM-powered agents capable of tool calling for autonomous task execution
- Implemented ReAct reasoning architecture from scratch
- Integrated external APIs and Python tools for real-world task solving
- Designed hybrid system comparing custom agents vs LangChain framework
- Optimized latency using caching and memory retrieval systems

#🔮 Future Improvements

- LangGraph migration for advanced agent orchestration
- Persistent long-term memory database
- Tool selection optimization (policy learning)
- Async tool execution for faster inference
