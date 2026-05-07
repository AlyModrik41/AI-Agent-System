🤖 LLM Agents with Tool Execution (Custom ReAct + LangChain)
📌 Overview

This project implements a dual AI agent system that combines a custom-built ReAct-style reasoning agent with a LangChain-based agent framework. The system enables Large Language Models (LLMs) to autonomously solve multi-step tasks using external tools, memory, and caching for optimized performance.

It is designed for learning, experimentation, and production-style agent architecture understanding.

🚀 Key Features
🧠 1. Custom ReAct Agent (Built from Scratch)
Implements a ReAct reasoning loop (Thought → Action → Observation)
Supports multi-step decision making
Dynamically selects and executes tools
Handles iterative reasoning until final answer
🔧 2. Tool Execution System

Integrated tools include:

🌐 Wikipedia Search (knowledge retrieval)
💱 Currency Exchange API (real-time FX rates)
➕ Calculator (arithmetic operations)

The agent can:

Select tools dynamically
Parse arguments from LLM outputs
Execute Python functions autonomously
⚡ 3. Multi-Model Fallback System
Supports multiple Gemini models
Automatically switches models on quota failure
Ensures system reliability under API limits
🧠 4. Memory System (FAISS Vector Store)
Stores past knowledge and observations
Uses sentence embeddings (MiniLM)
Retrieves relevant context using similarity search
Enables contextual reasoning across queries
⚡ 5. LLM Caching Layer
Reduces redundant API calls
Stores responses with TTL-based expiry
Improves latency significantly on repeated queries
🔀 6. Dual Execution Modes

The system supports two modes:

Mode	Description
custom	Fully custom-built ReAct agent
langchain	LangChain ZERO_SHOT_REACT_DESCRIPTION agent

This allows direct comparison between handcrafted and framework-based agents.

🏗️ Architecture
User Query
   │
   ├── Mode Selector (Custom / LangChain)
   │
   ├── Custom Agent
   │      ├── LLM (Gemini API)
   │      ├── ReAct Loop
   │      ├── Tool Executor
   │      ├── FAISS Memory
   │      └── Cache Layer
   │
   └── LangChain Agent
          ├── Tool Wrapper System
          ├── Gemini LLM (ChatGoogleGenerativeAI)
          └── Agent Executor
⚙️ Technologies Used
Python 🐍
Google Gemini API 🤖
LangChain 🦜
FAISS (Vector Memory Search)
SentenceTransformers
Wikipedia API
Requests (REST APIs)
Custom LLM Cache Layer
📦 Installation
git clone https://github.com/your-username/llm-agents-project.git
cd llm-agents-project

pip install -r requirements.txt
🔑 API Setup

Set your Gemini API key:

genai.configure(api_key="YOUR_API_KEY")
▶️ Usage
Run Custom Agent
run(user_input, mode="custom")
Run LangChain Agent
run(user_input, mode="langchain")
📊 Example
Input:
Convert 300 USD to EGP
Output (Custom Agent):
Thought: Need exchange rate
Action: currency_exchange(USD, EGP)
Observation: 48.2
Final Answer: 300 USD = 14460 EGP
⚡ Performance Optimizations
🔁 LLM response caching (reduces API calls)
🧠 Vector memory retrieval (FAISS)
⚡ Model fallback system (handles quota limits)
🧹 Prompt optimization for shorter reasoning cycles
📈 CV Highlights (Project Impact)
Built LLM-powered agents capable of tool calling for autonomous task execution
Implemented ReAct reasoning architecture from scratch
Integrated external APIs and Python tools for real-world task solving
Designed hybrid system comparing custom agents vs LangChain framework
Optimized latency using caching and memory retrieval systems
🔮 Future Improvements
LangGraph migration for advanced agent orchestration
Persistent long-term memory database
Tool selection policy learning (RL-based routing)
Async tool execution for faster inference
📌 Author

Aly Mahmoud
AI / ML Engineering Student
Focused on LLM Agents, Computer Vision, and Applied AI Systems
