# HVAC Service Management System

A Django-based web application for managing HVAC service cases and vehicle maintenance records. The system supports multilingual content (Ukrainian/English) and provides an administrative interface for managing service cases, vehicles, and company information.

## Features

- 🌐 Multilingual support (Ukrainian/English)
- 📱 Responsive design with Bootstrap
- 🚗 Vehicle management system with support for:
  - Different vehicle types (Fuel Engine, Electric, Hybrid)
  - Automatic engine capacity handling based on vehicle type
  - Case documentation and image management
- 💼 Service case management
- 📝 Rich text editing with CKEditor 5
- 🖼️ Image handling with automatic optimization
- 🔄 HTMX integration for enhanced interactivity

## Technologies Used

- Django 5.0.3
- Python 3.10
- Bootstrap 5
- CKEditor 5
- HTMX
- SQLite (Database)

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd hvac
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create database:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Collect static files:
```bash
python manage.py collectstatic
```

## Environment Setup

Create a `.env` file in the project root and configure the following variables:
```env
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
TIME_ZONE=Europe/Kiev
```

## Running the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000`

## Project Structure

```
hvac/
├── cases/                  # Main application directory
│   ├── admin.py           # Admin interface configuration
│   ├── forms.py           # Form definitions
│   ├── models.py          # Database models
│   ├── signals.py         # Signal handlers
│   ├── views.py           # View definitions
│   ├── static/            # Static files (CSS, JS)
│   └── templates/         # HTML templates
├── hvac/                  # Project configuration
├── locale/                # Translation files
│   ├── en/               # English translations
│   └── uk/               # Ukrainian translations
├── media/                # User-uploaded files
├── static/               # Collected static files
└── templates/            # Project-wide templates
```

## Translations

To create or update translations:

1. Generate message files:
```bash
python manage.py makemessages -l uk
python manage.py makemessages -l en
```

2. Edit translation files in `locale/[lang]/LC_MESSAGES/django.po`

3. Compile translations:
```bash
python manage.py compilemessages
```

## Admin Interface

Access the admin interface at `/admin` with your superuser credentials to manage:
- Cases
- Vehicles
- Services
- Contact Information
- About Messages

## Contributing

1. Create a feature branch
2. Commit your changes
3. Push to the branch
4. Create a Pull Request

## License

[Your License Here]

## Support

[Your Contact Information or Support Instructions]