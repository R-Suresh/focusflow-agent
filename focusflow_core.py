"""
FocusFlow core logic for the local Streamlit app.

Safe by default:
- Mock mode can run without any API keys.
- Slack posting happens only when explicitly enabled.
- Google Calendar event creation happens only when explicitly enabled.
- No secrets are hardcoded.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

DEFAULT_TIMEZONE = "America/Los_Angeles"
DEFAULT_MODEL_NAME = "gpt-4.1-mini"


def get_mock_focusflow_plan() -> Dict[str, Any]:
    """Return a deterministic demo plan so the app works without external setup."""
    return {
        "tasks": [
            {"task": "Finish project update", "category": "Work", "priority": "High", "effort": "High", "urgency": "High", "when": "Today", "estimated_minutes": 90, "reason": "Important work deliverable and likely dependency for others."},
            {"task": "Prepare slide outline", "category": "Work", "priority": "High", "effort": "Medium", "urgency": "High", "when": "Today", "estimated_minutes": 60, "reason": "Upcoming deadline and benefits from focused morning time."},
            {"task": "Email Sam", "category": "Admin", "priority": "Medium", "effort": "Low", "urgency": "Medium", "when": "Today", "estimated_minutes": 15, "reason": "Quick communication task that can be batched with admin work."},
            {"task": "Pay rent", "category": "Personal/Admin", "priority": "High", "effort": "Low", "urgency": "High", "when": "Today", "estimated_minutes": 10, "reason": "Time-sensitive personal admin task."},
            {"task": "Review AI paper", "category": "Learning", "priority": "Medium", "effort": "Medium", "urgency": "Low", "when": "This Week", "estimated_minutes": 60, "reason": "Useful learning task, but less urgent than deadline-driven work."},
            {"task": "Book dentist appointment", "category": "Personal", "priority": "Low", "effort": "Low", "urgency": "Low", "when": "This Week", "estimated_minutes": 10, "reason": "Quick task that can be handled later in an admin batch."},
            {"task": "Go to the gym", "category": "Health", "priority": "Medium", "effort": "Medium", "urgency": "Medium", "when": "Today", "estimated_minutes": 60, "reason": "Health task; best scheduled after work blocks."},
        ],
        "schedule": [
            {"title": "Finish project update", "start_time": "2026-05-21T09:00:00-07:00", "end_time": "2026-05-21T10:30:00-07:00", "type": "deep_work", "reason": "Highest-priority focus task, scheduled during preferred deep-work time."},
            {"title": "Prepare slide outline", "start_time": "2026-05-21T10:45:00-07:00", "end_time": "2026-05-21T11:45:00-07:00", "type": "deep_work", "reason": "Second major work task, kept in the morning focus block."},
            {"title": "Admin batch: email Sam and pay rent", "start_time": "2026-05-21T14:00:00-07:00", "end_time": "2026-05-21T14:30:00-07:00", "type": "admin", "reason": "Small admin tasks grouped together to reduce context switching."},
            {"title": "Gym", "start_time": "2026-05-21T18:00:00-07:00", "end_time": "2026-05-21T19:00:00-07:00", "type": "personal", "reason": "Health task scheduled outside main work blocks."},
        ],
        "risks": [
            "The task list includes more work than fits into a short focused workday.",
            "Reviewing the AI paper should move to later this week unless it has a deadline.",
            "Some tasks do not have explicit deadlines, so priorities were inferred conservatively.",
        ],
        "next_best_action": "Start with the project update before opening email or switching contexts.",
        "slack_message": "*FocusFlow Daily Plan*\n\n*Top priorities*\n1. Finish project update\n2. Prepare slide outline\n3. Admin batch: email Sam and pay rent\n\n*Suggested schedule*\n• 9:00–10:30 — Finish project update\n• 10:45–11:45 — Prepare slide outline\n• 2:00–2:30 — Admin batch\n• 6:00–7:00 — Gym\n\n*Plan check*\nYou listed more work than fits into a short focused day. Move paper review to later this week.\n\n*Next best action*\nStart with the project update before opening email.",
        "calendar_preview": [
            {"summary": "FocusFlow: Finish project update", "start": "2026-05-21T09:00:00-07:00", "end": "2026-05-21T10:30:00-07:00"},
            {"summary": "FocusFlow: Prepare slide outline", "start": "2026-05-21T10:45:00-07:00", "end": "2026-05-21T11:45:00-07:00"},
            {"summary": "FocusFlow: Admin batch: email Sam and pay rent", "start": "2026-05-21T14:00:00-07:00", "end": "2026-05-21T14:30:00-07:00"},
            {"summary": "FocusFlow: Gym", "start": "2026-05-21T18:00:00-07:00", "end": "2026-05-21T19:00:00-07:00"},
        ],
    }


def build_focusflow_system_prompt() -> str:
    """Build the system prompt for the FocusFlow planning agent."""
    return """
