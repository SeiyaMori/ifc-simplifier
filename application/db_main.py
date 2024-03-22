# main.py

# Test db functionality

from application.db_controller import DBController
from db_path import DB_PATH

def main():
    controller = DBController(DB_PATH)
    #new_project = ('New cool App with SQLite & Python', '2015-01-01', '2015-01-30');
    #project_id = controller.create(new_project)
    #update_project = ('Updated', '2024-03-22', '2024-04-01', 4)
    #controller.update(update_project)
    #controller.delete(1)
    #controller.delete_all()

if __name__ == "__main__":
    main()
    print("Finished.")
