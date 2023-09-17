import dearpygui.dearpygui as dpg
import os
import time

dpg.create_context()

def reset_dir(sender, data):
    path = os.listdir()
    
    if path:
        # Get the file name
        for item in path:
            file_name = os.path.basename(item)
            
            # Get the creation time and format it
            creation_time = os.path.getctime(item)
            creation_time = time.ctime(creation_time)

            # Get the type of the item
            item_type = "Directory" if os.path.isdir(item) else "File"

            # Get the size of the item
            item_size = os.path.getsize(item)

            # Add a row to the table
            with dpg.table_row(parent="file_dialog"):
                dpg.add_selectable(label=file_name)
                dpg.add_selectable(label=creation_time)
                dpg.add_selectable(label=item_type)
                dpg.add_selectable(label=str(item_size))



with dpg.window(label="File dialog", width=800, height=600):
    with dpg.menu_bar():
        with dpg.menu(label="Path"):
            dpg.add_menu_item(label="Add file...")
            dpg.add_menu_item(label="Add folder...")
            dpg.add_separator()
            dpg.add_menu_item(label="Reset current directory", callback=reset_dir)

    with dpg.table(
        tag=f'file_dialog',
        height=-1,
        resizable=True, 
        policy=dpg.mvTable_SizingStretchProp, 
        borders_innerV=True, 
        reorderable=True, 
        hideable=True,
        sortable=True,
        scrollX=True,
        scrollY=True,
        ):
        iwow_name = 100
        iwow_date = 50
        iwow_type = 50
        iwow_size = 50
        dpg.add_table_column(label='Name',     init_width_or_weight=iwow_name)
        dpg.add_table_column(label='Date',     init_width_or_weight=iwow_date)
        dpg.add_table_column(label='Type',     init_width_or_weight=iwow_type)
        dpg.add_table_column(label='Size',     init_width_or_weight=iwow_size)

        

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.maximize_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
