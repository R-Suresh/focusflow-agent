# FocusFlow Agent

FocusFlow is a beginner-friendly AI planning agent that turns a messy task dump into a prioritized daily plan, realistic schedule, Slack-ready summary, and Google Calendar-ready holds.

This project was built for the **Applied AI Labs** workshop:

> **Your First Practical AI Agent in 30 Minutes**

The goal is to help beginners understand how practical AI agents move beyond basic prompting and produce structured, useful, integration-ready outputs.

FocusFlow starts as a Google Colab notebook and evolves into a local Streamlit app.

---

## What FocusFlow Does

FocusFlow takes messy natural language input like:

```text
I need to prepare slides for Friday, email Sam, review an AI paper,
book a dentist appointment, finish project update, go to the gym,
pay rent, and plan the meetup agenda.

I have 4 hours today and prefer deep work in the morning.
```

And turns it into:

- A prioritized task table
- A realistic daily schedule
- Risk and overload analysis
- A next-best-action recommendation
- A Slack-ready daily plan message
- Google Calendar-ready event previews
- Optional Slack posting
- Optional Google Calendar event creation

---

## Why This Is an AI Agent

FocusFlow is not just a chatbot that rewrites your to-do list.

It follows a simple agentic workflow:

```text
Messy input
   ↓
Task extraction
   ↓
Categorization
   ↓
Prioritization
   ↓
Scheduling
   ↓
Risk check
   ↓
Tool-ready outputs
   ↓
Optional Slack + Google Calendar actions
```

This makes FocusFlow a practical introduction to how AI agents can reason over user intent, structure information, make planning decisions, validate outputs, and prepare actions for real tools.

---

## Project Milestones

### Milestone 1: Basic Colab Notebook

Build the core FocusFlow planning agent in Google Colab.

Includes:

- Messy task input
- Task extraction
- Task categorization
- Priority, urgency, and effort estimation
- Daily schedule generation
- Risk and overload checks
- Slack message preview
- Calendar holds preview
- CSV export

### Milestone 2: Slack Integration

Extend FocusFlow so it can send the generated daily plan to a real Slack channel using a Slack incoming webhook.

Outcome:

```text
FocusFlow plan → Slack daily summary
```

### Milestone 3: Google Calendar Holds

Extend FocusFlow so it can turn the generated schedule into Google Calendar-ready event payloads and optionally create real calendar holds.

Outcome:

```text
FocusFlow schedule → Google Calendar time blocks
```

### Milestone 4: One-Cell Notebook Demo

Wrap the notebook workflow into a simpler one-cell demo experience.

Instead of running many separate cells, users can:

```text
Paste task dump → Run one FocusFlow cell → See plan, Slack preview, and Calendar holds
```

### Milestone 5: Local Streamlit App

Turn FocusFlow into a local web app using Streamlit.

The local app provides:

- A simple browser-based UI
- Sidebar settings
- Mock mode
- Real OpenAI mode
- Slack message preview and posting
- Google Calendar event preview and creation
- Safety checks before taking real actions

Run locally with:

```bash
streamlit run app.py
```

See:

```text
README_LOCAL_APP.md
```

for detailed local setup instructions.

---

## Repository Structure

```text
focusflow-agent/
├── app.py
├── focusflow_core.py
├── requirements.txt
├── .env.example
├── README.md
├── README_LOCAL_APP.md
├── docs/
│   └── google_calendar_setup.md
├── assets/
│   └── screenshots/
│       └── README.md
├── notebooks/
│   └── focusflow_milestone_*.ipynb
├── .gitignore
└── LICENSE
```

---

## Quick Start: Local Streamlit App

The fastest way to try FocusFlow as a local app is to run the Streamlit version.

### 1. Clone the repository

```bash
git clone https://github.com/R-Suresh/focusflow-agent.git
cd focusflow-agent
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

By default, the app runs in mock mode, so you can try it without an OpenAI API key, Slack webhook, or Google Calendar setup.

---

## Running With OpenAI

To call a real OpenAI model locally:

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

3. Restart the Streamlit app:

```bash
streamlit run app.py
```

4. In the sidebar, turn off:

```text
Use mock mode
```

The app will then call OpenAI locally.

---

## Slack Integration

To enable Slack posting:

1. Add your Slack incoming webhook URL to `.env`:

```env
SLACK_WEBHOOK_URL=your_slack_webhook_url_here
```

2. Restart the app.
3. Turn on **Enable Slack posting** in the sidebar.
4. Generate a plan.
5. Open the **Slack** tab.
6. Review the message.
7. Click **Post Daily Plan to Slack**.

---

## Google Calendar Integration

To create real Google Calendar holds, follow:

```text
docs/google_calendar_setup.md
```

At a high level, you will:

1. Create a Google Cloud project.
2. Enable the Google Calendar API.
3. Configure OAuth consent.
4. Add yourself as a test user.
5. Add the `calendar.events` scope.
6. Create a Desktop OAuth client.
7. Download the OAuth file as `credentials.json`.
8. Place `credentials.json` in the repo root.
9. Run the Streamlit app.
10. Enable Google Calendar creation in the sidebar.

The app will create `token.json` after the first successful Google login.

Do not commit either file.

---

## Notebook Workshop Path

The notebooks are designed for workshop-style learning.

They show the project progression step by step:

```text
Milestone 1 → basic planning agent
Milestone 2 → Slack integration
Milestone 3 → Google Calendar integration
Milestone 4 → one-cell notebook demo
```

Use the notebooks if you want to understand how the agent is built incrementally.

Use the Streamlit app if you want to try FocusFlow as a local web application.

---

## Expected Output

After running FocusFlow, you should see:

### 1. Prioritized Task Table

| Task | Category | Priority | Effort | Urgency | When | Estimated Minutes |
|---|---|---|---|---|---|---:|

### 2. Daily Schedule

| Title | Start Time | End Time | Type | Reason |
|---|---|---|---|---|

### 3. Plan Check

FocusFlow flags issues such as:

- Too many deep-work tasks in one day
- Missing deadlines
- Overloaded schedules
- Tasks that should be moved to later
- Unclear tasks that need clarification

### 4. Next Best Action

Example:

```text
Start with the project update before opening email.
```

### 5. Slack Message Preview

FocusFlow generates a Slack-ready daily summary.

### 6. Calendar Preview

FocusFlow generates calendar-ready event blocks that can optionally be converted into real Google Calendar holds.

---

## Safety Notes

Do not commit secrets to this repository.

Never commit:

- OpenAI API keys
- Slack webhook URLs
- Google credentials
- `.env` files
- `credentials.json`
- `token.json`
- `.streamlit/secrets.toml`

Use environment variables, local `.env` files, Colab secrets, or `getpass()` prompts instead.

The app is designed to be safe by default:

- Mock mode is on by default.
- Slack posting is off by default.
- Google Calendar creation is off by default.
- Real actions require explicit user enablement.

---

## License

This project is licensed under the MIT License.
