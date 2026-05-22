# Ridge School of Anaesthesia Management System

Enterprise-grade Flask web platform for a School of Anaesthesia — public website, student portal, and admin dashboard.

## Tech Stack

- **Backend:** Flask, Flask-Login, Flask-WTF, SQLAlchemy
- **Database:** PostgreSQL (production) / SQLite (development)
- **Frontend:** Bootstrap 5, Tailwind CSS, Font Awesome, AOS, Chart.js
- **Deploy:** Gunicorn + Render

## Quick Start

```bash
cd school_anaesthesia
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env

flask --app run init-db
flask --app run seed
python run.py
```

Open **http://localhost:5000**

### Default Accounts

| Role    | Email                         | Password      |
|---------|-------------------------------|---------------|
| Admin   | admin@ridgeanaesthesia.edu    | Admin@2024!   |
| Student | student@ridgeanaesthesia.edu  | Student@2024! |

## Project Structure

```
school_anaesthesia/
├── app/
│   ├── auth/          # Login, password reset
│   ├── admin/         # Admin dashboard & CRUD
│   ├── student/       # Student portal
│   ├── models/        # SQLAlchemy models
│   ├── routes/        # Public pages
│   ├── forms/         # WTForms
│   ├── utils/         # Files, QR, email, reports
│   ├── api/           # JSON API for charts
│   ├── templates/
│   └── static/
├── config.py
├── run.py
└── requirements.txt
```

## Features

- Public website: Home, About, Programmes, Admissions, News, Events, Gallery
- Online applications with tracking ID
- Role-based auth: Admin, Lecturer, Student
- Student portal: Results, timetable, materials, assignments, clinical postings, QR ID card
- Admin dashboard: Charts, student/lecturer management, applications, clinical rotations
- Dark mode, search, live announcement ticker, CSV export

## Deploy to Render

Repo: [github.com/khobie/buildbyowusu-soa](https://github.com/khobie/buildbyowusu-soa)

### Option A — Blueprint (recommended)

1. Sign in at [render.com](https://render.com) → **New** → **Blueprint**
2. Connect **khobie/buildbyowusu-soa** and apply `render.yaml`
3. Wait for the web service and **ridge-db** PostgreSQL to deploy
4. Open your site URL (e.g. `https://ridge-anaesthesia.onrender.com`)

5. **Shell** (required on free tier — pre-deploy commands are not supported):

```bash
flask --app run init-db
flask --app run seed
```

### Option B — Manual Web Service

1. **New** → **Web Service** → connect the GitHub repo
2. **Runtime:** Python 3 · **Build:** `pip install -r requirements.txt`
3. **Start:** `gunicorn run:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
4. **New** → **PostgreSQL** (free), copy **Internal Database URL**
5. Environment variables:

| Key | Value |
|-----|--------|
| `FLASK_CONFIG` | `production` |
| `SECRET_KEY` | (generate a long random string) |
| `DATABASE_URL` | (paste Postgres URL from step 4) |

6. **Shell** (first deploy only):

```bash
flask --app run init-db
flask --app run seed
```

### After deploy

- **Admin:** `admin@ridgeanaesthesia.edu` / `Admin@2024!` — change the password immediately
- Free tier sleeps after inactivity; first visit may take ~30s to wake

## Environment Variables

See `.env.example` for all options.

## License

Proprietary — Ridge School of Anaesthesia
