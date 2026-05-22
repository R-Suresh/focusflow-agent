"""
FocusFlow local Streamlit app.

Run:
    streamlit run app.py
"""

from __future__ import annotations

import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from focusflow_core import (
    DEFAULT_MODEL_NAME,
    DEFAULT_TIMEZONE,
    calendar_payloads_dataframe,
    create_google_calendar_holds,
    post_to_slack,
    run_focusflow,
    schedule_dataframe,
    tasks_dataframe,
)

load_dotenv()

st.set_page_config(page_title="FocusFlow Agent", page_icon="🧭", layout="wide")

st.title("🧭 FocusFlow Agent")
st.caption("Turn messy tasks into a focused daily plan, Slack summary, and calendar-ready holds.")

with st.sidebar:
    st.header("Settings")

    use_mock_mode = st.toggle(
        "Use mock mode",
        value=True,
        help="Try the app without OpenAI, Slack, or Google setup.",
    )

    model_name = st.text_input("OpenAI model", value=DEFAULT_MODEL_NAME)
    available_hours = st.slider("Available hours today", 1, 12, 4)
    deep_work_preference = st.selectbox(
        "Deep work preference",
        ["Morning", "Afternoon", "Evening", "No preference"],
        index=0,
    )
    timezone = st.text_input("Timezone", value=DEFAULT_TIMEZONE)

    st.divider()
    st.subheader("Integrations")

    enable_slack_posting = st.toggle(
        "Enable Slack posting",
        value=False,
        help="Requires SLACK_WEBHOOK_URL in .env.",
    )

    enable_calendar_creation = st.toggle(
        "Enable Google Calendar creation",
        value=False,
        help="Requires credentials.json in the project root.",
    )

    st.divider()
    st.subheader("Setup status")

    st.write(f"OpenAI key: {'✅ Found' if os.getenv('OPENAI_API_KEY') else '⚠️ Missing'}")
    st.write(f"Slack webhook: {'✅ Found' if os.getenv('SLACK_WEBHOOK_URL') else '⚠️ Missing'}")
    st.write(f"Google credentials: {'✅ Found' if os.path.exists('credentials.json') else '⚠️ Missing'}")

    if not use_mock_mode and not os.getenv("OPENAI_API_KEY"):
        st.warning("Mock mode is off, but OPENAI_API_KEY is missing.")

default_task_dump = """I need to prepare slides for Friday, email Sam, review an AI paper,
book a dentist appointment, finish project update, go to the gym,
pay rent, and plan the meetup agenda.

I have 4 hours today and prefer deep work in the morning.
"""

task_dump = st.text_area(
    "Paste your messy task dump",
    value=default_task_dump,
    height=180,
)

generate = st.button("Generate FocusFlow Plan", type="primary")

if generate:
    if not task_dump.strip():
        st.error("Please paste a task dump first.")
    else:
        with st.spinner("Generating FocusFlow plan..."):
            try:
                result = run_focusflow(
                    task_dump=task_dump,
                    available_hours=available_hours,
                    deep_work_preference=deep_work_preference,
                    timezone=timezone,
                    use_mock_mode=use_mock_mode,
                    model_name=model_name,
                )
                st.session_state["focusflow_result"] = result
                st.success("FocusFlow plan generated.")
            except Exception as exc:
                st.exception(exc)

if "focusflow_result" not in st.session_state:
    st.info("Paste a task dump and click **Generate FocusFlow Plan** to begin.")
else:
    result = st.session_state["focusflow_result"]
    plan = result["plan"]
    calendar_events = result["calendar_events"]

    plan_tab, schedule_tab, slack_tab, calendar_tab, safety_tab = st.tabs(
        ["Prioritized Plan", "Schedule", "Slack", "Calendar", "Safety Check"]
    )

    with plan_tab:
        st.subheader("Prioritized Task Table")
        df = tasks_dataframe(plan)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No tasks found.")
    with schedule_tab:
        st.subheader("Today's Schedule")
        df = schedule_dataframe(plan)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No schedule found.")

        st.subheader("Risks")
        for risk in plan.get("risks", []):
            st.warning(risk)

        st.subheader("Next Best Action")
        st.success(plan.get("next_best_action", "No next action generated."))

    with slack_tab:
        st.subheader("Slack Message Preview")
        slack_message = plan.get("slack_message", "")
        st.code(slack_message, language="markdown")

        if enable_slack_posting:
            if not os.getenv("SLACK_WEBHOOK_URL"):
                st.error("SLACK_WEBHOOK_URL is missing from .env.")
            elif st.button("Post Daily Plan to Slack"):
                try:
                    post_to_slack(slack_message)
                    st.success("Posted to Slack.")
                except Exception as exc:
                    st.exception(exc)
        else:
            st.info("Slack posting is disabled in the sidebar.")

    with calendar_tab:
        st.subheader("Calendar Holds Preview")
        calendar_df = calendar_payloads_dataframe(calendar_events)
        if not calendar_df.empty:
            st.dataframe(calendar_df, use_container_width=True)
        else:
            st.warning("No calendar events prepared.")

        if enable_calendar_creation:
            if not os.path.exists("credentials.json"):
                st.error("credentials.json not found. Follow docs/google_calendar_setup.md.")
            else:
                st.warning("This will create real Google Calendar events. Review the preview first.")
                if st.button("Create Google Calendar Holds"):
                    try:
                        created_events = create_google_calendar_holds(calendar_events=calendar_events)
                        created_df = pd.DataFrame(created_events)
                        st.success(f"Created {len(created_events)} calendar holds.")
                        st.dataframe(created_df, use_container_width=True)
                        for item in created_events:
                            if item.get("htmlLink"):
                                st.link_button(f"Open: {item.get('summary', 'Calendar event')}", item["htmlLink"])
                    except Exception as exc:
                        st.exception(exc)
        else:
            st.info("Google Calendar creation is disabled in the sidebar.")

    with safety_tab:
        st.subheader("Validation Results")
        if result["is_valid"]:
            st.success("Plan structure passed validation.")
        else:
            st.error("Plan structure needs review.")

        for message in result["validation_messages"]:
            st.write(f"- {message}")

        st.subheader("Action Safety")
        st.write(f"- Mock mode: {'ON' if use_mock_mode else 'OFF'}")
        st.write(f"- Slack posting: {'ENABLED' if enable_slack_posting else 'DISABLED'}")
        st.write(f"- Calendar creation: {'ENABLED' if enable_calendar_creation else 'DISABLED'}")
        st.caption("FocusFlow follows a preview-before-action pattern: generate, preview, validate, then act.")
