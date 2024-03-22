# ifc_entity_finder.py
import ifcopenshell

class IFCEntityFinder:
    def find_entities(self, ifc_file_path):
        # Use ifcopenshell to find entities and their properties in the IFC file
        # Example:
        entities = []
        ifc_file = ifcopenshell.open(ifc_file_path)
        for entity in ifc_file.by_type("IfcProduct"):
            # Extract properties or other information
            entity_info = {"id": entity.id(), "name": entity.Name}
            entities.append(entity_info)
        return entities
