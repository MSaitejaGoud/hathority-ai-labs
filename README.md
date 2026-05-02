# Hathority AI Labs

A Django web platform that displays AI agent projects built by the Hathority team
(e.g. Boomi Agents, Boomi AI Agents, Active Agents). All content is managed
exclusively via the Django Admin. The frontend uses only HTML5, CSS3, and
vanilla JavaScript — no React, Vue, Tailwind, or build tools.

## Features

- Responsive homepage with a card grid of all projects
- Search bar that filters by title, short description, or category (`?q=`)
- Project detail page with full description, metadata, and back navigation
- Fully configured Django Admin (list filters, search, image upload)
- Status badges (Live / Completed / In Progress / Planned)
- Clean, modern, AI/tech aesthetic (dark blue + teal accents)

## Tech Stack

- Python 3.10+
- Django 5.x
- Pillow (for `ImageField` uploads)
- SQLite (default dev database)

## Project Structure

```
hathority-ai-labs/
├── core/                     # Django settings, root URLs, WSGI/ASGI
├── projects/                 # Main app (models, views, admin, templates)
│   └── templates/projects/
│       ├── base.html
│       ├── home.html
│       └── project_detail.html
├── static/
│   ├── css/style.css
│   └── js/main.js
├── media/                    # Uploaded project images (created at runtime)
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd hathority-ai-labs

# 2. Create + activate a virtual environment
python -m venv venv
source venv/bin/activate            # macOS / Linux
# venv\Scripts\activate             # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py migrate

# 5. Create an admin user
python manage.py createsuperuser

# 6. Run the dev server
python manage.py runserver
```

Then open:

- Site: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

Add projects from the admin — they will appear instantly on the homepage.

## Hathority Team Workflow (3 people, 1 primary dev)

- `main` is **protected** and always production-ready
- Always `git pull` **before** `git push`
- Use feature branches: `git checkout -b feature/<short-name>`
- Open a PR into `main`; primary dev reviews & merges
- Never commit `db.sqlite3`, `media/`, or `.env` (already in `.gitignore`)

## About

Built by the Hathority AI Labs team — showcasing intelligent systems, Boomi AI Agents, and active autonomous workflows.

## Notes

- Media uploads work in development because `core/urls.py` serves
  `MEDIA_URL` via `static()` when `DEBUG=True`.
- For production, configure a real web server (nginx + gunicorn) and a
  proper static/media file strategy (S3, WhiteNoise, etc.).
