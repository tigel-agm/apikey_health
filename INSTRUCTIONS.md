# Instructions for Universal API Key Health Monitor

These instructions will help you get started, understand the core features, and know the best practices for using the API Key Health Monitor.

## Purpose
Basic API health check:
- Continuously validate that API keys are valid and usable.
- Track health over time to catch expiry, rate limits, or errors early.
- Simplify monitoring across multiple AI platforms with one dashboard.

## Core Features
1. **Manage Keys**: Add, view, and delete API keys via the Streamlit UI.
2. **Health Checks**:
   - **Automated**: Runs every 5 minutes by default (configurable).
   - **Manual**: Trigger on-demand checks for any key.
3. **Health Logs**: See history of checks, response times, and error messages.
4. **Service Adapters**:
   - **OpenAI**: Model list call.
   - **Azure OpenAI**: Chat/completion call.
   - **Google Gemini**: Embedding/chat call.
   - **Ollama**: Local server ping.
   - **Custom**: User-defined HTTP checks via JSON.
5. **Customization**:
   - Use `.env` to store endpoint URLs, model overrides, and keys.
   - Custom JSON templates for advanced HTTP health-checks.

## How to Use
### 1. Add a New Key
1. Navigate to **Manage Keys**.
2. Click **➕ Add New API Key**.
3. Select your service from the dropdown.
4. Fill in the **Name** and **Key Value**.
5. Configure service-specific fields (e.g. model, deployment).
6. Click **Add Key**. The app will confirm and rerun.

### 2. Trigger a Health Check
- On the **Manage Keys** tab, click **Check Now** next to any key.
- Or let the scheduler automatically run checks every 5 minutes.

### 3. View Health Logs
1. Switch to the **Health Logs** tab.
2. Filter logs by key, date range, status, etc. (future feature).
3. Review response times and errors.

### 4. Customize Health Checks
- Click **Custom API Configuration** for the **Custom** service.
- Edit the JSON template: set URL, HTTP method, headers, body, and success codes.
- Use the `{key}` placeholder in headers or body to inject your API key.
- Validate JSON; errors will display in red.

## Advanced Tips
- **Use Docker**: Run `docker-compose up` to launch with SQLite and HTTPS support.
- **Switch to PostgreSQL**: Set `DATABASE_URL=postgresql://...` in `.env`.
- **Email Alerts**: Configure `SMTP_URL` to receive failure notifications.
- **Slack Webhooks**: Set `SLACK_WEBHOOK_URL` for alert messages.
- **Extend Adapters**: Add new service adapters in `backend/adapters/` and update `crud.py`.

## Troubleshooting
- **Import Errors**: Run from project root with `uvicorn backend.main:app`.
- **Port Conflicts**: Change ports with `--port` flags for Uvicorn and Streamlit.
- **Missing Models**: Use **Fetch live model list** only if your key has appropriate permissions.
- **JSON Errors**: Ensure your custom JSON is valid; use an online linter if needed.

## Next Steps
- Contribute features on GitHub.
- Submit issues for bugs or improvements.

Happy monitoring!
