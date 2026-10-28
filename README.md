# GPT-Based Code Review System

A web application built with **Python, Django, MySQL, HTML & CSS** that reviews
submitted source code and gives students automated, structured feedback to
support programming education.

## Features
- **User authentication** — register, login, logout (Django auth)
- **Code submission** — paste code, pick a language, submit for review
- **Automated review engine** — dual-mode:
  - If `OPENAI_API_KEY` is set, reviews are generated via the OpenAI Chat
    Completions API (true "GPT-based" review).
  - Otherwise, a built-in static-analysis engine detects real issues
    (bare `except:`, hardcoded secrets, long lines, missing docstrings,
    print statements, wildcard imports, long functions, etc.) and computes
    a 0–100 quality score — so the app is fully functional with **zero**
    external setup.
- **Review history** — every submission and its review is stored and listed
- **Responsive UI** — clean, mobile-friendly HTML/CSS, no framework needed
- **MySQL-backed** — structured storage for users, submissions, and reviews
  (SQLite fallback for instant local development)

## Quick start (local demo — SQLite, no setup)

```bash
python -m venv venv
source venv/bin/activate        # venv\Scripts\activate on Windows
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser   # optional, for /admin/
python manage.py runserver
```

Visit http://127.0.0.1:8000/, register an account, and submit some code.

## Switching to MySQL

1. Create a database: `CREATE DATABASE code_review_db;`
2. Copy `.env.example` to `.env` and set:
   ```
   DB_ENGINE=mysql
   DB_NAME=code_review_db
   DB_USER=root
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=3306
   ```
   (Uses `PyMySQL`, a pure-Python driver — no system build tools needed.)
3. Run `python manage.py migrate` again to create tables in MySQL.

## Enabling real GPT-based reviews

Set `OPENAI_API_KEY` (and optionally `OPENAI_MODEL`, default `gpt-4o-mini`)
in your `.env`. When present, `reviewer/review_engine.py` calls the OpenAI
API with a prompt engineered for accurate, education-focused code review
and falls back automatically to the static-analysis engine if the call
fails for any reason.

## Project structure

```
codereview_system/
├── codereview/            # Django project settings/urls
├── reviewer/              # Main app
│   ├── models.py          # CodeSubmission, Review
│   ├── views.py           # auth, submit, dashboard, history, detail
│   ├── forms.py
│   ├── review_engine.py   # GPT / static-analysis review logic
│   ├── admin.py
│   └── urls.py
├── templates/reviewer/    # HTML templates
├── static/reviewer/css/   # Responsive stylesheet
├── requirements.txt
└── .env.example
```

## Resume bullet mapping

- *Developed a web-based application that reviews submitted source code and
  provides automated programming feedback* → `review_engine.py` + `Review` model
- *User authentication, code submission, review history, application workflow
  modules* → `register/login/logout`, `submit_code`, `review_history`,
  `CodeSubmission.status` workflow (pending → reviewed/failed)
- *Integrated MySQL for structured storage* → `settings.py` MySQL config via PyMySQL
- *Responsive web interface* → `static/reviewer/css/style.css`