You are FocusFlow, a personal planning AI agent.

Your job is to turn a messy task dump into a realistic daily plan.

Follow this workflow:
1. Extract individual tasks.
2. Categorize each task.
3. Estimate urgency, effort, and importance.
4. Prioritize tasks into Today, This Week, and Later.
5. Create a realistic schedule based on available time and user constraints.
6. Flag risks such as overload, missing deadlines, unclear tasks, or too many deep-work items.
7. End with the single next best action.
8. Generate a Slack-ready daily plan message.
9. Generate calendar-ready event previews.

Rules:
- Do not schedule more work than the available time allows.
- Prefer deep work in the morning if the user requests it.
- Batch small admin tasks together.
- Include breaks between deep-work blocks.
- Be practical, concise, and realistic.
- Return valid JSON only.
"""


def build_focusflow_user_prompt(task_dump: str, available_hours: int, deep_work_preference: str, timezone: str) -> str:
    """Build the user prompt with task input and planning constraints."""
    today_date = datetime.now().strftime("%Y-%m-%d")
    return f"""
Task dump:
{task_dump}

Today's date:
{today_date}

Timezone:
{timezone}

User constraints:
- Available hours today: {available_hours}
- Deep work preference: {deep_work_preference}

Return JSON with exactly these keys:
- tasks
- schedule
- risks
- next_best_action
- slack_message
- calendar_preview

Each task must include:
- task
- category
- priority
- effort
- urgency
- when
- estimated_minutes
- reason

Each schedule item must include:
- title
- start_time
- end_time
- type
- reason

Each calendar_preview item must include:
- summary
- start
- end

Use ISO 8601 datetime strings for all schedule and calendar times.
"""


def generate_focusflow_plan(task_dump: str, available_hours: int = 4, deep_work_preference: str = "Morning", timezone: str = DEFAULT_TIMEZONE, use_mock_mode: bool = True, model_name: str = DEFAULT_MODEL_NAME) -> Dict[str, Any]:
    """Generate a FocusFlow plan via mock output or the OpenAI API."""
    if use_mock_mode:
        return get_mock_focusflow_plan()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is missing. Add it to .env or enable mock mode.")

    from openai import OpenAI
    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model=model_name,
        input=[
            {"role": "system", "content": build_focusflow_system_prompt()},
            {"role": "user", "content": build_focusflow_user_prompt(task_dump, available_hours, deep_work_preference, timezone)},
        ],
        temperature=0.2,
    )

    try:
        return json.loads(response.output_text)
    except json.JSONDecodeError as exc:
        raise ValueError("Model response was not valid JSON. Try rerunning.") from exc


def validate_plan(plan: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate the minimum structure needed for display and integrations."""
    messages: List[str] = []
    required = ["tasks", "schedule", "risks", "next_best_action", "slack_message", "calendar_preview"]
    missing = [key for key in required if key not in plan]
    if missing:
        messages.append(f"Missing required keys: {missing}")

    for key in ["tasks", "schedule", "risks", "calendar_preview"]:
        if key in plan and not isinstance(plan[key], list):
            messages.append(f"{key} must be a list.")

    if not str(plan.get("slack_message", "")).strip():
        messages.append("slack_message is empty.")

    for index, item in enumerate(plan.get("schedule", []), start=1):
        if not item.get("start_time") or not item.get("end_time"):
            messages.append(f"Schedule item {index} is missing start_time or end_time.")
            continue
        try:
            start = datetime.fromisoformat(item["start_time"])
            end = datetime.fromisoformat(item["end_time"])
            if end <= start:
                messages.append(f"Schedule item {index} has end_time before start_time.")
        except ValueError:
            messages.append(f"Schedule item {index} has invalid ISO datetime format.")

    if not messages:
        return True, ["Plan structure looks good."]
    return False, messages


def tasks_dataframe(plan: Dict[str, Any]) -> pd.DataFrame:
    """Convert plan tasks to a DataFrame for display."""
    df = pd.DataFrame(plan.get("tasks", []))
    preferred = ["task", "category", "priority", "effort", "urgency", "when", "estimated_minutes", "reason"]
    cols = [col for col in preferred if col in df.columns]
    return df[cols] if cols else df


