# delete.py

# Delete an item from sqlite.db

from db_controller import DBController
from db_path import DB_PATH

ITEM_ID = 1
ITEM_IFC_ID = 999
ITEM_NAME = "Updated name"
ITEM_TYPE = "Updated type"

if __name__ == "__main__":
    controller = DBController(DB_PATH)
    element = (ITEM_IFC_ID, ITEM_NAME, ITEM_TYPE, ITEM_ID)
    controller.update(element)
    print("Finished.")
