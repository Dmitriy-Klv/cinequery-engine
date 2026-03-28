import sys

from cli.menu import CineQueryApp


def main():
    """Initializes and runs the CineQuery TUI application."""
    try:
        app = CineQueryApp()
        app.run()
    except Exception as e:
        print(f"\n[❌] A critical error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
