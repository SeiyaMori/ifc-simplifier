# main.py

import ifcopenshell
import numpy as np # linear algebra
#import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

file = ifcopenshell.open("example_building.ifc")

walls = file.by_type("IfcWall")
doors = file.by_type("IfcDoor")
rooms = file.by_type("IfcSpace")
windows = file.by_type("IfcWindow")

msg = "Report:"
msg += "\n\nWalls: " + str(len(walls))
msg += "\nDoors: " + str(len(doors))
msg += "\nRooms: " + str(len(rooms))
msg += "\nWindows: " + str(len(windows))


container = ifcopenshell.util.element.get_container(walls[0])
print(container.Name)

"""
# get a reference to all objects in file that are of type "IfcSpace", effectively getting the list of all rooms in model. 
rooms = file.by_type("IfcSpace")

print("There are {} rooms in this model".format(len(rooms)))

"""
