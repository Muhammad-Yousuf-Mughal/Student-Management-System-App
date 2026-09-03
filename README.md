# Student Management System (Django)

A complete web-based Student Management System built with Django that allows educational institutions to manage students, teachers, courses, attendance, and academic records through a centralized platform.

## Features

### Administrator
- Full CRUD on students, teachers, and courses
- Manage departments
- View dashboard with statistics
- View all attendance and academic records
- Bulk enroll students in courses

### Teacher
- View assigned courses and enrolled students
- Mark daily attendance per course
- Enter marks and grades
- View student information
- View course attendance reports

### Student
- View personal profile
- View enrolled courses
- View personal attendance record and percentage
- View marks, grades, and academic results

## Tech Stack
- **Backend:** Python 3.x, Django 5.x/6.x
- **Database:** SQLite (default) / PostgreSQL
- **Frontend:** HTML5, CSS3, Bootstrap 5, Bootstrap Icons
- **Auth:** Django built-in authentication with custom User model

## Project Structure

```
student_management/    # Django project settings
accounts/              # Custom User model + authentication
core/                  # Base views, dashboard, role-based decorators
students/              # Student model, views, forms
teachers/              # Teacher model, views, forms
courses/               # Course, Department, Enrollment models
attendance/            # Attendance model, views, reports
grades/                # Mark/Grade model, views
templates/             # Global HTML templates
static/                # Static assets
```

## Setup Instructions

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run migrations
```bash
python manage.py migrate
```

### 3. Seed sample data (optional)
```bash
python manage.py seed_data
```

### 4. Run the development server
```bash
python manage.py runserver
```

### 5. Open in browser
Visit http://127.0.0.1:8000/

## Default Login Credentials (after seeding)

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@school.com | admin123 |
| Teacher | john.smith@school.com | teacher123 |
| Student | alice.williams@student.com | student123 |

## URL Map

| Path | Description |
|------|-------------|
| `/` | Dashboard (role-based) |
| `/accounts/login/` | Login |
| `/accounts/register/` | Register a new user |
| `/accounts/logout/` | Logout |
| `/accounts/profile/` | User profile |
| `/students/` | Student list |
| `/students/add/` | Add new student (admin) |
| `/students/<id>/` | Student detail |
| `/teachers/` | Teacher list |
| `/teachers/add/` | Add new teacher (admin) |
| `/teachers/<id>/` | Teacher detail |
| `/courses/` | Course list |
| `/courses/add/` | Add new course (admin) |
| `/courses/<id>/` | Course detail |
| `/courses/<id>/enroll/` | Enroll a student |
| `/courses/<id>/bulk-enroll/` | Bulk enroll students |
| `/courses/departments/` | Department list |
| `/attendance/` | Attendance records |
| `/attendance/mark/` | Mark attendance |
| `/attendance/report/<course_id>/` | Course attendance report |
| `/grades/` | Marks list |
| `/grades/add/` | Add marks |
| `/grades/student/<id>/` | Student results |
| `/grades/course/<id>/` | Course marks |
| `/grades/course/<id>/quick-entry/` | Quick bulk entry of marks |
| `/admin/` | Django admin |

## Authentication & Security
- Custom User model extending `AbstractUser`
- Email-based login (no username)
- Role-based access (admin / teacher / student)
- Password-protected routes via `login_required`
- Role-restricted views via custom decorators and mixins
- CSRF protection on all POST forms

## Database Models
- **User** — custom user with `role` field
- **Student** — OneToOne with User, includes student_id, DOB, grade_level, parent info
- **Teacher** — OneToOne with User, includes employee_id, department, qualification
- **Department** — academic department with head teacher
- **Course** — academic course with code, credits, teacher, department
- **Enrollment** — through-model for student-course many-to-many with status and grade
- **Attendance** — student-course-date with status (present/absent/late)
- **Mark** — student-course-exam_type with marks_obtained, max_marks

## Testing

