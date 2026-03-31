from typing import List

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Input,
    Label,
    OptionList,
    SelectionList,
    Static,
    TabbedContent,
    TabPane,
)
from textual.widgets.option_list import Option
from textual.widgets.selection_list import Selection

from app.models.movie import Movie
from app.repositories.log_repository import LogRepository
from app.repositories.movie_repository import MovieRepository


class CineQueryApp(App):
    """Main TUI application for movie searching and filtering."""

    TITLE = "CINEQUERY ENGINE"
    BINDINGS = [
        ("q", "quit", "Exit"),
        ("d", "toggle_dark", "Theme"),
    ]

    CSS = """
        Screen { background: $surface; }
        DataTable { height: 1fr; border: tall $primary; margin: 1 0; }
        Input { margin: 0 0 1 0; border: double $secondary; }

        SelectionList {
            height: 8;
            border: double $accent;
            margin: 1 0;
            background: $panel;
        }

        .year-selector {
            height: 5;
            border: double $secondary;
            margin: 1 0;
            width: 1fr;
        }

        #active_filters_info {
            padding: 1 2;
            background: $accent-darken-3;
            color: $text;
            margin: 1 0;
            border: solid $accent;
            text-style: bold;
        }

        #button_row {
            height: auto;
            width: 100%;
        }

        #button_row Button {
            margin-right: 2;
        }

        TabPane { padding: 1; }
    """

    def __init__(self):
        """Initializes application state and repositories."""
        super().__init__()
        self.movie_repo = MovieRepository()
        self.log_repo = LogRepository()
        self.min_db, self.max_db = self.movie_repo.get_year_range()

        self.search_page = 1
        self.category_page = 1
        self.last_keyword = ""
        self.selected_genres = []
        self.start_y = self.min_db
        self.end_y = self.max_db

    def compose(self) -> ComposeResult:
        """Defines the TUI layout and widgets."""
        yield Header(show_clock=True)
        with TabbedContent():
            with TabPane("🔎 Search", id="search_tab"):
                yield Label("Search by title:")
                yield Input(placeholder="Keyword...", id="keyword_input")
                yield DataTable(id="movie_table")
                yield Button("Load 10 More", id="next_search_btn", variant="primary")
                yield Button("Load All Results", id="load_all_search_btn", variant="success")

            with TabPane("📂 Filter", id="category_tab"):
                yield Label("1. Check Genres (Multi-select):")
                categories = self.movie_repo.get_all_categories()
                yield SelectionList(
                    *[Selection(cat, cat, False) for cat in categories], id="genre_sel"
                )

                yield Label(f"2. Select Year Range (From - To):")
                with Horizontal():
                    year_options_start = [
                        Option(str(y)) for y in range(self.min_db, self.max_db + 1)
                    ]
                    yield OptionList(
                        *year_options_start, id="year_start_strip", classes="year-selector"
                    )

                    year_options_end = [
                        Option(str(y)) for y in range(self.max_db, self.min_db - 1, -1)
                    ]
                    yield OptionList(
                        *year_options_end, id="year_end_strip", classes="year-selector"
                    )

                yield Static("Filters: No genres selected", id="active_filters_info")
                yield DataTable(id="cat_movie_table")

                with Horizontal(id="button_row"):
                    yield Button("Load 10 More", id="next_cat_btn", variant="primary")
                    yield Button("Load All Results", id="load_all_btn", variant="success")

            with TabPane("🔥 Top 5", id="stats_tab"):
                yield DataTable(id="stats_table")
            with TabPane("🕒 History", id="history_tab"):
                yield DataTable(id="history_table")
        yield Footer()

    def _fill_table(self, table_id: str, movies: List[Movie], clear: bool = True):
        """Populates the specified DataTable with movie objects."""
        table = self.query_one(table_id, DataTable)
        if clear:
            table.clear()
            self.row_count = 0

        for m in movies:
            self.row_count += 1
            table.add_row(str(self.row_count), m.title.upper(), str(m.release_year), m.rating_text)

    def update_filter_display(self):
        """Refreshes the active filters display panel."""
        genres_text = ", ".join(self.selected_genres) if self.selected_genres else "None"
        low = self.start_y
        high = self.end_y
        info_text = f"ACTIVE FILTERS: [Genres: {genres_text}] | [Years: {low} - {high}]"
        self.query_one("#active_filters_info", Static).update(info_text)

    @on(SelectionList.SelectedChanged, "#genre_sel")
    def on_genre_changed(self, event: SelectionList.SelectedChanged):
        """Handles genre selection updates."""
        self.selected_genres = event.selection_list.selected
        self.category_page = 1
        self.update_filter_display()
        self.perform_category_search(clear=True)

    @on(OptionList.OptionSelected, "#year_start_strip")
    def on_start_year_selected(self, event: OptionList.OptionSelected):
        """Updates start year filter."""
        self.start_y = int(event.option.prompt)
        self.category_page = 1
        self.update_filter_display()
        self.perform_category_search(clear=True)

    @on(OptionList.OptionSelected, "#year_end_strip")
    def on_end_year_selected(self, event: OptionList.OptionSelected):
        """Updates end year filter."""
        self.end_y = int(event.option.prompt)
        self.category_page = 1
        self.update_filter_display()
        self.perform_category_search(clear=True)

    @on(Button.Pressed, "#next_search_btn")
    def handle_next_search_page(self):
        """Loads the next page of search results."""
        self.search_page += 1
        self.perform_keyword_search(clear=False)

    @on(Button.Pressed, "#load_all_search_btn")
    def handle_load_all_search(self):
        """Fetches all results matching the keyword search."""
        if self.last_keyword:
            movies = self.movie_repo.search_all(self.last_keyword)
            self._fill_table("#movie_table", movies, clear=True)
            self.query_one("#next_search_btn").display = False
            self.query_one("#load_all_search_btn").display = False

    @on(Button.Pressed, "#next_cat_btn")
    def handle_next_cat_page(self):
        """Loads the next page of category-filtered results."""
        self.category_page += 1
        self.perform_category_search(clear=False)

    @on(Button.Pressed, "#load_all_btn")
    def handle_load_all(self):
        """Fetches all results matching the active filters."""
        if self.selected_genres:
            real_start = min(self.start_y, self.end_y)
            real_end = max(self.start_y, self.end_y)
            movies, _ = self.movie_repo.find_by_category_and_year(
                self.selected_genres, real_start, real_end, page=1, limit=1000
            )
            self._fill_table("#cat_movie_table", movies, clear=True)
            self.query_one("#next_cat_btn").display = False
            self.query_one("#load_all_btn").display = False

    def perform_category_search(self, clear=True):
        """Executes a search based on selected categories and years."""
        if self.selected_genres:
            real_start = self.start_y
            real_end = self.end_y
            movies, has_more = self.movie_repo.find_by_category_and_year(
                self.selected_genres, real_start, real_end, page=self.category_page
            )
            self._fill_table("#cat_movie_table", movies, clear=clear)
            if clear:
                self.query_one("#load_all_btn").display = True
            self.query_one("#next_cat_btn").display = has_more
            self.refresh_logs()

    @on(Input.Submitted, "#keyword_input")
    def keyword_submit(self, event: Input.Submitted):
        """Processes keyword submission."""
        self.search_page = 1
        self.last_keyword = event.value.strip()
        self.perform_keyword_search()

    def perform_keyword_search(self, clear=True):
        """Executes search based on title keywords."""
        if self.last_keyword:
            movies, has_more = self.movie_repo.search(self.last_keyword, page=self.search_page)
            if not movies and clear:
                self.notify(
                    f"No results found for '{self.last_keyword}'",
                    title="Search Result",
                    severity="warning"
                )
            self._fill_table("#movie_table", movies, clear=clear)
            self.query_one("#next_search_btn").display = has_more
            self.query_one("#load_all_search_btn").display = has_more or not clear
            self.refresh_logs()

    def on_mount(self) -> None:
        """Configures initial UI state on application mount."""
        for tid in ["#movie_table", "#cat_movie_table"]:
            self.query_one(tid, DataTable).add_columns("№", "Title", "Year", "Rating")
        self.query_one("#stats_table", DataTable).add_columns("№", "Query", "Count")
        self.query_one("#history_table", DataTable).add_columns("№", "Time", "Query", "Found")

        self.query_one("#next_search_btn").display = False
        self.query_one("#load_all_search_btn").display = False
        self.query_one("#next_cat_btn").display = False

        self.update_filter_display()
        self.refresh_logs()

    def refresh_logs(self):
        """Updates stats and history tables from LogRepository."""
        st_table = self.query_one("#stats_table", DataTable)
        st_table.clear()
        for i, s in enumerate(self.log_repo.get_top_queries(), start=1):
            st_table.add_row(
                str(i),
                s["query"],
                str(s["count"])  #
            )

        h_table = self.query_one("#history_table", DataTable)
        h_table.clear()
        for i, log in enumerate(self.log_repo.get_history(), start=1):
            h_table.add_row(
                str(i),
                log.get("time", "N/A"),
                log.get("query"),
                str(log.get("results_found"))
            )
