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

1. Push to GitHub
2. Create Web Service on Render, connect repo
3. Set `FLASK_CONFIG=production`, `SECRET_KEY`, `DATABASE_URL`
4. Build: `pip install -r requirements.txt`
5. Start: `gunicorn run:app`
6. Run `flask init-db` and `flask seed` via Render shell

## Environment Variables

See `.env.example` for all options.

## License

Proprietary — Ridge School of Anaesthesia