def schedule_dataframe(plan: Dict[str, Any]) -> pd.DataFrame:
    """Convert plan schedule to a DataFrame for display."""
    df = pd.DataFrame(plan.get("schedule", []))
    preferred = ["title", "start_time", "end_time", "type", "reason"]
    cols = [col for col in preferred if col in df.columns]
    return df[cols] if cols else df


def post_to_slack(message: str, webhook_url: Optional[str] = None) -> bool:
    """Post a message to Slack using an incoming webhook."""
    webhook_url = webhook_url or os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        raise ValueError("Missing Slack webhook URL.")

    response = requests.post(webhook_url, json={"text": message}, timeout=10)
    if response.status_code != 200:
        raise RuntimeError(f"Slack post failed. Status={response.status_code}. Response={response.text}")
    return True


def build_calendar_event_payloads(plan: Dict[str, Any], timezone: str = DEFAULT_TIMEZONE, event_prefix: str = "FocusFlow") -> List[Dict[str, Any]]:
    """Convert FocusFlow schedule items into Google Calendar event payloads."""
    events: List[Dict[str, Any]] = []
    for item in plan.get("schedule", []):
        title = item.get("title", "Untitled FocusFlow Hold")
        start_time = item.get("start_time")
        end_time = item.get("end_time")
        if not start_time or not end_time:
            continue

        events.append({
            "summary": f"{event_prefix}: {title}",
            "description": "Created by FocusFlow Agent.\n\n" + f"Type: {item.get('type', 'focus_block')}\nReason: {item.get('reason', '')}",
            "start": {"dateTime": start_time, "timeZone": timezone},
            "end": {"dateTime": end_time, "timeZone": timezone},
        })
    return events


def calendar_payloads_dataframe(calendar_events: List[Dict[str, Any]]) -> pd.DataFrame:
    """Convert Google Calendar event payloads to a DataFrame for preview."""
    return pd.DataFrame([
        {
            "summary": event.get("summary"),
            "start": event.get("start", {}).get("dateTime"),
            "end": event.get("end", {}).get("dateTime"),
            "timezone": event.get("start", {}).get("timeZone"),
            "description": event.get("description"),
        }
        for event in calendar_events
    ])


def authenticate_google_calendar(credentials_file: str = "credentials.json", token_file: str = "token.json"):
    """Authenticate with Google Calendar using a local Desktop OAuth client."""
    if not os.path.exists(credentials_file):
        raise FileNotFoundError("credentials.json not found. Follow docs/google_calendar_setup.md.")

    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    scopes = ["https://www.googleapis.com/auth/calendar.events"]
    creds = None

    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, scopes)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scopes)
            creds = flow.run_local_server(port=0, prompt="consent")

        with open(token_file, "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


def create_google_calendar_holds(calendar_events: List[Dict[str, Any]], calendar_id: str = "primary", credentials_file: str = "credentials.json", token_file: str = "token.json") -> List[Dict[str, Any]]:
    """Create Google Calendar events from prepared event payloads."""
    service = authenticate_google_calendar(credentials_file=credentials_file, token_file=token_file)

    created: List[Dict[str, Any]] = []
    for event in calendar_events:
        created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
        created.append({
            "summary": created_event.get("summary"),
            "start": created_event.get("start", {}).get("dateTime"),
            "end": created_event.get("end", {}).get("dateTime"),
            "htmlLink": created_event.get("htmlLink"),
            "id": created_event.get("id"),
        })
    return created


def run_focusflow(task_dump: str, available_hours: int = 4, deep_work_preference: str = "Morning", timezone: str = DEFAULT_TIMEZONE, use_mock_mode: bool = True, model_name: str = DEFAULT_MODEL_NAME) -> Dict[str, Any]:
    """Run the planning workflow and prepare integration payloads."""
    plan = generate_focusflow_plan(
        task_dump=task_dump,
        available_hours=available_hours,
        deep_work_preference=deep_work_preference,
        timezone=timezone,
        use_mock_mode=use_mock_mode,
        model_name=model_name,
    )
    is_valid, validation_messages = validate_plan(plan)
    calendar_events = build_calendar_event_payloads(plan, timezone=timezone)
    return {
        "plan": plan,
        "is_valid": is_valid,
        "validation_messages": validation_messages,
        "calendar_events": calendar_events,
    }