A couple of smoke-test scripts are included:
- `test_smoke.py` — login + page-level smoke tests for all roles
- `test_create.py` — tests for creating students/teachers via admin forms
- `test_crud.py` — tests for creating courses and registering new users

Run with:
```bash
python test_smoke.py
```

## Future Enhancements
- Online fee management
- Email notifications
- PDF report generation
- Examination scheduling
- Parent accounts
- Online admission system
- Notifications & announcements

## Deployment (Railway)

This repository includes `railway.json` for the Railway build and start commands.

1. In Railway, create a new project and deploy the GitHub repository.
2. Add a PostgreSQL database to the project.
3. In the web service variables, add `DATABASE_URL` using the PostgreSQL service's connection URL.
4. Add `SECRET_KEY` with a long random value. Do not reuse the local development key.
5. Set `DEBUG=False` and deploy. Railway's `RAILWAY_PUBLIC_DOMAIN` is used automatically for allowed hosts and CSRF.
6. Open the deployed service and run this once from Railway's shell or one-off command:
   ```
   python manage.py seed_data
   ```

Railway's filesystem is ephemeral. The current profile-picture uploads stored under `media/` can be lost on redeploy or restart. Add a Railway volume mounted at `/app/media`, or configure an object-storage backend before relying on uploaded images in production.

### Railway environment variables

| Var | Purpose |
|-----|---------|
| `SECRET_KEY` | Production Django secret |
| `DEBUG` | Set to `False` |
| `DATABASE_URL` | Connection URL from Railway PostgreSQL |
| `CSRF_TRUSTED_ORIGINS` | Optional comma-separated custom HTTPS origins |
| `EMAIL_HOST` | SMTP server for production email |
| `EMAIL_PORT` | SMTP port, normally `587` |
| `EMAIL_HOST_USER` | SMTP username |
| `EMAIL_HOST_PASSWORD` | SMTP password |
| `EMAIL_USE_TLS` | Set to `True` for SMTP TLS |

## Deployment (Render)

This project is configured for one-click deployment to [Render](https://render.com) (free tier, PostgreSQL included).

### Option A: One-click via render.yaml (easiest)

1. Push the project to a GitHub repository.
2. Go to https://render.com → **New** → **Blueprint**.
3. Connect your GitHub repo. Render will detect `render.yaml` and provision:
   - A free PostgreSQL database (`studentms-db`)
   - A free web service (`student-management-system`) with the right env vars
4. Wait for the first build. Once live, visit your `*.onrender.com` URL.
5. Run the seed command once via the Render Shell:
   ```
   python manage.py seed_data
   ```

### Option B: Manual setup on Render

1. Push the project to GitHub.
2. On Render, create a new **PostgreSQL** database (free plan) and copy its **Internal Connection String**.
3. On Render, create a new **Web Service** from the GitHub repo with:
   - **Environment:** `Python`
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn student_management.wsgi:application --log-file -`
4. Add these environment variables in the Render dashboard:
   - `DATABASE_URL` — paste the connection string from step 2
   - `SECRET_KEY` — click **Generate**
   - `PYTHON_VERSION` — `3.12.0`
   - `WEB_CONCURRENCY` — `2`
5. Wait for the first deploy. Open the **Shell** tab and run:
   ```
   python manage.py seed_data
   ```
6. Visit your `*.onrender.com` URL.

### Environment variables used

| Var | Purpose | Local default |
|-----|---------|---------------|
| `SECRET_KEY` | Django secret key | insecure dev value |
| `DEBUG` | Toggle debug mode | `True` |
| `ALLOWED_HOSTS` | Allowed hostnames | `localhost,127.0.0.1` |
| `DATABASE_URL` | DB connection (auto-set by Render) | falls back to SQLite |

When `DATABASE_URL` is set, Django automatically uses PostgreSQL. Otherwise it falls back to the local SQLite file.

### Why not Vercel?

Vercel is built for stateless serverless functions. Django needs a persistent filesystem (for SQLite, sessions, uploaded media) and a long-running WSGI process, so Vercel is not a good fit. Render / Railway / PythonAnywhere are designed for this.
