# main.py

# Test db functionality

import ifcopenshell
from db_controller import DBController
from db_path import DB_PATH


def main():
    controller = DBController(DB_PATH)

    # Delete all elements in db
    controller.delete_all()
    print("All elements deleted.")

    # Create new elements in db
    file = ifcopenshell.open("example_building.ifc")
    ifc_elements = file.by_type("IfcBuildingElement")
    for e in ifc_elements:
        info = e.get_info()
        controller.create((info["id"], info["Name"], info["type"], False))

if __name__ == "__main__":
    main()
    print("Finished.")
