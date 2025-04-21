# Universal API Key Health Monitor

A self-hosted solution to continuously validate and monitor the health of API keys across multiple AI and external services. Provides a real-time dashboard, scheduled and manual checks, health logs, and support for popular AI platforms as well as custom APIs.

## What This Can Do
- Register and store API keys with metadata.
- Automated health checks every 5 minutes (configurable).
- Manual health check trigger per key.
- Health check status codes: `OK`, `EXPIRED`, `RATE_LIMITED`, `ERROR`.
- Record response times and error messages.
- View historical health logs in Streamlit UI.
- Support for OpenAI, Azure OpenAI, Google Gemini, Ollama, and Custom HTTP APIs.
- Live-fetch OpenAI model list.
- Simple Streamlit dashboard with dropdowns and tooltips.
- Local-first: no authentication required; runs on your machine.

## What This Cannot Do
- Multi-user authentication and role-based access.
- Production-grade horizontal scaling.
- Automatic key rotation except manual triggers; full rotation hooks not implemented.
- Built-in alert channels (email/Slack) require additional setup.
- Built-in HTTPS certificates; default is HTTP. Self-signed HTTPS requires custom config.
- Comprehensive error handling for all edge cases; intended for local development (for now).

## Prerequisites
- Python 3.11+

## Installation
1. Clone the repo:
   ```bash
   git clone https://github.com/username/universal-api-key-monitor.git
   cd universal-api-key-monitor
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the App
1. Start the backend API:
   ```bash
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```
2. In a separate terminal, start the Streamlit UI:
   ```bash
   streamlit run frontend/streamlit_app.py
   ```
3. Open [http://localhost:8501](http://localhost:8501) in your browser.

## Project Structure
```
.
├── backend
│   ├── main.py
│   ├── db.py
│   ├── models.py
│   ├── crud.py
│   ├── schemas.py
│   ├── adapters
│   ├── routers
│   └── scheduler.py
├── frontend
│   └── streamlit_app.py
├── requirements.txt
```


## Contributing
- Fork and create feature branches.

## License
MIT
