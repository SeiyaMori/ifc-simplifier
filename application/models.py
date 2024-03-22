# models.py


class Element:
    def __init__(self, ifc_element):
        self.ifc_element = ifc_element
        self.id = self.get_id()
        self.name = self.get_name()
        self.type = self.get_type()
        self.exclude = False
    
    def get_id(self):
        return 1
    
    def get_name(self):
        return "Door 1"

    def get_type(self):
        return ("Door")
    

class IFCImporter:
    @classmethod
    def ifc_to_elements(cls, ifc_file):
        pass
        #return [Element(i) for i in ifc_file]

