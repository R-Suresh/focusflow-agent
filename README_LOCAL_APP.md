# FocusFlow Local Streamlit App

This is the local app version of FocusFlow.

FocusFlow turns a messy task dump into:

- prioritized tasks
- a realistic schedule
- risk and overload checks
- a Slack-ready daily summary
- Google Calendar-ready holds

The app is safe by default:

- mock mode is on by default
- Slack posting is off by default
- Google Calendar creation is off by default

## Project files

```text
app.py
focusflow_core.py
requirements.txt
.env.example
docs/google_calendar_setup.md
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

## Run with mock mode

Mock mode is enabled by default. This lets you try the UI without OpenAI, Slack, or Google Calendar setup.

## Run with OpenAI

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Add your API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Then turn off mock mode in the sidebar.

## Run with Slack

Add your Slack webhook to `.env`:

```env
SLACK_WEBHOOK_URL=your_slack_webhook_url_here
```

Then enable Slack posting in the sidebar.

## Run with Google Calendar

Follow:

```text
docs/google_calendar_setup.md
```

You will create a local `credentials.json` file and place it in the repo root.

Then enable Google Calendar creation in the sidebar.

## Important safety notes

Never commit:

```text
.env
credentials.json
token.json
```

These files contain private credentials or access tokens.
