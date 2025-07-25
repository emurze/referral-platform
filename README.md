# Referral Platfrom

A simple authentication and user profile management API built with 
Django REST Framework.

## API Documentation

See the [API Documentation](docs/api.md) file for detailed endpoint info.

## Getting Started

### Prerequisites

Before you begin, make sure the following are installed on your system:

- Python 3.12 or higher
- Docker – [https://www.docker.com/](https://www.docker.com/)
- Poetry – [https://python-poetry.org/](https://python-poetry.org/)

### Installation Guide

#### 1. Clone the repository from GitHub

First, clone the repository to your local machine using Git:

```bash
git clone git@github.com:emurze/referral-platform.git
```

Navigate to the project folder:

```bash
cd referral-platform
```

#### 2. Install dependencies using Poetry

Make sure you have **Poetry** installed. If not, install it by following the instructions on the official Poetry website:  
https://python-poetry.org/docs/#installation

Then, install all project dependencies, including development dependencies:

```bash
poetry install --with dev
```

#### 3. Set up environment file

Create a `.env.prod` configuration file to define environment variables. Example:

```bash
touch .env.prod
```

Sample content of `.env.prod`:

```ini
# Application settings
PYTHONPATH = src
DJANGO_ENV = production
SECRET_KEY = secret_key  # Insert your own secret key here
ALLOWED_HOSTS = 0.0.0.0

# Database settings
DB_NAME = db
DB_USER = user
DB_PASSWORD = 12345678
DB_HOST = db

# PostgreSQL settings
POSTGRES_DB = db
POSTGRES_USER = user
POSTGRES_PASSWORD = 12345678
```

#### 4. Run the app in production mode

To run the application in production mode, use the following command:

```bash
poetry run poe up_prod
```

This will execute `docker compose up` and start all required containers.  
Once running, the application will be available at: [http://0.0.0.0:80](http://0.0.0.0:80)

#### 5. In case of issues

If you encounter issues during startup, you might already have running Docker containers conflicting with this setup.  
To stop and remove all production containers, use the command:

```bash
poetry run poe down_prod -v
```

This will remove all containers created for the production environment so you can restart the system cleanly.

---

### Development Environment Guide

If you want to work in a **development environment**, follow the steps below.

#### 1. Install development dependencies

Install all required development dependencies (same as step 2):

```bash
poetry install --with dev
```

#### 2. Start development infrastructure

To start the application in development mode with necessary containers, run:

```bash
poetry run poe up -d
```

#### 3. Apply migrations

To apply database migrations, use the command:

```bash
poetry run poe migrate
```

#### 4. Run the local application

To start the local development server, use the command:

```bash
poetry run poe runserver
```

The application will be available at [http://localhost:8000](http://localhost:8000) unless configured otherwise.

---

### Useful Commands

- **Stop production containers**:

```bash
poetry run poe down_prod -v
```

- **Stop development containers**:

```bash
poetry run poe down -v
```
