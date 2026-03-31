from pathlib import Path

import uvicorn
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.repositories.log_repository import LogRepository
from app.repositories.movie_repository import MovieRepository

app = FastAPI(title="CineQuery Web")

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "web" / "templates"))

static_path = BASE_DIR / "web" / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

movie_repo = MovieRepository()
log_repo = LogRepository()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Renders the main search page with categories and year range."""
    categories = movie_repo.get_all_categories()
    min_y, max_y = movie_repo.get_year_range()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "view": "search",
            "categories": categories,
            "min_year": min_y,
            "max_year": max_y,
            "current_start": min_y,
            "current_end": max_y,
            "movies": [],
        },
    )


@app.post("/search", response_class=HTMLResponse)
async def search(
    request: Request,
    keyword: str = Form(None),
    category: str = Form("All"),
    year_start: int = Form(None),
    year_end: int = Form(None),
):
    """Processes search requests by title, category, or year range."""
    min_db, max_db = movie_repo.get_year_range()
    start = year_start if year_start is not None else min_db
    end = year_end if year_end is not None else max_db

    movies = []

    if keyword and keyword.strip():
        movies, _ = movie_repo.search(keyword, page=1)
    elif category:
        target_categories = [category] if category != "All" else movie_repo.get_all_categories()
        movies, _ = movie_repo.find_by_category_and_year(
            categories=target_categories,
            start=start,
            end=end,
            page=1,
            limit=500,
        )

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "movies": movies,
            "view": "search",
            "categories": movie_repo.get_all_categories(),
            "min_year": min_db,
            "max_year": max_db,
            "current_start": start,
            "current_end": end,
            "last_keyword": keyword,
            "selected_cat": category,
        },
    )


@app.get("/analytics", response_class=HTMLResponse)
async def analytics(request: Request):
    """Displays top search queries from the analytics repository."""
    return templates.TemplateResponse(
        "index.html", {"request": request, "stats": log_repo.get_top_queries(), "view": "analytics"}
    )


@app.get("/history", response_class=HTMLResponse)
async def history(request: Request):
    """Displays the recent search activity history."""
    return templates.TemplateResponse(
        "index.html", {"request": request, "history": log_repo.get_history(), "view": "history"}
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
