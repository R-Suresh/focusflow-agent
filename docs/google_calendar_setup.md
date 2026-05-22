# Google Calendar Setup for FocusFlow

This guide is only needed if you want the local Streamlit app to create real Google Calendar holds.

The app works in preview mode without this setup.

## What you will create

You will create a Google OAuth client file named:

```text
credentials.json
```

This file stays local on your machine. Do not commit it to GitHub.

## Step 1: Create a Google Cloud project

1. Go to Google Cloud Console.
2. Create a new project.
3. Suggested name: `FocusFlow Calendar Demo`.

## Step 2: Enable Google Calendar API

1. Go to **APIs & Services → Library**.
2. Search for **Google Calendar API**.
3. Click **Enable**.

## Step 3: Configure OAuth consent

1. Go to **Google Auth Platform** or **OAuth consent screen**.
2. Create/configure the app.
3. Suggested app name: `FocusFlow Calendar Demo`.
4. Use your email for support/developer contact.
5. Keep the app in **Testing** mode.

## Step 4: Add yourself as a test user

1. Go to **Audience**.
2. Find **Test users**.
3. Add the Gmail account whose calendar you want to update.

## Step 5: Add Calendar scope

1. Go to **Data Access**.
2. Click **Add or remove scopes**.
3. Add this scope:

```text
https://www.googleapis.com/auth/calendar.events
```

4. Save.

## Step 6: Create OAuth client

1. Go to **Clients** or **Credentials**.
2. Click **Create OAuth client**.
3. Application type: **Desktop app**.
4. Suggested name: `FocusFlow Local Calendar Client`.
5. Download the JSON file.

## Step 7: Rename and place the file

Rename the downloaded JSON file to:

```text
credentials.json
```

Place it in the root of this repository, next to `app.py`.

## Step 8: Run the local Streamlit app

```bash
streamlit run app.py
```

In the sidebar:

1. Generate a FocusFlow plan.
2. Enable **Google Calendar creation**.
3. Review the Calendar tab preview.
4. Click **Create Google Calendar Holds**.

The first time you create holds, your browser will open a Google OAuth flow.

If you see an unverified app warning, use:

```text
Advanced → Go to FocusFlow Calendar Demo
```

This is expected for your own testing app.

## Safety notes

Do not commit these files:

```text
credentials.json
token.json
.env
```

The app creates `token.json` after the first successful Google login. This file is also private.
