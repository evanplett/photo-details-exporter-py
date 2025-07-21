from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLineEdit, QLabel, QGroupBox, QHBoxLayout

from .exif_exporting import get_exif_tags_from_file, get_files_in_directory
from .settings import get_read_directory, set_read_directory, get_supported_extensions



# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    selected_directory_text_edit: QLineEdit

    output_file: Path
    output_file_text_edit: QLineEdit

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image EXIF Exporter")

        self.resize(800, 200)

        widget = QWidget(self)
        main_layout = QVBoxLayout(widget)

        self.setCentralWidget(widget)
        widget.setLayout(main_layout)

        # Input
        input_group = QGroupBox("Input")
        input_group_layout = QHBoxLayout(input_group)

        input_group_layout.addWidget(QLabel("Directory: "))

        self.selected_directory_text_edit = QLineEdit(get_read_directory())
        self.selected_directory_text_edit.textChanged.connect(self.__update_selected_read_directory)
        input_group_layout.addWidget(self.selected_directory_text_edit)


        button = QPushButton("Choose Directory", )
        button.clicked.connect(self.__choose_read_directory)
        input_group_layout.addWidget(button)

        main_layout.addWidget(input_group)

        # Options
        options_group = QGroupBox("Options")


        main_layout.addWidget(options_group)

        # Output
        output_group = QGroupBox("Output")
        output_group_layout = QHBoxLayout(output_group)

        output_group_layout.addWidget(QLabel("Output FIle"))

        # Duplicate the input directory logic for the output file

        main_layout.addWidget(output_group)


    def __update_selected_read_directory(self):
        ''' Updates the selected read directory '''
        set_read_directory(self.selected_directory_text_edit.text())
        available_tags = self.__get_available_tags_from_directory()
        # TODO: Use `available_tags` to update the GUI
        print("Here")


    def __choose_read_directory(self):
        ''' Allows the user to choose the directory to read from '''
        chosen_directory = QFileDialog.getExistingDirectory(dir=get_read_directory())
        self.selected_directory_text_edit.setText(chosen_directory)

    def __get_available_tags_from_directory(self):
        ''' Gets the tags available in the files in the chosen directory '''
        files = get_files_in_directory(get_read_directory(), get_supported_extensions())

        tags = set()

        for file in files:
            file_tags = get_exif_tags_from_file(file)
            tags.update(file_tags)

        return list(tags)



def create_gui():

    app = QApplication([])

    window = MainWindow()


    window.show()
    app.exec_()






















# import dearpygui.dearpygui as dpg


# def callback(sender, app_data):
#     print('OK was clicked.')
#     print("Sender: ", sender)
#     print("App Data: ", app_data)

# def cancel_callback(sender, app_data):
#     print('Cancel was clicked.')
#     print("Sender: ", sender)
#     print("App Data: ", app_data)

    # dpg.create_context()
    # dpg.create_viewport(title='Image EXIF Exporter', width=600, height=300)

    # default_dir = Path('.')


    # with dpg.window(tag="Primary Window"):
    #     dpg.add_file_dialog(
    #         directory_selector=True, show=False, callback=callback, tag="file_dialog_id",
    #         cancel_callback=cancel_callback, width=700 ,height=400)



    #     dpg.add_text("Directory: ")
    #     dpg.add_input_text(default_value=default_dir.absolute())

    #     dpg.add_button(label="Choose Directory", callback=lambda: dpg.show_item("file_dialog_id"))









    #     # with dpg.group():
    #     #     dpg.add_button(label="Button 3")
    #     #     dpg.add_text(label="Stuff")


    #     # dpg.add_button(label="Save")
    #     # dpg.add_input_text(label="string", default_value="Quick brown fox")
    #     # dpg.add_slider_float(label="float", default_value=0.273, max_value=1)


    # dpg.setup_dearpygui()
    # dpg.show_viewport()
    # dpg.set_primary_window("Primary Window", True)
    # dpg.start_dearpygui()
    # dpg.destroy_context()
