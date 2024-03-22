# main_viewer.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from ifc_viewer_3d import IFCViewer3D
from geometry_extractor import GeometryExtractor
from ifc_entity_finder import IFCEntityFinder

class MainViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IFC Viewer")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.viewer_3d = IFCViewer3D()
        print(self.viewer_3d)
        layout.addWidget(self.viewer_3d)

        self.extractor = GeometryExtractor()
        self.entity_finder = IFCEntityFinder()

        self.btn_open_ifc = QPushButton("Open IFC")
        self.btn_open_ifc.clicked.connect(self.open_ifc_file)
        layout.addWidget(self.btn_open_ifc)

    def open_ifc_file(self):
        # Implement file dialog to open an IFC file
        ifc_file_path = "example_building.ifc"  # Replace with actual file path
        geometries = self.extractor.extract_geometries(ifc_file_path)
        entities = self.entity_finder.find_entities(ifc_file_path)

        #self.viewer_3d.load_geometries(geometries)
        # Display entities or properties in another widget or console output

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = MainViewer()
    viewer.show()
    sys.exit(app.exec_())
