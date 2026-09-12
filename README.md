# ResearchMind — Multi-Agent AI Research System

A multi-agent research pipeline built with LangChain that autonomously searches the web, scrapes deeper content, writes a structured report, and critiques its own output — all running on a free-tier LLM stack.

## How it works

Four agents/chains work in sequence:

1. **Search Agent** — Uses DuckDuckGo Search to find recent, relevant information on a topic.
2. **Reader Agent** — Scrapes the most relevant URL from the search results using BeautifulSoup for deeper content.
3. **Writer Chain** — An LCEL pipeline (`prompt | llm | StrOutputParser`) that synthesizes the research into a structured report (Introduction, Key Findings, Conclusion, Sources).
4. **Critic Chain** — Reviews the report and returns a score out of 10 with strengths and areas to improve.

## Tech Stack

- **LLM:** Google Gemini (`gemini-3.5-flash-lite`) via `langchain-google-genai`
- **Search:** DuckDuckGo Search (`ddgs`) — no API key required
- **Scraping:** BeautifulSoup + Requests
- **Orchestration:** LangChain `create_agent` (ReAct-style agents) + LCEL (Runnables)
- **UI:** Streamlit

## Setup

1. Clone the repo:
   ```
   git clone https://github.com/PradyumnaKmsrit/Multi-agent-research-system.git
   cd Multi-agent-research-system
   ```

2. Create a virtual environment and activate it:
   ```
   uv venv
   .venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   uv pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root:
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```
   Get a free key at https://aistudio.google.com/apikey

5. Run the app:
   ```
   python -m streamlit run app.py
   ```

## Project Structure

```
├── tools.py         # DuckDuckGo search tool + web scraping tool
├── agents.py        # Search Agent, Reader Agent, Writer Chain, Critic Chain
├── pipeline.py       # CLI version of the research pipeline
├── app.py           # Streamlit UI
└── requirements.txt
```

## Notes

- This project runs entirely on free-tier APIs — no paid keys required.
- Model availability on free-tier providers can change over time; check the provider's docs if you hit a "model not found" error.