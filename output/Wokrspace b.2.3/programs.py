"""
Programs
=====================================

programs.py is the main script where are the Workspace programs like XTerm, Text Editor, Paint and etc.
This script does also contain programs that are used for testing and debugging purposes
"""

import dearpygui.dearpygui as dpg
import dearpygui_extend as dpge

def center_window(modal_id):
    with dpg.mutex():
        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()

    width = dpg.get_item_width(modal_id)
    height = dpg.get_item_height(modal_id)
    dpg.set_item_pos(modal_id, [viewport_width // 2 - width // 2, viewport_height // 2 - height // 2])

def check_internet():
    import requests
    url = 'http://www.google.com/'
    timeout = 5
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print("No internet connection available.")
    return False


def message_box(title, message, selection_callback):
    with dpg.mutex():
        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()
        with dpg.window(label=title, modal=True, no_close=True) as modal_id:
            dpg.add_text(message)
            with dpg.group(horizontal=True):
                dpg.add_button(label="Ok", width=75, user_data=(modal_id, True), callback=selection_callback)
                dpg.add_button(label="Cancel", width=75, user_data=(modal_id, False), callback=selection_callback)
        
    dpg.split_frame()
    width = dpg.get_item_width(modal_id)
    height = dpg.get_item_height(modal_id)
    dpg.set_item_pos(modal_id, [viewport_width // 2 - width // 2, viewport_height // 2 - height // 2])


def terminal():
    import subprocess, os

    _auto_scroll = True
    path = os.getcwd()

    def cout(message, color=(255,255,255)):
        dpg.add_text(message, color=color, parent="output")
        if _auto_scroll:
            dpg.set_y_scroll("output", -1)
 
    def reset_input():
        dpg.set_value("input", "")
        dpg.focus_item("input")

    def chdir(path):
        try:
            os.chdir(path)
        except:
            cout("XTERM:ERROR: No such file or directory", color=(255,0,0))

    def fs():
        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()

        dpg.set_item_height(item="xterm", height=viewport_height-17)
        dpg.set_item_width(item="xterm", width=viewport_width)
        dpg.set_item_pos("xterm", [0,0])

    def nm():
        dpg.set_item_height(item="xterm", height=550)
        dpg.set_item_width(item="xterm", width=900)
        dpg.set_item_pos("xterm", [0,0])
        center_window("xterm")

    def about():
        with dpg.window(label="About", no_resize=True) as xt_about:                                                                                                                                                                                                                                                                                                                                                                                                                                                         
            dpg.add_text("XTerm 1.1 (Alpha)\nXTerm or XTerminal is the terminal from Workspace, basically emulates your os terminal.\n\n\nProblems and Bugs of this version (BETA):\n - Does not support inputs from other programs\n - Colors are not supported from other programs\n - Some OS Terminal commands will not work or it will cause\n   problems on the terminal\n\n\nWhat's new in 1.1?\n - The clear output command is now avaible\n\n\nWorking on:\n - Adding more features\n - Fixing errors when the cd command beings executed\n\n\nNOTE:\nXTerm is in alpha, bugs, issues or unfinished features might appear when using.")
            center_window(xt_about)
    def run_command(command):
        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            cout(f"XTERM:INTERNAL_ERROR: An internal error has occured : v info v :\n{e}", color=(255,0,0))
            return None

    def send_output(sender, data):
        noncom = ["ubuntu"]
        text = dpg.get_value("input")
        if text == "cls" or text == "clear":
            reset_input()
            
            return dpg.delete_item("output", children_only=True)
        elif text.startswith("cd"):
            chdir(text.replace("cd ", ""))
            reset_input()
        elif text.startswith("exit"):
            reset_input()
            dpg.hide_item("xterm")
        elif text.startswith("ubuntu"):
            reset_input()
            return cout(f"XTERM:ERROR: Command not avaible in Xterm : {text}", color=(255,0,0))

        output = run_command(text)
        if output is not None:
            reset_input()
            cout(output)
        else:
            reset_input()
        reset_input()
        path = os.getcwd()
        dpg.set_value("path", path)
    

    with dpg.window(label="XTerminal", height=550, width=900, show=False, tag="xterm"):
        with dpg.menu_bar():
            with dpg.menu(label="XTerm"):
                dpg.add_menu_item(label="About", callback=about)
            with dpg.menu(label="Window"):
                dpg.add_menu_item(label="Fullscreen", callback=fs)
                dpg.add_menu_item(label="Normal size", callback=nm)
                dpg.add_menu_item(label="Scroll up", callback=lambda:dpg.move_item_up("output"))
                dpg.add_menu_item(label="Scroll down", callback=lambda:dpg.move_item_down("output"))
        with dpg.child_window(height=-48, width=-1, horizontal_scrollbar=True, tag="output", tracked=True):
            dpg.add_text("[XTerm BETA Loaded v.23.08]\nOpen 'About' for more information of this version", tag="xt_txt")
        
        dpg.add_text(path, tag="path")
        dpg.add_input_text(tag="input", on_enter=True, callback=send_output, width=-1, hint=("Type a terminal command"))
    
    center_window("xterm")
    
def explorer():
    import os

    def clear_child_window():
        for child in list(dpg.get_item_children("filefolderlist")):
            print("DEL: ", child)
            dpg.delete_item(child)


    def on_button_click(sender, data):
        # Get the label of the button that was clicked
        button_label = dpg.get_item_configuration(sender)["label"]
        # Check if the label corresponds to a file or a folder
        if os.path.isfile(button_label):
            print(f"{button_label} is a file")
        elif os.path.isdir(button_label):
            clear_child_window()
            fflist = os.listdir(button_label)
            for file in fflist:
                dpg.add_button(label=file, width=-1, height=18, parent="listoffilefolder")
        else:
            print(f"{button_label} is not a file or a folder")

    with dpg.window(label="Explorer", height=750, width=1200):
        with dpg.menu_bar():
            with dpg.menu(label="Explorer"):
                dpg.add_menu_item(label="About")
        # Create a horizontal group
        with dpg.group(horizontal=True):
            # Create the first child window within the group
            with dpg.child_window(height=-1, width=250, horizontal_scrollbar=True, tag="filefolderlist"):
                fflist = os.listdir()
                for file in fflist:
                    dpg.add_button(label=file, width=-1, height=18, callback=on_button_click)

            # Create the second child window within the group
            with dpg.child_window(height=-1, width=250, horizontal_scrollbar=True, tag="listoffilefolder"):
                dpg.add_text("View")





def video_capture():
    import cv2 as cv
    import numpy as np
    
    vid = cv.VideoCapture(0)
    ret, frame = vid.read()

    # image size or you can get this from image shape
    frame_width = vid.get(cv.CAP_PROP_FRAME_WIDTH)
    frame_height = vid.get(cv.CAP_PROP_FRAME_HEIGHT)
    video_fps = vid.get(cv.CAP_PROP_FPS)
    print(frame_width)
    print(frame_height)
    print(video_fps)

    data = np.flip(frame, 2)  # because the camera data comes in as BGR and we need RGB
    data = data.ravel()  # flatten camera data to a 1 d stricture
    data = np.asfarray(data, dtype='f')  # change data type to 32bit floats
    texture_data = np.true_divide(data, 255.0)  # normalize image data to prepare for GPU


    with dpg.texture_registry(label="Texture Registry", show=True):
        dpg.add_raw_texture(frame.shape[1], frame.shape[0], texture_data, tag="texture_tag", format=dpg.mvFormat_Float_rgb)

    with dpg.window(label="Example Window"):
        dpg.add_text(F"FPS: {video_fps}", tag="video_fps")
        dpg.add_image("texture_tag")

    while dpg.is_dearpygui_running():

        # updating the texture in a while loop the frame rate will be limited to the camera frame rate.
        # commenting out the "ret, frame = vid.read()" line will show the full speed that operations and updating a texture can run at
        
        ret, frame = vid.read()
        data = np.flip(frame, 2)
        data = data.ravel()
        data = np.asfarray(data, dtype='f')
        texture_data = np.true_divide(data, 255.0)
        dpg.set_value("texture_tag", texture_data)
        dpg.set_value("video_fps", video_fps)

        # to compare to the base example in the open cv tutorials uncomment below
        #cv.imshow('frame', frame)
        dpg.render_dearpygui_frame()

    vid.release()

def video_player():
    import cv2 as cv
    import numpy as np
    video_path = "lcb.mp4"  # Replace with the path to your MP4 video file
    vid = cv.VideoCapture(video_path)

    frame_width = vid.get(cv.CAP_PROP_FRAME_WIDTH)
    frame_height = vid.get(cv.CAP_PROP_FRAME_HEIGHT)
    video_fps = vid.get(cv.CAP_PROP_FPS)

    with dpg.texture_registry(label="Texture Registry", show=True):
        dpg.add_dynamic_texture(width=int(frame_width), height=int(frame_height), default_value=np.zeros((frame_height, frame_width, 3), dtype=np.uint8), tag="video_player")

    with dpg.window(label="Example Window"):
        dpg.add_text(F"FPS: {video_fps}", tag="video_fps")

    while dpg.is_dearpygui_running():
        ret, frame = vid.read()
        if not ret:
            # End of video reached
            break

        data = np.flip(frame, 2)
        data = np.asfarray(data, dtype='f')
        texture_data = np.true_divide(data, 255.0)
        dpg.set_value("video_player", texture_data)
        dpg.set_value("video_fps", video_fps)
        dpg.render_dearpygui_frame()

    vid.release()


def node_editor():
    def new_node():
        with dpg.node(label="Node", parent="node_editor"):
            with dpg.node_attribute(label="Node A1"):
                dpg.add_input_float(label="F1", width=150)

            with dpg.node_attribute(label="Node A2", attribute_type=dpg.mvNode_Attr_Output):
                dpg.add_input_float(label="F2", width=150)
    
    def link_callback(sender, app_data):
        # app_data -> (link_id1, link_id2)
        dpg.add_node_link(app_data[0], app_data[1], parent=sender)

    
    def delink_callback(sender, app_data):
        # app_data -> link_id
        dpg.delete_item(app_data)

    with dpg.window(label="Node Editor", width=400, height=400):
        with dpg.menu_bar():
            with dpg.menu(label="Node"):
                dpg.add_menu_item(label="Add new node", callback=new_node)

        with dpg.node_editor(callback=link_callback, delink_callback=delink_callback, minimap=True, tag="node_editor"):
            with dpg.node(label="Node 1"):
                with dpg.node_attribute(label="Node A1"):
                    dpg.add_input_float(label="F1", width=150)

                with dpg.node_attribute(label="Node A2", attribute_type=dpg.mvNode_Attr_Output):
                    dpg.add_input_float(label="F2", width=150)

            with dpg.node(label="Node 2"):
                with dpg.node_attribute(label="Node A3"):
                    dpg.add_input_float(label="F3", width=200)

                with dpg.node_attribute(label="Node A4", attribute_type=dpg.mvNode_Attr_Output):
                    dpg.add_input_float(label="F4", width=200)

def plots_xy():
    from math import sin

    sindatax = []
    sindatay = []
    for i in range(0, 100):
        sindatax.append(i / 100)
        sindatay.append(0.5 + 0.5 * sin(50 * i / 100))

    with dpg.window(label="Tutorial", width=400, height=600):
        dpg.add_text("Click and drag the middle mouse button over the top plot!")


        def query(sender, app_data, user_data):
            dpg.set_axis_limits("xaxis_tag2", app_data[0], app_data[1])
            dpg.set_axis_limits("yaxis_tag2", app_data[2], app_data[3])


        # plot 1
        with dpg.plot(no_title=True, height=200, callback=query, query=True, no_menus=True, width=-1):
            dpg.add_plot_axis(dpg.mvXAxis, label="x")
            dpg.add_plot_axis(dpg.mvYAxis, label="y")
            dpg.add_line_series(sindatax, sindatay, parent=dpg.last_item())

        # plot 2
        with dpg.plot(no_title=True, height=200, no_menus=True, width=-1):
            dpg.add_plot_axis(dpg.mvXAxis, label="x1", tag="xaxis_tag2")
            dpg.add_plot_axis(dpg.mvYAxis, label="y1", tag="yaxis_tag2")
            dpg.add_line_series(sindatax, sindatay, parent="yaxis_tag2")

def text_editor():
    global file, te
    file = "null"

    def on_key_press(sender, app_data):
        if dpg.is_key_down(dpg.mvKey_Control) and app_data == dpg.mvKey_O:
            open_file()


    def callback(sender, app_data, user_data):
        global file_path
        selections = app_data["selections"]
        for file_name, file_path in selections.items():
            dpg.configure_item("te", label=f"Text Editor - {file_name}")
            pass
        set_text_from_file(file_path, "txt_content")

    def save_file(file_path):
        with open(file_path, "w") as f:
            f.write(dpg.get_value("txt_content"))

    
    with dpg.file_dialog(directory_selector=False, show=False, callback=callback, tag="file_dialog", width=700 ,height=400):
        dpg.add_file_extension(".*")
        dpg.add_file_extension("", color=(150, 255, 150, 255))
        dpg.add_file_extension("Source files (*.cpp *.h *.hpp){.cpp,.h,.hpp}", color=(0, 255, 255, 255))
        dpg.add_file_extension(".h", color=(255, 0, 255, 255), custom_text="[header]")
        dpg.add_file_extension(".py", color=(0, 255, 0, 255), custom_text="[Python]")
        dpg.add_file_extension(".pyl", color=(242,172,185, 255), custom_text="[Pyl]")

    def del_msg_box(sender, unused, user_data):
        if user_data[1]: dpg.delete_item(user_data[0])
        else: dpg.delete_item(user_data[0])

    def set_text_from_file(file_path, text_input_id):
        with open(file_path, "r") as f:
            # Errors that may occur when opening a file:
            #   UnicodeDecodeError: When there are stranges characters inside the file
            #   PermissionError: When the file is a system file or it's not possible to read or make changes to that file
            try:
                file_content = f.read()
            except UnicodeDecodeError:
                message_box("UnicodeDecodeError", "Cannot open file, unsupported file or contains machine code", del_msg_box) 
            except PermissionError:
                message_box("PermissionError", "Cannot open file, permission denied", del_msg_box)
        dpg.set_value(text_input_id, file_content)

    def open_file():
        dpg.configure_item("file_dialog", callback=callback, directory_selector=False)
        dpg.show_item("file_dialog")

    with dpg.handler_registry():
        dpg.add_key_press_handler(callback=on_key_press, tag="new_file_keycombo")

    #main
    with dpg.window(label="Text Editor", tag="te", width=1200, height=700, show=False) as te:
        with dpg.menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="New file", shortcut="CTRL+N")
                #dpg.add_menu_item(label="New folder", shortcut="CTRL+MAIUSC+N")
                #dpg.add_menu_item(label="", enabled=False)
                dpg.add_menu_item(label="Open file", shortcut="CTRL+O", callback=open_file)
                #dpg.add_menu_item(label="Open folder", shortcut="CTRL+O")
                dpg.add_separator()
                dpg.add_menu_item(label="Save", shortcut="CTRL+S", callback=lambda:save_file(file_path))
                dpg.add_menu_item(label="Save as...", shortcut="CTRL+MAIUSC+S")
            with dpg.menu(label="Help"):
                dpg.add_menu_item(label="About")
                dpg.add_menu_item(label="Introduction")
                dpg.add_menu_item(label="Documentation")
                dpg.add_menu_item(label="Bug report")

        #main text
        dpg.add_input_text(multiline=True, height=-1, width=-1, id="txt_content", tab_input=True)

def web_browser():
    import webbrowser

    def _hyperlink(text, address):
        b = dpg.add_button(label=text, callback=lambda:webbrowser.open(address))
        dpg.bind_item_theme(b, "__demo_hyperlinkTheme")

    with dpg.window(label="Web Browser", width=500, height=350):
        _hyperlink("click me :)", "e621.net")

def paint():
    def render(_, app_data):
        x,y = dpg.get_mouse_pos()
        while dpg.is_mouse_button_down(button=dpg.mvMouseButton_Left):
            new_x,new_y = dpg.get_mouse_pos()
            if new_x != x or new_y != y:
                dpg.draw_line((x,y), (new_x,new_y), parent=app_data[1], color=dpg.get_value("brush_color"), thickness=dpg.get_value("brush_thickness"))
                x,y = new_x,new_y

    def change_theme():
        global clear_color
        with dpg.theme() as clear_color:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, dpg.get_value("clear_color"), category=dpg.mvThemeCat_Core)
                
                

    def render_bg():
        change_theme()
        dpg.bind_item_theme("canvas", clear_color)
    

    with dpg.window(label="Paint", width=1200, height=700, tag="paint", show=False, on_close=lambda:dpg.hide_item("paint")):
        with dpg.child_window(width=-1, height=-1, tag="canvas"):
            change_theme()
            render_bg()
            dpg.bind_item_theme("canvas", clear_color)
            drawlist = dpg.add_drawlist(width=2000, height=2000)
            with dpg.item_handler_registry() as registry:
                dpg.add_item_clicked_handler(button=dpg.mvMouseButton_Left, callback=render)
            dpg.bind_item_handler_registry(drawlist, registry)
    with dpg.window(label="Brush Tools", show=False, tag="paint_bt", no_scrollbar=True):
        with dpg.group(horizontal=True):
            dpg.add_color_picker(default_value=[0,0,0], label="Color", tag="brush_color", height=300, width=300, picker_mode=dpg.mvColorPicker_wheel)
            dpg.add_color_picker(default_value=[255,255,255], label="Background color", tag="clear_color", height=300, width=300, callback=render_bg,  picker_mode=dpg.mvColorPicker_wheel)
        dpg.add_button(label="clear canvas", callback=lambda:dpg.delete_item(drawlist, children_only=True))
        dpg.add_combo(["circle", "triangle", "arrow", "text", "line", "polygon", "polyline", "elipse"], default_value="circle")
        dpg.add_slider_float(label="Thickness", default_value=1, tag="brush_thickness", min_value=1, max_value=10)
        dpg.add_slider_float(label="Radius", default_value=1.735, tag="radius", min_value=1, max_value=50)

    center_window("paint")
    
def empty_window():
    with dpg.window(label="Empty window"):
        pass

def image_viewer():

    def open_img(sender, app_data):
        print(app_data)

    def open_file(sender, app_data):
        print(app_data)
    with dpg.file_dialog(directory_selector=False, show=False, callback=open_img, tag="file_dialog", width=700 ,height=400):
        dpg.add_file_extension(".*")
        dpg.add_file_extension("", color=(150, 255, 150, 255))
        dpg.add_file_extension(".png", color=(242,172,185, 255), custom_text="[PNG]")
        dpg.add_file_extension(".bmp", color=(242,172,185, 255), custom_text="[JPEG]")
        dpg.add_file_extension(".psd", color=(242,172,185, 255), custom_text="[PSD]")
        dpg.add_file_extension(".gif", color=(242,172,185, 255), custom_text="[GIF]")
        dpg.add_file_extension(".hdr", color=(242,172,185, 255), custom_text="[HDR]")
        dpg.add_file_extension(".pic", color=(242,172,185, 255), custom_text="[PIC]")
        dpg.add_file_extension(".ppm", color=(242,172,185, 255), custom_text="[PPM]")
        dpg.add_file_extension(".pgm", color=(242,172,185, 255), custom_text="[PGM]")
    width, height, channels, data = dpg.load_image("image.png")

    with dpg.texture_registry(show=True):
        dpg.add_static_texture(width=width, height=height, default_value=data, tag="iw_image")

    
    with dpg.window(label="Image Viewer", width=width, height=height+50, tag="image_viewer"):
        with dpg.menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Open image", callback=open_file)

        dpg.add_image("iw_image", tag="rendered_img")

def spectrum():
    import random

    with dpg.window(label="Spectrum like", width=500, height=500):
        with dpg.stage():
            dpg.add_2d_histogram_series([0,0], [0,0])



def system_information():
    with dpg.window(label="System Information", height=750, width=1200, show=False, tag="sys_info", on_close=lambda:(dpg.hide_item("sys_info"), dpg.hide_item("cpu"), dpg.hide_item("disk"))):
        with dpg.group(horizontal=True):
            with dpg.child_window(height=-1, width=250, horizontal_scrollbar=True, tag="main"):
                dpg.add_button(label="Theme", width=-1, height=18, callback=lambda:(dpg.show_item("cpu"), dpg.hide_item("disk")))
                dpg.add_button(label="Viewport", width=-1, height=18, callback=lambda:(dpg.show_item("disk"), dpg.hide_item("cpu")))

            # Theme menu
            with dpg.child_window(height=-1, width=-1, horizontal_scrollbar=True, tag="cpu", show=False):
                dpg.add_text("Theme\nYou can customize many things like the theme and the default font\n\n")

            
            # Viewport menu
            with dpg.child_window(height=-1, width=-1, horizontal_scrollbar=True, tag="disk", show=False):
                dpg.add_text("Viewport\nSettings about the viewport and the window itself\n\n")

def vertex_engine():
    import json, ursina
    """
    This is not a game engine made from zero, it uses node editor and ursina
    engine to run, altough this is a prototype of the engine.
    """
    search_enabled = False
    connections = {}

    class nodes:
        class events:
            def new_collision_event_node():
                with dpg.node(label="Event Node", parent="ve_node_editor"):
                    with dpg.node_attribute(label="Node A1", attribute_type=dpg.mvNode_Attr_Input):
                        dpg.add_text("Entity")

                    with dpg.node_attribute(label="Node", attribute_type=dpg.mvNode_Attr_Output):
                        dpg.add_text("output")

            def new_entity_event_node():
                with dpg.node(label="Event Node", parent="ve_node_editor"):
                    with dpg.node_attribute(label="Node A1", attribute_type=dpg.mvNode_Attr_Input):
                        dpg.add_combo(items=["cube", "triangle", "sphere"], label="Entity", width=300)
                        dpg.add_color_picker(default_value=[255,255,255], width=300, height=300, label="Color")
                        

                    with dpg.node_attribute(label="Node A2", attribute_type=dpg.mvNode_Attr_Output):
                        dpg.add_text("output")
        class basic:
            def new_note():
                with dpg.node(label="Note", parent="ve_node_editor"):
                    with dpg.node_attribute(label="Node A1", attribute_type=dpg.mvNode_Attr_Static):
                        dpg.add_input_text(multiline=True, height=300, width=300, tab_input=True)



    def save_node_editor(filename, node_editor_id): 
        nodes = dpg.get_item_children(node_editor_id)
        data = {}
        for node_id in nodes:
            node_info = dpg.get_item_configuration(node_id)
            attributes = dpg.get_item_children(node_id)
            attribute_info = [dpg.get_item_configuration(a) for a in attributes]
            node_info["attributes"] = attribute_info
            data[node_id] = node_info
        with open(filename, 'w') as f:
            json.dump(data, f)
    

    
    # Callback for when a link is created
    def link_callback(sender, app_data):
        # app_data -> (link_id1, link_id2)
        dpg.add_node_link(app_data[0], app_data[1], parent=sender)

    def delink_callback(sender, app_data):
        # app_data -> link_id
        dpg.delete_item(app_data)

    def nodes_connected(node1_id, node2_id):
        if node1_id in connections and node2_id in connections[node1_id]:
            return True
        else:
            return False


    with dpg.window(label="Node Editor", width=400, tag="ve_main_ne", show=False, height=400):
        with dpg.menu_bar():
            with dpg.menu(label="Node"):
                dpg.add_menu_item(label="Save node editor", callback=lambda:save_node_editor("node.json", "ve_node_editor"))
                with dpg.menu(label="Nodes"):
                    dpg.add_menu_item(label="Add new collision event", callback=nodes.events.new_collision_event_node)
                    dpg.add_menu_item(label="Add new entity", callback=nodes.events.new_entity_event_node)
                    dpg.add_menu_item(label="Add new note", callback=nodes.basic.new_note)
            
        with dpg.group(horizontal=True):
            with dpg.node_editor(callback=link_callback, delink_callback=delink_callback, minimap=True, tag="ve_node_editor", menubar=True):
                with dpg.node(label="Main"):
                    with dpg.node_attribute(label="Game settings", attribute_type=dpg.mvNode_Attr_Static):
                        dpg.add_input_int(label="FPS", width=150)
                        dpg.add_radio_button(["Fullscreen on start", "test", "another test"], label="Window options")

                    with dpg.node_attribute(label="Node", attribute_type=dpg.mvNode_Attr_Output):
                        dpg.add_text("output")


    with dpg.window(label="Vertex Engine", height=750, width=1200, on_close=lambda:(dpg.hide_item("vertex_engine")), show=False, tag="vertex_engine"):
        with dpg.menu_bar():
            with dpg.menu(label="Vertex Engine"):
                dpg.add_menu_item(label="About")
            with dpg.menu(label="Project"):
                dpg.add_menu_item(label="Save", shortcut="CTRL+S")
                dpg.add_menu_item(label="Open node editor", callback=lambda:dpg.show_item("ve_main_ne"))

    

    
            
        
        with dpg.group(horizontal=True):
            with dpg.child_window(height=-1, width=-1):
                pass


def pdf_viewer():
    import PyPDF2

    def start_file(sender, app_data):
        global file_path
        selections = app_data["selections"]
        for file_name, file_path in selections.items():
            dpg.configure_item("pdf_viewer", label=f"PDF Viewer - {file_name}")
            pass
        reader = PyPDF2.PdfReader(file_path)
        text = reader.pages[0].extract_text()
        
        for line in text.split('\n'):
            if line.startswith("•") or line.startswith("o") or line.startswith("?"):
                dpg.add_text(line[2:], bullet=True, parent="pdf_render")
            else:
                dpg.add_text(line, parent="pdf_render")


    with dpg.window(label="PDF Viewer - None", height=750, width=1200, show=False, tag="pdf_viewer", on_close=lambda:(dpg.hide_item("pdf_viewer"))):
        with dpg.menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Open a PDF file", callback=lambda:(dpg.configure_item("file_dialog", callback=start_file), dpg.show_item("file_dialog")))

        with dpg.child_window(width=-1, height=-1, tag="pdf_render"):
            dpg.add_text("open a PDF file")

def ppack_packer():
    import ppack.ppack as ppack
    import json

    files = []

    def start_dir(sender, app_data):
        global file_path, file_name
        selections = app_data["selections"]
        for file_name, file_path in selections.items():
            print("working")
            dpg.configure_item("ppack_pack", label="working")
            print(f'{dpg.get_value("ppack_filename")}\t:\t{dpg.get_value("ppack_files")}\t:\t{file_path}')
            ppack.make_pack(dpg.get_value("ppack_filename"), json.loads(dpg.get_value("ppack_files")))
            print(dpg.get_value("ppack_filename"))
            
    def start_pack(sender, files, cancel_pressed):
        if not cancel_pressed:
            ppack.make_pack(dpg.get_value("ppack_filename"), files)
            


    with dpg.window(label="ppack packer", height=750, width=1200, show=False, tag="ppack_pack", on_close=lambda:(dpg.hide_item("ppack_pack"))):

        dpg.add_text("Create a ppack package, any file formats are supported, no limit on selecting files")
        dpg.add_input_text(label="File name", hint='E.g: source_1', tag="ppack_filename")
        dpge.add_file_browser(
            width=800,
            height=600,
            show_as_window=True, 
            show_ok_cancel=True, 
            allow_multi_selection=True, 
            collapse_sequences=True,
            callback=start_pack,
            allow_drag=True)


def pcall_editor():

    def file_to_hex_list(file_path):
        hex_list = []
        with open(file_path, 'r') as file:
            while True:
                char = file.read(1)
                if not char:
                    break
                hex_list.append(hex(ord(char))[2:])
        return hex_list
    
    def add(char):
        dpg.add_text(char, parent="pcall_output")

    def remove():
        #files.pop()
        last_input = dpg.get_item_children('ppack_file_list',1)[-1]
        dpg.delete_item(last_input)

    def start_dir(sender, app_data):
        global file_path, file_name
        selections = app_data["selections"]
        for file_name, file_path in selections.items():
            hexl = file_to_hex_list(file_path)
        for event in hexl:
            add(event)



        
    def new_fd():
        dpg.configure_item("file_dialog", callback=start_dir, directory_selector=False)
        dpg.show_item("file_dialog")
            


    with dpg.window(label="pcall editor", height=750, width=1200, show=False, tag="pcall_editor", on_close=lambda:(dpg.hide_item("pcall_editor"))):
        with dpg.menu_bar():
            with dpg.menu(label="Script"):
                dpg.add_menu_item(label="Open script", callback=new_fd)
                dpg.add_menu_item(label="Save script")



        with dpg.group(horizontal=True, tag="pcall_output"):
            pass
            

def mail_box():
    from Google import create_service
    import base64
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.utils import parseaddr
    import threading, os

    CLIENT_SECRET_FILE = "workspace/AppData/EmailSender/client_secret_1042249688389-rm2iabq65p414ua3e8nupjvefk50napk.apps.googleusercontent.com.json"
    API_NAME = "gmail"
    API_VERSION = "v1"
    SCOPES = ['https://mail.google.com/']


    if check_internet():
        dpg.set_viewport_decorated(True)
        dpg.set_viewport_always_top(False)
        if create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES):
            print("SERVICE CREATED")
            service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
            dpg.set_viewport_decorated(False)
            dpg.set_viewport_always_top(True)
        else:
            print("ERROR ON SERVICE, HALTING")
            dpg.stop_dearpygui()
            os.startfile("ga_error1.vbs")
            dpg.set_viewport_decorated(False)
            dpg.set_viewport_always_top(True)
    else:
        dpg.set_viewport_decorated(False)
        dpg.set_viewport_always_top(True)



    def send_email(to_email, email_subject, email_msg):
        global emailMsg, mimeMessage
        emailMsg = email_msg
        mimeMessage = MIMEMultipart()
        mimeMessage['to'] = to_email
        mimeMessage['subject'] = email_subject
        mimeMessage.attach(MIMEText(emailMsg, "plain"))
        raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

        message = service.users().messages().send(userId="me", body={"raw": raw_string}).execute()
        print(message)

    def get_username_from_email(email_address):
        real_name, email = parseaddr(email_address)
        username = email.split('@')[0]
        return username


    def select(sender, _, user_data):
        if user_data[1]:
            dpg.delete_item(user_data[0])
            send_email(dpg.get_value("email_recipient"), dpg.get_value("email_subject"), dpg.get_value("email_message"))
        else:
            dpg.delete_item(user_data[0])

    def warn():
        message_box("Warning - Email sender", f"Before you send the email we want to let you know\nthat you information are completely safe\nand Workspace will not share them anywhere.\nPress Ok to continue or Cancel to stop sending the email", select)
        
    def display_email(sender, subject, snippet):
        with dpg.window(label="Email Details", width=1100, height=400) as w:
            with dpg.child_window(horizontal_scrollbar=True):
                dpg.add_text(f"From: {sender}\n\n")
                dpg.add_text(f"{subject}")
                dpg.add_separator()
                dpg.add_text(snippet)
        center_window(w)
                

    def create_callback(from_name, subject, snippet):
        def callback():
            display_email(from_name, subject, snippet)
        return callback

    def list_emails():
        if check_internet():
            try:
                results = service.users().messages().list(userId='me').execute()
                messages = results.get('messages', [])
                
                if not messages:
                    dpg.add_text("No new messages")
                else:
                    for message in messages:
                        msg = service.users().messages().get(userId='me', id=message['id']).execute()
                        email_data = msg['payload']['headers']
                        from_name = subject = ""  # Initialize variables
                        for values in email_data:
                            name = values['name']
                            if name == 'From':
                                from_name = values['value']
                            if name == 'Subject':
                                subject = values['value']
                        snippet = msg['snippet']
                        button_label = f"{get_username_from_email(from_name)}\t\t\t\t\t\t{snippet[:48]}..."  # Adjust the number of words as needed
                        dpg.add_menu_item(label=button_label, parent="mb_emails", callback=create_callback(from_name, subject, snippet))
                        dpg.add_separator(parent="mb_emails")
            except Exception:
                print("ERROR ON SERVICE, HALTING")
                dpg.stop_dearpygui()
                os.startfile("ga_error1.vbs")
        else:
            print("no internet")
            


    thread = threading.Thread(target=list_emails, args=(), daemon=True)

    with dpg.window(label="MailBox", width=1200, height=800, show=False, tag="mail_box", on_close=lambda:(dpg.hide_item("mail_box"))):
        with dpg.menu_bar():
            with dpg.menu(label="Emails"):
                dpg.add_menu_item(label="Refresh", callback=lambda:(dpg.delete_item("mb_emails", children_only=True), list_emails()))
        with dpg.group(horizontal=True):
            with dpg.child_window(height=-1, width=250):
                dpg.add_button(label="Send email", width=-1, height=18, callback=lambda:(dpg.show_item("mb_send_email"), dpg.hide_item("mb_main_emails")))
                dpg.add_button(label="New emails", width=-1, height=18, callback=lambda:(dpg.show_item("mb_main_emails"), dpg.hide_item("mb_send_email")))

            # Send Email window
            with dpg.child_window(width=-1, height=-1, show=False, tag="mb_send_email"):
                dpg.add_input_text(width=-1, hint="Recipient email", tag="email_recipient")
                dpg.add_input_text(width=-1, hint="Subject of the email", tag="email_subject")
                dpg.add_input_text(width=-1, height=250, tab_input=True, multiline=True, hint="Message", tag="email_message")
                dpg.add_button(label="Send Email", callback=warn)
            
            # Read email window
            with dpg.child_window(width=-1, height=-1, show=False, tag="mb_main_emails"):
                dpg.add_input_text(hint="Search emails", tag="mb_search_emails")
                with dpg.child_window(width=-1, height=-1, tag="mb_emails"):
                    thread.start() # this makes the workspace start up more faster

    center_window("mail_box")