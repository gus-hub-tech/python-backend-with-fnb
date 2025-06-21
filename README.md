# 📝 Django Survey API & Node.js Data Display

This repository provides a Django REST Framework backend for creating and managing surveys, along with a Node.js + Express example for fetching and displaying survey data. It serves as both a Django API starter template and a full-stack example for integrating Django with a Node.js frontend.

---

## 📚 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Django Backend](#django-backend)
  - [Survey API](#survey-api)
  - [Authentication](#authentication)
  - [Requirements](#requirements)
- [Node.js Example](#nodejs-example)
  - [Setup Steps](#setup-steps)
  - [Important Considerations](#important-considerations)
- [Development Environment](#development-environment)
- [License](#license)

---

## Project Overview

- **Django Backend:** Provides a REST API for surveys with full CRUD (Create, Read, Update, Delete) support, requiring authentication. Built with Django and Django REST Framework.
- **Node.js Example:** Demonstrates how to fetch data from the Django API using an Express server and display it with EJS templates.

---

## Features

- 🔒 **Authentication Required:** Uses Django REST Framework's token/session authentication.
- 📝 **Survey CRUD:** Create, retrieve, update, and delete surveys.
- 👤 **User Tracking:** Automatically records which user created each survey.
- 🧩 **Modular Architecture:** Clean separation for scalability and maintainability.
- 🌐 **Node.js Integration Example:** Fetches and displays API data using Express and EJS.

---

## Project Structure

```
python-backend-with-fnb/
├── mysite/
│   ├── requirements.txt
│   └── mysite/
│       └── settings.py
├── surveys/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── node-js-api-connection.md
├── surv.md
├── README.md
└── manage.py
```

---

## Django Backend

### Survey API

- **SurveyCreateViewSet**: Main endpoint for survey CRUD operations.
- All operations are restricted to authenticated users.
- On creation, the `created_by` field is set to the current user.

#### Example Model (`surveys/models.py`):

```python
from django.db import models
from django.contrib.auth.models import User

class Survey(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    # Add more fields as needed
```

### Authentication

- Uses DRF token/session authentication.
- Only authenticated users can manage surveys.

### Requirements

Main Python dependencies (see `mysite/requirements.txt`):

```
Django==5.0.11
djangorestframework
asgiref==3.7.2
sqlparse==0.4.4
typing_extensions==4.9.0
```
> Install packages with:  
> `pip install -r mysite/requirements.txt`

---

## Node.js Example

The `node-js-api-connection.md` file provides a step-by-step guide to building a Node.js Express server that fetches survey data from the Django API and renders it using EJS.

### Setup Steps

1. **Install Node.js and npm**  
   [Download here](https://nodejs.org/)

2. **Initialize the Project**
   ```bash
   mkdir django-data-display
   cd django-data-display
   npm init -y
   ```

3. **Install Dependencies**
   ```bash
   npm install express axios ejs bootstrap@5
   ```

4. **Create Server and Views**
   - Build `server.js` to request data from the Django API.
   - Create the `views` directory and add `display.ejs` for rendering.

5. **Run the App**
   ```bash
   node server.js
   ```
   Visit `http://localhost:<port>` to view data.

### Important Considerations

- **CORS:** Use `django-cors-headers` in Django if accessing from a different port.
- **Error Handling:** Add robust error handling for production use.
- **Security:** Never expose secrets or sensitive data.
- **Styling:** Use Bootstrap or other CSS frameworks for better UI.

---

## Development Environment

- Uses Nix for reproducible environments (see `.idx/dev.nix`).
- VSCode extension recommendations for Python development.

---

## License

This project is for educational and demonstration purposes.  
See individual files for additional licensing information if present.

---

**Feel free to expand, adapt, or integrate this template to fit your own full-stack Django and Node.js applications!**


# Django

A Django starter template as per the docs: https://docs.djangoproject.com/en/5.0/intro/tutorial01/

