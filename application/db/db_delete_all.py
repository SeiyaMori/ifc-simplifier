# delete.py

# Delete an item from sqlite.db

from application.db_controller import DBController
from db_path import DB_PATH

if __name__ == "__main__":
    controller = DBController(DB_PATH)
    controller.delete_all()
    print("Finished.")
