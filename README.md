# 🎬 CineQuery

**CineQuery** is an interactive application for searching movies in the
**Sakila (MySQL)** database with logging of user queries in
**MongoDB**.
The project follows clean architecture principles, supports two
interfaces (TUI and Web), and includes a query analytics system.

The project provides two interfaces:

-   🖥 **TUI (Textual UI)** --- a modern terminal-based interface
-   🌐 **Web (FastAPI)** --- a web interface with templates

------------------------------------------------------------------------

# 🚀 Features

### 🔍 Movie Search

-   Search by keyword (movie title)
-   Pagination (10 results per page)
-   Ability to load all results

### 📂 Filtering

-   By genre (multi-select)
-   By year range
-   Combined filtering

### 📊 Analytics

-   Top 5 most popular queries
-   Recent search history

### 🧠 Logging

-   All queries are stored in MongoDB
-   Stored data includes:
    -   query text
    -   number of results
    -   search type
    -   parameters
    -   timestamp

------------------------------------------------------------------------

# 🏗 Project Architecture

The project is built following clean architecture principles:

    ├── app/
    │   ├── core/           # Database connections and configuration
    │   ├── models/         # Domain models (Movie Dataclass)
    │   ├── repositories/   # Data access layer (SQL/NoSQL logic)
    ├── cli/                # TUI logic (Textual)
    ├── web/                # Templates and static files for Web
    ├── tests/              # Automated tests
    ├── main.py             # TUI entry point
    └── run_web.py          # Web entry point

### 🔑 Key Principles

-   Separation of concerns\
-   Repository pattern\
-   Minimal code duplication\
-   PEP8 compliance

------------------------------------------------------------------------

# 🛠 Technologies

-   Python 3.10+
-   MySQL\
-   MongoDB\
-   FastAPI\
-   Textual (TUI)\
-   pymysql / pymongo\
-   Jinja2\
-   pytest

------------------------------------------------------------------------

# ⚙️ Installation & Setup

## 1. Clone the repository

``` bash
git clone <your-repo>
cd CineQuery
```

## 2. Create a virtual environment

``` bash
python -m venv venv

# Linux / Mac
source venv/bin/activate  

# Windows
venv\Scripts\activate
```

## 3. Install dependencies

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## 4. Environment Configuration

Create a `.env` file based on `.env.example`.

------------------------------------------------------------------------

## 5. Database Setup

### MySQL

-   Install MySQL\
-   Import the **Sakila** database

### MongoDB

-   Install MongoDB locally or use MongoDB Atlas

------------------------------------------------------------------------

# ▶️ Running the Application

## 🖥 TUI Version

``` bash
python main.py
```

## 🌐 Web Version

``` bash
python run_web.py
```

------------------------------------------------------------------------

# 🧪 Testing

``` bash
pytest tests
```

Coverage includes:

-   Repository layer\
-   Models\
-   Logging

------------------------------------------------------------------------

## 📌 Purpose

This project demonstrates:

-   Clean Architecture\
-   Working with SQL + NoSQL\
-   Building CLI + Web applications

------------------------------------------------------------------------

## 👨‍💻 Author

Educational project for portfolio purposes.
