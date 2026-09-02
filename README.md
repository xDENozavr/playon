# PlayOn

A Django web platform for a city basketball league - team registration, tournament calendar, and team rankings.

**Live demo:** https://playon-0cyx.onrender.com/playon/
**Note:** hosted on Render's free tier - the app may take up to 50 seconds to wake up on the first request after a period of inactivity.

## Features

- Custom user authentication (registration, login, session management) via a JSON API that interacts with the frontend
- Team creation with validated eligibility rules (gender/age compatibility with the selected category, checked against the team captain's profile)
- Event registration flow: users pick one of their own teams, with server-side validation for gender, age, and team type (basketball 5x5 / streetball 3x3) before registration is allowed
- Team rankings computed from game results (wins/losses), optimized with `select_related`/`prefetch_related`/`annotate()` - reduced query count from 155 to 7 on a key page (verified with Django Debug Toolbar)
- Editable player profiles (height, phone, avatar) with custom Django validators
- Admin customization for managing clubs, teams, categories, and events
- Mobile-responsive design, including a custom hamburger navigation menu

## Tech stack

- **Backend:** Python, Django, Django REST Framework
- **Database:** PostgreSQL (via Django ORM)
- **Frontend:** HTML/CSS, vanilla JavaScript
- **Auth:** JWT (djangorestframework-simplejwt) for the API layer
- **Media storage:** Cloudinary (production)
- **Static files:** WhiteNoise
- **Testing:** Django TestCase, DRF APIClient, JWT-based permission tests
- **Deployment:** Render

## Running locally

```bash
git clone https://github.com/xDENozavr/playon.git
cd playon
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=playon_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
```

Then:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Project structure

```
core/          - teams, events, clubs, categories, admin customization
blog/          - homepage, news
users/         - authentication, player profiles
config/        - project settings, URL routing
```

## About this project

Built as a personal portfolio project to practice Django fundamentals: custom user models, form/model validation, query optimization, JWT authentication, and automated testing.
