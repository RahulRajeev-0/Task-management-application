
# 🗂️ Task Management Application

A simple yet robust Django-based Task Management system with Django REST Framework, JWT authentication, and role-based access control.

---

## 🚀 Features

- 🧑‍💼 Role-Based Access (`Admin`, `SuperAdmin`, `User`)
- ✅ Task CRUD with status tracking and User Management
- 🔒 JWT Authentication (Login, Refresh)
- 📝 Assign tasks to users
- 🧾 Completion report & worked hours on task completion
- 🔍 API endpoints to manage and view tasks
- 🌐 Admin Panel Frontend 

---

## 🏗️ Tech Stack

- Backend: **Django**, **Django REST Framework**
- Auth: **djangorestframework-simplejwt**
- Database: **SQLite** (can be switched)
- UI: **Tailwind CSS**, Django Templates

---

## API Documentation

For detailed API documentation (user api endpoints only), visit [API Docs](https://documenter.getpostman.com/view/31743247/2sB2qWH4Yo)

---

## 📦 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/RahulRajeev-0/Task-management-application.git
cd Task-management-application
````

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```


### 4. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Run Server

```bash
python manage.py runserver
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

---


## 🧑 Roles & Permissions

| Role       | Description                       |
| ---------- | --------------------------------- |
| SuperAdmin | Full access including reports     |
| Admin      | Assign tasks, view reports        |
| User       | View own tasks, mark as completed |

---

## 📌 TODOs / Improvements

* ✅ Add pagination and filtering to APIs
* 🔒 Improve permission classes
---

## 👤 Author

**Rahul** – Full Stack Developer (Django + React)
Feel free to connect or contribute!

---



