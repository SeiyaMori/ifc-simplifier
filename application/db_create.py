# create.py

from db_controller import DBController
from db_path import DB_PATH


ITEM_IFC_ID = 111
ITEM_NAME = "New name"
ITEM_TYPE = "New type"

if __name__ == "__main__":
    controller = DBController(DB_PATH)
    element = (ITEM_IFC_ID, ITEM_NAME, ITEM_TYPE)
    element_id = controller.create(element)
    print(f"Finished. New element id: {element_id}")
