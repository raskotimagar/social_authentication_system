# 🌐 Social Authentication System

A Django-based authentication system with support for social login (Google, GitHub, etc.) using `django-allauth` and styled with Tailwind CSS.

---

## 🚀 Features

- Traditional email/password signup and login
- Social authentication (Google, GitHub, etc.)
- Tailwind CSS styling for modern UI
- Custom user fields (e.g. phone number, username)
- Extendable and easy to customize

---

## 📦 Tech Stack

- **Backend:** Django, django-allauth
- **Frontend:** Tailwind CSS
- **Auth:** OAuth2 (via allauth)

---

## 🛠️ Installation

```bash
git clone https://github.com/your-username/social_authentication_system.git
cd social_authentication_system

# Set up virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
