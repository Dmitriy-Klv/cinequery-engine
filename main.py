import sys
from cli.menu import CineQueryApp
from app.core.database.mysql import db_mysql
from app.core.database.mongo import db_mongo


def main():
    try:
        app = CineQueryApp()
        app.run()
    except Exception as e:
        print(f"\n[❌] A critical error occurred: {e}")
        sys.exit(1)
    finally:
        db_mysql.close()
        db_mongo.close()
        print("[✅] Database connections closed.")


if __name__ == "__main__":
    main()
