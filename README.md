# FocusFlow Agent

FocusFlow is a beginner-friendly AI planning agent that turns a messy task dump into a prioritized daily plan, realistic schedule, Slack-ready summary, and calendar-ready holds.

This project is designed for the **Applied AI Labs** workshop:

> **Your First Practical AI Agent in 30 Minutes**

The goal is to help beginners understand how a practical AI agent can move beyond basic prompting and produce structured, useful, integration-ready outputs.

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
- Calendar-ready event previews

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
Integration-ready outputs
```

This makes the notebook a practical introduction to how AI agents can reason over user intent, structure information, make planning decisions, and prepare outputs for real tools.

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

Notebook:

```text
notebooks/focusflow_milestone_1_colab.ipynb
```

### Milestone 2: Slack Integration

Send the FocusFlow daily plan message to a real Slack channel using a Slack incoming webhook.

Planned outcome:

```text
FocusFlow plan → Slack daily summary
```

### Milestone 3: Google Calendar Holds

Create real Google Calendar holds from the FocusFlow schedule output.

Planned outcome:

```text
FocusFlow schedule → Google Calendar time blocks
```

---

## Repository Structure

```text
focusflow-agent/
├── notebooks/
│   └── focusflow_milestone_1_colab.ipynb
├── README.md
├── .gitignore
└── LICENSE
```

---

## How to Run Milestone 1

### Option 1: Run in Google Colab

1. Open the notebook:

```text
notebooks/focusflow_milestone_1_colab.ipynb
```

2. Upload it to Google Colab or open it directly from GitHub.

3. Run the notebook cells from top to bottom.

By default, the notebook uses mock mode so it can run without an API key:

```python
USE_MOCK_MODE = True
```

This is useful for workshops, demos, and first-time users.

---

### Option 2: Run With a Real OpenAI API Key

To call a real model, set:

```python
USE_MOCK_MODE = False
```

Then run the API key setup cell and enter your OpenAI API key when prompted.

The notebook uses `getpass()` so your key is not printed in the notebook output.

---

## Expected Output

After running Milestone 1, the notebook should produce:

### 1. Prioritized Task Table

| Task | Category | Priority | Effort | Urgency | When | Estimated Minutes |
|---|---|---|---|---|---|---:|

### 2. Today’s Schedule

| Title | Start Time | End Time | Type | Reason |
|---|---|---|---|---|

### 3. Plan Check

The agent flags issues such as:

- Too many deep-work tasks in one day
- Missing deadlines
- Overloaded schedules
- Tasks that should be moved to later
- Unclear tasks that need clarification

### 4. Next Best Action

The notebook ends with a single recommended next step.

Example:

```text
Start with the project update before opening email.
```

### 5. Slack Message Preview

The notebook generates a Slack-ready daily summary.

### 6. Calendar Preview

The notebook generates calendar-ready event blocks that can later be converted into real Google Calendar holds.

---

## Workshop Use

This project is designed to be easy to teach in a short beginner workshop.

Recommended flow:

```text
0–5 min: Explain the FocusFlow agent workflow
5–10 min: Run setup and sample input
10–18 min: Generate the structured plan
18–23 min: Review task table, schedule, risks, and next action
23–27 min: Preview Slack message and calendar holds
27–30 min: Explain next milestones
```

The first milestone works even without real integrations, making it safe for live demos.

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

Use environment variables, Colab secrets, or `getpass()` prompts instead.

Recommended `.gitignore` entries:

```gitignore
.env
*.env
credentials.json
token.json
*.pem
*.key
__pycache__/
.ipynb_checkpoints/
```

---

## Who This Is For

This project is useful for:

- AI beginners
- Students
- Builders
- Product managers
- Founders
- Engineers new to LLM agents
- Anyone who wants a practical introduction to applied AI workflows

---

## License

This project is licensed under the MIT License.
