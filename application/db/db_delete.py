# delete.py

# Delete an item from sqlite.db

from db_controller import DBController
from db_path import DB_PATH

ITEM_ID = 1

if __name__ == "__main__":
    controller = DBController(DB_PATH)
    controller.delete(ITEM_ID)
    print("Finished.")
