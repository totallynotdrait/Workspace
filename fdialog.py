import dearpygui.dearpygui as dpg
import os
import time

dpg.create_context()

def reset_dir(sender, data):
    path = os.path.curdir
    list_dir = os.listdir(path)

    # Clear the table before adding new rows
    dpg.delete_item("file_table", children_only=True)

    for item in list_dir:
        # Get the full path of the item
        full_path = os.path.join(path, item)

        # Get the creation time and format it
        creation_time = os.path.getctime(full_path)
        creation_time = time.ctime(creation_time)

        # Get the type of the item
        item_type = "Directory" if os.path.isdir(full_path) else "File"

        # Get the size of the item
        item_size = os.path.getsize(full_path)

        # Add a row to the table
        with dpg.table_row(parent="file_table"):
            dpg.add_text(item)
            dpg.add_text(creation_time)
            dpg.add_text(item_type)
            dpg.add_text(str(item_size))


with dpg.window(label="Tutorial"):
    with dpg.menu_bar():
        with dpg.menu(label="Path"):
            dpg.add_menu_item(label="Add file...")
            dpg.add_menu_item(label="Add folder...")
            dpg.add_separator()
            dpg.add_menu_item(label="Reset current directory", callback=reset_dir)

    with dpg.table(header_row=True, borders_innerV=True, resizable=True, policy=dpg.mvTable_SizingFixedFit, no_pad_innerX=True, tag="file_table"):
        dpg.add_table_column(label="Name", tag="fd_name")
        dpg.add_table_column(label="Date", tag="fd_date")
        dpg.add_table_column(label="Type", tag="fd_type")
        dpg.add_table_column(label="Size", tag="fd_size")

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
