#------------------= Workspace Python Version =------------------#
#
# This is a little project, it's like workspace in C#, but it's Python

#TODO: Make the PDF viewer more better
#TODO: Implement pcall

#NOTE: Workspace will change startup language (Python to pcall)
#      for better and small instructions files

#NOTE: Possibly in version b.3.0, Workspace will change File Dialog
#      to DearPyGui_Extend File browser (package fileseq is required)
#NOTE: Possibly in version b.3.0, Workspace will add animation
#      using DearPyGui_Animation
#hello
print("[STARTING]")

#------------------= Modules =------------------#

import platform
version = "b.2.3"

import os
try:
    import dearpygui.dearpygui as dpg
    import PyPDF2
    import dearpygui_ext.themes
    import dearpygui_ext.logger
    import fileseq
    import psutil
    import requests
    import dearpygui_extend
    import ursina
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
except ModuleNotFoundError:
    if platform.system() == "Windows":
        print("running on windows")
        print("WARNING: Required modules not found, installing")
        os.system("pip3 install dearpygui")
        os.system("pip3 install PyPDF2")
        os.system("pip3 install psutil")
        os.system("pip3 install requests")
        os.system("pip3 install dearpygui_ext")
        os.system("pip3 install pywin32")
        os.system("pip3 install fileseq")
        os.system("pip3 install ursina")
        os.system("pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib")
        os.system("pip3 install dearpygui-extend")
        print("INFO: Finished, starting Workspace BETA")
    elif platform.system() == "Linux":
        print("running on Linux")
        print("WARNING: Required modules not found, installing")
        os.system("pip3 install dearpygui")
        os.system("pip3 install PyPDF2")
        os.system("pip3 install ursina")
        os.system("pip3 install requests")
        os.system("pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib")
        os.system("pip3 install psutil")
        os.system("pip3 install dearpygui_ext")
        os.system("pip3 install pywin32")
        os.system("pip3 install fileseq")
        os.system("pip3 install dearpygui-extend")
        os.system("sudo apt install libgl1-mesa-glx")
        print("INFO: Finished, starting Workspace BETA")

import dearpygui.dearpygui as dpg
import dearpygui_extend as dpge
import dearpygui_ext.themes
import dearpygui_ext.logger
import dpga.dearpygui_animate as dpga
import ppack.ppack as ppack
import datetime, programs, widgets, sys, psutil, threading, requests
from datetime import datetime
from configparser import ConfigParser
import ppack

if platform.system() == "Linux" or platform.system() == "Darwin":
    print("ERROR: Cannot use ctypes, tools, and windoweffect because system is not Windows")
else:
    import tools
    from windoweffect import window_effect
    import ctypes


#------------------= Function Calls =------------------#


#------------------= Vars =------------------#

search_enabled = False

config = ConfigParser()
config.read("config.ini")

is_load = False

background_color_str = config.get("theme", "background_color")
resizable_str = config.get("window", "resizable")
ontop_str = config.get("window", "on_top")
docking_str = config.get("workspace", "dock")
theme_str = config.get("theme", "default_theme")
font_str = config.get("theme", "font")


if platform.system() == "Linux" or platform.system() == "Darwin":
    print("ERROR: Cannot create MARGINS because system is not Windows")
else:
    class MARGINS(ctypes.Structure):
        _fields_ = [
            ("cxLeftWidth", ctypes.c_int),
            ("cxRightWidth", ctypes.c_int),
            ("cyTopHeight", ctypes.c_int),
            ("cyBottomHeight", ctypes.c_int)
        ]



#------------------= Config =--- ---------------#
BACKGROUND_COLOUR = list(background_color_str)
#------------------= Functions =------------------#

class ws_effects:
    def setAeroEffect():
        window_effect.setAeroEffect(tools.get_hwnd())

    def setMicaEffect():
        window_effect.setMicaEffect(tools.get_hwnd(), isDarkMode=True)

    def restoreBackground():
        margins = MARGINS(0, 0, 0, 0)
        ctypes.windll.dwmapi.DwmExtendFrameIntoClientArea(tools.get_hwnd(), margins)


def reset():
    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

def bytes_to_gb(bytes):
    return bytes / 1024**3

def get_vp_w():
    with dpg.mutex():
        viewport_width = dpg.get_viewport_client_width()
    return viewport_width


def center_window(modal_id):
    with dpg.mutex():
        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()


    width = dpg.get_item_width(modal_id)
    height = dpg.get_item_height(modal_id)
    dpg.set_item_pos(modal_id, [viewport_width // 2 - width // 2, viewport_height // 2 - height // 2])

def check_internet():
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

def ws_quit(sender, unused, user_data):
    if user_data[1]:
        dpg.stop_dearpygui()
    else:
        dpg.delete_item(user_data[0])

def on_close_key(sender, app_data):
    if dpg.is_key_down(dpg.mvKey_Alt) and app_data == dpg.mvKey_F4:
        print("called shut workspace")
        message_box("Workspace", "Are you sure you want to quit Workspace?", ws_quit)

def open_xterm_key(sender, app_data):
    if dpg.is_key_down(dpg.mvKey_Alt) and app_data == dpg.mvKey_F1:
        dpg.show_item("xterm")

#################################################################################################################
############################################## WORKSPACE FUNCTIONS ##############################################
#################################################################################################################

def load_programs():
    programs.terminal()
    programs.text_editor()
    built_in_programs.control_panel()
    programs.vertex_engine()
    programs.paint()
    programs.pcall_editor()
    programs.pdf_viewer()
    programs.ppack_packer()
    programs.mail_box()
    built_in_programs.rotating_cube()

def load_ini():
    if theme_str == "modern":
        log.log("modern theme detected")
        log.log("setting aero effect")
        ws_effects.setAeroEffect()
        dpg.bind_item_theme("ws_mb_time", ws_button)
        log.log_warning("WARNING: Aero Effect is enabled but the effect may not work for many reasons like:\n - The viewport transparency is not set to 0\n - Transperency is not enabled on windows\n - Dock is enabled\n - The version of windows is not supported for the Aero Effect\n - probably many others")
    else: log.log("modern theme not detected, contuine")
        
def setup_dpg():
    log.log_info("setting up DPG")
    dpg.setup_dearpygui()
    log.log_info("setting up viewport")
    dpg.show_viewport() 
    dpg.maximize_viewport()
    dpg.set_viewport_always_top(True)
    dpg.set_viewport_resizable(True)
    dpg.set_viewport_decorated(False)

def import_themes():
    global modern_theme
    with dpg.theme() as modern_theme:
        rounding = 3
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, rounding, category=dpg.mvThemeCat_Core)

            dpg.add_theme_style(dpg.mvStyleVar_PopupBorderSize, 0, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0, category=dpg.mvThemeCat_Core)

            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, rounding, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, rounding, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, rounding, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 0, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_TabRounding, rounding, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_WindowTitleAlign, x=.50, y=.50, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (0,0,0,50), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (0,0,0,50), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, (0,0,0,50), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (0,0,0, 100), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (0,0,0, 120), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (0,0,0, 170), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0, category=dpg.mvThemeCat_Core)
def load_font():
    global modern_theme
    if font_str == "arial":
        dpg.bind_font(arial_font)
    elif font_str == "consola":
        dpg.bind_font(consola_font)
    elif font_str == "proggyclean":
        pass
    else:
        log.log_error("WORKSPACE:ERROR:THEME: Theme not found, the theme will be deafult")

def load_dock():
    if docking_str == "True":
        dpg.configure_app(docking=True, docking_space=True)
    else: pass

def load_theme():
    global modern_theme
    if theme_str == "default":
        pass
    elif theme_str == "modern":
        dpg.bind_theme(modern_theme)
        if platform.system() == "Windows":
            ws_effects.setAeroEffect()
        else:
            print("ERROR: Platform is not Windows, cannot apply Aero effect")
    elif theme_str == "light":
        dpg.bind_theme(dearpygui_ext.themes.create_theme_imgui_light())
    elif theme_str == "dark":
        dpg.bind_theme(dearpygui_ext.themes.create_theme_imgui_dark())
    else:
        log.log_error("WORKSPACE:ERROR:THEME: Theme not found, the theme will be deafult")


def load_handlers():
    with dpg.handler_registry():
        dpg.add_key_press_handler(callback=on_close_key, tag="new_close_keycombo")
        dpg.add_key_press_handler(callback=open_xterm_key, tag="xterm_keycombo")


def import_fonts():
    global arial_font, consola_font
    with dpg.font_registry():
        arial_font = dpg.add_font("workspace/fonts/arial.ttf", 13)
        consola_font = dpg.add_font("workspace/fonts/consola.ttf", 13)


def render_loop():
    while dpg.is_dearpygui_running():
        """
        Quick note:
        This are checks if program manager or the menu bar are opened,
        else it whill stop the process, this is to avoid any script erros
        since this is a render loop. This check will change in the future
        in the ini configuration file.
        """
        if platform.system() == "Linux" or platform.system() == "Darwin":
            disk = psutil.disk_usage(os.path.expanduser("~"))
        else:
            disk = psutil.disk_usage("C:")
        dpga.run()


        # Program Manager
        if dpg.does_item_exist("program_manager"):
            now = datetime.now()
            ttime = now.strftime("%H:%M:%S")
            date = now.strftime("%d/%m/%Y")
            dpg.set_value("pm_time", ttime)
            dpg.set_value("pm_disk_total", f"Total: {bytes_to_gb(disk.total):.2f} GB")
            dpg.set_value("pm_disk_usage", f"Used: {bytes_to_gb(disk.used):.2f} GB")
            dpg.set_value("pm_disk_free", f"Free: {bytes_to_gb(disk.free):.2f} GB")
            dpg.set_value("pm_date", date)
        else: 
            dpg.set_viewport_always_top(False)
            dpg.stop_dearpygui()
            os.startfile("pm_error1.vbs")
        
        if dpg.does_item_exist("ws_menubar"):
            now = datetime.now()
            ttime = now.strftime("%H:%M:%S")
            dpg.configure_item("ws_mb_time", label=ttime)
            dpg.set_item_pos("ws_mb_time", [get_vp_w()-70, 0])
        else:
            dpg.set_viewport_always_top(False)
            dpg.stop_dearpygui()
            os.startfile("ws_warn1.vbs")

        # Weather Widget
        #if dpg.does_item_exist("wid_weather"):
            #city_name = g.city
            #data = get_weather_data(api_key, city_name)
            #current_temp = f"{data.get('main', {}).get('temp')}°C : Current temperature"
            #max_temp = f"{data.get('main', {}).get('temp_max')}°C : Maximum temperature"
            #min_temp = f"{data.get('main', {}).get('temp_min')}°C : Minimum temperature\n"
            #sky_stat = f"{data.get('weather', [{}])[0].get('description', 'N/A')} : Sky status"
            #dpg.set_value("current_temp", current_temp)
            #dpg.set_value("max_temp", max_temp)
            #dpg.set_value("min_temp", min_temp)
            #dpg.set_value("sky_stat", sky_stat)


        dpg.render_dearpygui_frame()

#------------------= Apps =------------------#
class built_in_programs:
    def rotating_cube():
        global x_rot, y_rot, z_rot
        import math

        size = 5
        verticies = [
                [-size, -size, -size],  # 0 near side
                [ size, -size, -size],  # 1
                [-size,  size, -size],  # 2
                [ size,  size, -size],  # 3
                [-size, -size,  size],  # 4 far side
                [ size, -size,  size],  # 5
                [-size,  size,  size],  # 6
                [ size,  size,  size],  # 7
                [-size, -size, -size],  # 8 left side
                [-size,  size, -size],  # 9
                [-size, -size,  size],  # 10
                [-size,  size,  size],  # 11
                [ size, -size, -size],  # 12 right side
                [ size,  size, -size],  # 13
                [ size, -size,  size],  # 14
                [ size,  size,  size],  # 15
                [-size, -size, -size],  # 16 bottom side
                [ size, -size, -size],  # 17
                [-size, -size,  size],  # 18
                [ size, -size,  size],  # 19
                [-size,  size, -size],  # 20 top side
                [ size,  size, -size],  # 21
                [-size,  size,  size],  # 22
                [ size,  size,  size],  # 23
            ]

        colors = [
                [255,   0,   0, 150],
                [255, 255,   0, 150],
                [255, 255, 255, 150],
                [255,   0, 255, 150],
                [  0, 255,   0, 150],
                [  0, 255, 255, 150],
                [  0,   0, 255, 150],
                [  0, 125,   0, 150],
                [128,   0,   0, 150],
                [128,  70,   0, 150],
                [128, 255, 255, 150],
                [128,   0, 128, 150]
            ]

        with dpg.window(label="Rotating Cube", width=600, height=600, tag="rc", no_title_bar=True, no_collapse=True, show=False, no_resize=True, no_focus_on_appearing=True, on_close=lambda:(dpg.hide_item("rc"))):

            with dpg.drawlist(width=500, height=500):

                with dpg.draw_layer(tag="main pass", depth_clipping=True, perspective_divide=True, cull_mode=dpg.mvCullMode_Back):

                    with dpg.draw_node(tag="cube"):

                        dpg.draw_triangle(verticies[1],  verticies[2],  verticies[0], color=[0,0,0.0],  fill=colors[0])
                        dpg.draw_triangle(verticies[1],  verticies[3],  verticies[2], color=[0,0,0.0],  fill=colors[1])
                        dpg.draw_triangle(verticies[7],  verticies[5],  verticies[4], color=[0,0,0.0],  fill=colors[2])
                        dpg.draw_triangle(verticies[6],  verticies[7],  verticies[4], color=[0,0,0.0],  fill=colors[3])
                        dpg.draw_triangle(verticies[9],  verticies[10], verticies[8], color=[0,0,0.0],  fill=colors[4])
                        dpg.draw_triangle(verticies[9],  verticies[11], verticies[10], color=[0,0,0.0], fill=colors[5])
                        dpg.draw_triangle(verticies[15], verticies[13], verticies[12], color=[0,0,0.0], fill=colors[6])
                        dpg.draw_triangle(verticies[14], verticies[15], verticies[12], color=[0,0,0.0], fill=colors[7])
                        dpg.draw_triangle(verticies[18], verticies[17], verticies[16], color=[0,0,0.0], fill=colors[8])
                        dpg.draw_triangle(verticies[19], verticies[17], verticies[18], color=[0,0,0.0], fill=colors[9])
                        dpg.draw_triangle(verticies[21], verticies[23], verticies[20], color=[0,0,0.0], fill=colors[10])
                        dpg.draw_triangle(verticies[23], verticies[22], verticies[20], color=[0,0,0.0], fill=colors[11])

        x_rot = 10
        y_rot = 45
        z_rot = 0

        view = dpg.create_fps_matrix([0, 0, 50], 0.0, 0.0)
        proj = dpg.create_perspective_matrix(math.pi*45.0/180.0, 1.0, 0.1, 100)
        model = dpg.create_rotation_matrix(math.pi*x_rot/180.0 , [1, 0, 0])*\
                                dpg.create_rotation_matrix(math.pi*y_rot/180.0 , [0, 1, 0])*\
                                dpg.create_rotation_matrix(math.pi*z_rot/180.0 , [0, 0, 1])

        dpg.set_clip_space("main pass", 0, 0, 500, 500, -1.0, 1.0)
        dpg.apply_transform("cube", proj*view*model)
#dpg.mvWindowAppItem
    def control_panel():
        from configparser import ConfigParser

        config = ConfigParser()
        config.read("config.ini")

        background_color_str = config.get("theme", "background_color")
        resizable_str = bool(config.get("window", "resizable"))
        ontop_str = bool(config.get("window", "on_top"))
        docking_str = bool(config.get("workspace", "dock"))
        theme_str = config.get("theme", "default_theme")
        font_str = config.get("theme", "font")
        save_window_str = bool(config.get("workspace", "save_window"))
        BACKGROUND_COLOUR = list(background_color_str)

        def selected_font(sender, app_data):
            font = dpg.get_value(sender)
            if font == "Arial":
                config.set("theme", "font", "arial")
                dpg.bind_font(arial_font)
            elif font == "ProggyClean":
                config.set("theme", "font", "proggyclean")
                pass
            elif font == "Consola":
                config.set("theme", "font", "consola")
                dpg.bind_font(consola_font)

        def selected_theme(sender, app_data):
            theme = dpg.get_value(sender)
            if theme == "Modern":
                config.set("theme", "default_theme", "modern")
                dpg.bind_theme(modern_theme)
            elif theme == "Default":
                config.set("theme", "default_theme", "default")
                dpg.bind_theme(0)
            elif theme == "Dark":
                config.set("theme", "default_theme", "dark")
                dpg.bind_theme(dearpygui_ext.themes.create_theme_imgui_dark())
            elif theme == "Light":
                config.set("theme", "default_theme", "light")
                dpg.bind_theme(dearpygui_ext.themes.create_theme_imgui_light())

        def checkbox_callback(section, option, value):
            config.set(section, option, value)

        def color_picker_callback():
            config.set("theme", "background_color", str(dpg.get_value("cp_cp")))


        with dpg.window(label="Control panel", height=750, show=False, width=1200, tag="control_panel", on_close=lambda:(dpg.hide_item("control_panel"), dpg.hide_item("theme"), dpg.hide_item("viewport"))):
            with dpg.group(horizontal=True):
                with dpg.child_window(height=-1, width=250, horizontal_scrollbar=True, tag="main"):
                    dpg.add_button(label="Theme", width=-1, height=18, callback=lambda:(dpg.show_item("theme"), dpg.hide_item("viewport")))
                    dpg.add_button(label="Viewport", width=-1, height=18, callback=lambda:(dpg.show_item("viewport"), dpg.hide_item("theme")))

                # Theme menu
                with dpg.child_window(height=-1, width=-1, horizontal_scrollbar=True, tag="theme", show=False):
                    dpg.add_text("Theme\nYou can customize many things like the theme and the default font\n\n")
                    with dpg.group(horizontal=True):
                        dpg.add_text("Default theme")
                        dpg.add_combo(items=["Default", "Modern", "Light", "Dark"], callback=selected_theme, default_value=theme_str, width=350)

                    with dpg.group(horizontal=True):
                        dpg.add_text("Default font ")
                        dpg.add_combo(items=["Arial", "Consola", "ProggyClean"], callback=selected_font, default_value=font_str, width=350)

                    dpg.add_button(label="Save", callback=lambda:config.write(open("config.ini", "w")))
                
                # Viewport menu
                with dpg.child_window(height=-1, width=-1, horizontal_scrollbar=True, tag="viewport", show=False):
                    dpg.add_text("Viewport\nSettings about the viewport and the window itself\n\n")
                    dpg.add_color_picker(default_value=BACKGROUND_COLOUR, display_type=dpg.mvColorEdit_uint8, picker_mode=dpg.mvColorPicker_bar, alpha_bar=True, alpha_preview=True, label="Clear color", tag="cp_cp", width=250, height=250, callback=color_picker_callback)

                    with dpg.group(horizontal=True):
                        dpg.add_checkbox(label="Enable Dock", tag="enable_dock", default_value=docking_str, callback=lambda:checkbox_callback("workspace", "dock", str(dpg.get_value("enable_dock"))))
                        dpg.add_checkbox(label="Enable Window Position and size saving", tag="ewpass", default_value=save_window_str, callback=lambda:checkbox_callback("workspace", "save_window", str(dpg.get_value("ewpass"))))
                        dpg.add_checkbox(label="Always on top", tag="aot", default_value=ontop_str, callback=lambda:checkbox_callback("window", "on_top", str(dpg.get_value("aot"))))
                        dpg.add_checkbox(label="Resizable", tag="resizable", default_value=resizable_str, callback=lambda:checkbox_callback("window", "resizable", str(dpg.get_value("resizable"))))

                    dpg.add_button(label="Save", callback=lambda:config.write(open("config.ini", "w")))


class ws_programs():
    # Program Manager
    def program_manager():
        """
        Remember Windows 2.0 or 3.0 program manager?
        This is like that, just different

        Features:
        - executes default and system programs
        - opens widgets
        - cool design (probably)
        """
        global pm
        def about():
            with dpg.window(label="About", no_resize=True) as pm_about:                                                                                                                                                                                                                                                                                                                                                                                                                                                         
                dpg.add_text("Program Manager b.2.0\nThe main application of Workspace that manages applications\n\n\nNOTE:\nProgram Manager is in development, bugs, issues or unfinished features might appear when using.")
                center_window(pm_about)


        with dpg.window(label="Program Manager", width=600, height=400, tag="program_manager", show=False, no_close=True) as pm:
            with dpg.menu_bar():
                with dpg.menu(label="Program Manager"):
                    dpg.add_menu_item(label="About", callback=about)

                with dpg.menu(label="Programs"):
                    with dpg.menu(label="Workspace programs"):
                        with dpg.menu(label="System"):
                            dpg.add_menu_item(label="Control panel",callback=lambda:(center_window("control_panel"), dpg.show_item("control_panel")))

                        dpg.add_menu_item(label="XTerminal", callback=lambda:(dpg.show_item("xterm"))) # , dpga.add("opacity", "xterm", 0, 1, [.16,.66,.83,.67], 10, loop="")
                        dpg.add_menu_item(label="MailBox", callback=lambda:dpg.show_item("mail_box"))
                        dpg.add_menu_item(label="pcall editor", callback=lambda:dpg.show_item("pcall_editor"))
                        dpg.add_menu_item(label="Vertex Engine", callback=lambda:(center_window("vertex_engine"), dpg.show_item("vertex_engine")))
                        dpg.add_menu_item(label="Image Viewer", callback=programs.image_viewer)
                        dpg.add_menu_item(label="Explorer", callback=programs.explorer)
                        dpg.add_menu_item(label="Text Editor", callback=lambda:dpg.show_item(programs.te))
                        dpg.add_menu_item(label="PDF Viewer", callback=lambda:dpg.show_item("pdf_viewer"))
                        dpg.add_menu_item(label="ppack packer", callback=lambda:dpg.show_item("ppack_pack"))
                        dpg.add_menu_item(label="Video Player", callback=programs.video_player)
                        dpg.add_menu_item(label="Paint", callback=lambda:(dpg.show_item("paint"), dpg.show_item("paint_bt")))
                        dpg.add_menu_item(label="Web Browser", callback=programs.web_browser)

                        with dpg.menu(label="Debug/Test programs"):
                            dpg.add_menu_item(label="Video Capture", callback=programs.video_capture)
                            dpg.add_menu_item(label="Node Editor", callback=programs.node_editor)
                            dpg.add_menu_item(label="Plots XY", callback=programs.plots_xy)
                            dpg.add_menu_item(label="Spectrum", callback=programs.spectrum)
                            dpg.add_menu_item(label="Empty window", callback=programs.empty_window)
                            dpg.add_menu_item(label="Widget test", callback=widgets.widget_test)

                    with dpg.menu(label="DPG programs"):
                        dpg.add_menu_item(label="About", callback=dpg.show_about)
                        dpg.add_menu_item(label="ImGui Demo", callback=dpg.show_imgui_demo)
                        dpg.add_menu_item(label="Font manager", callback=dpg.show_font_manager)
                        dpg.add_menu_item(label="ImPlot Demo", callback=dpg.show_implot_demo)
                        dpg.add_menu_item(label="Debug", callback=dpg.show_debug)
                        dpg.add_menu_item(label="Style Editor", callback=dpg.show_style_editor)
                        dpg.add_menu_item(label="Item Registry", callback=dpg.show_item_registry)
                        dpg.add_menu_item(label="Metrics", callback=dpg.show_metrics)
                        dpg.add_menu_item(label="Documentation", callback=dpg.show_documentation)

                    with dpg.menu(label="DearPyGui_ext"):
                        dpg.add_menu_item(label="Logger", callback=lambda:dpg.show_item(log.window_id))
                
                with dpg.menu(label="Widgets"):
                    dpg.add_menu_item(label="Weather", callback=widgets.weather)
                    dpg.add_menu_item(label="Quick note", callback=widgets.quick_note)
                    dpg.add_menu_item(label="Rotating cube", callback=lambda:dpg.show_item("rc"))

                
                with dpg.menu(label="Window"):
                    dpg.add_menu_item(label="Center window", callback=lambda:center_window(pm))

            with dpg.group(horizontal=True):
                dpg.add_text(f"00:00:00", tag="pm_time")
                dpg.add_text(f"00/00/0000", tag="pm_date", indent=512)
                dpg.add_text(f"\n\n\n\n\n\n\nWorkspace {version}\n\n\n\n\n\n\n\n\n\n\n\n\n\n", indent=486/2)
            dpg.add_text(f"error", tag="pm_disk_total")
            dpg.add_text(f"error", tag="pm_disk_usage")
            dpg.add_text(f"error", tag="pm_disk_free")


    def ws_menu_bar():
        global ws_button, ws_menubg
        with dpg.viewport_menu_bar(tag="ws_menu_bar"):
            def save_init():
                dpg.save_init_file("win.ini")

            def about():
                with dpg.window(label="About", no_resize=True) as ws_about:
                    dpg.add_text("Workspace Desktop Interface 2023\n\nWorkspace was originally made in C# using a TUI library Terminal.Gui\nThis version of Workspace is made in Python using DearPyGui, more modern and has a lot of features for more applications\n\n\nWhat's new in b.2.1\n - Improved DearPyGui start up and shutdown speed\n - Improved Workspace applications\n - New programs\n - Improved the theme selection in control panel\n - Improved the Modern theme\n\t - added more transparency to the widgets\n\t - borders are now disabled\n - Added the Aero and Mica effect\n\n\nPlanned features:\n - Improving the new programns\n - Adding new features\n - Support for Mac and Linux\n\n\n\n\nWorkspace is in development, bugs, issues or unfinished features might appear when using.")
                    center_window(ws_about)
            def enable_dock():
                def select_dock(sender, unused, user_data):
                    if user_data[1]:
                        config.set("workspace", "DOCK", "True")
                        config.write(open("config.ini", "w"))
                        dpg.delete_item(user_data[0])
                    else:
                        dpg.delete_item(user_data[0])

                message_box("Workspace", "Workspace needs to restart", select_dock)
            
            def disable_dock():
                def select_dock(sender, unused, user_data):
                    if user_data[1]:
                        config.set("workspace", "DOCK", "False")
                        config.write(open("config.ini", "w"))
                        dpg.delete_item(user_data[0])
                    else:
                        dpg.delete_item(user_data[0])

                message_box("Workspace", "Workspace needs to restart", select_dock)

            with dpg.theme() as ws_button:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(dpg.mvThemeCol_Button, (0,0,0,0), category=dpg.mvThemeCat_Core)
                    dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 0, category=dpg.mvThemeCat_Core)

        
                    

            dpg.add_button(label="00:00:00", tag="ws_mb_time", height=17)
            dpg.bind_item_theme("ws_mb_time", ws_button)
            
            with dpg.menu(label="Workspace", tag="ws_menubar", show=False):
                dpg.add_menu_item(label="About", callback=about)  
                with dpg.menu(label="Window"):
                    dpg.add_menu_item(label="Enable Aero effect", callback=ws_effects.setAeroEffect)
                    dpg.add_menu_item(label="Enable Mica effect", callback=lambda:(ws_effects.setMicaEffect(), ws_effects.setMicaEffect()))
                    dpg.add_separator()
                    dpg.add_menu_item(label="Restore window", callback=ws_effects.restoreBackground)
                with dpg.menu(label="System"):
                    with dpg.menu(label="Dock"):
                        dpg.add_menu_item(label="Enable dock", callback=enable_dock)
                        dpg.add_menu_item(label="Disable dock", callback=disable_dock)
                    with dpg.menu(label="Current workspace"):
                        dpg.add_menu_item(label="Save window position", callback=save_init)
                    
                dpg.add_menu_item(label="Quit", filter_key="ALT+F4",callback=lambda:message_box("Workspace", "Are you sure you want to quit Workspace?", ws_quit)) 
            

    def load_ws():
        import time,os
        global lws, prog_status, is_load

        is_load = True
        prog_status = 0

        def add_value_prog_stat(value):
            global prog_status
            prog_status += value
            dpg.set_value("lws_prog_status", 1/100 * prog_status)

        def change_lws_status(text):
            dpg.set_value("lws_status", text)

        def run_task():
            load_time = .0
            change_lws_status("Please wait...")
            time.sleep(load_time)
            change_lws_status("Starting up")
            change_lws_status("checking system folders")
            time.sleep(1)
            change_lws_status("checking system folders (workspace)")
            if os.path.exists("workspace"):
                center_window(lws)
                center_window(lws)
                center_window(lws)
                add_value_prog_stat(10)
                change_lws_status("checking system folders (windoweffect)")
                time.sleep(load_time)
            if os.path.exists("windoweffect"):
                center_window(lws)
                center_window(lws)
                center_window(lws)
                add_value_prog_stat(10)
                change_lws_status("checking system folders (ppack)")
                time.sleep(load_time)
            if os.path.exists("ppack"):
                center_window(lws)
                center_window(lws)
                center_window(lws)
                add_value_prog_stat(10)
                time.sleep(load_time)
            change_lws_status("checking system files")
            time.sleep(1)
            if os.path.exists("config.ini"):
                center_window(lws)
                center_window(lws)
                center_window(lws)
                print("config")
                add_value_prog_stat(10)
                change_lws_status("checking system files (widgets.py)")
                time.sleep(load_time)
                print("ended")
            if os.path.exists("widgets.py"):
                center_window(lws)
                center_window(lws)
                center_window(lws)
                print("widgets")
                add_value_prog_stat(10)
                change_lws_status("checking system files (tools.py)")
                time.sleep(load_time)
            if os.path.exists("tools.py"):
                center_window(lws)
                center_window(lws)
                center_window(lws)
                print("tools")
                add_value_prog_stat(10)
                change_lws_status("checking system files (programs.py)")
                time.sleep(load_time)
            if os.path.exists("programs.py"):
                center_window(lws)
                center_window(lws)
                center_window(lws)
                print("programs")
                add_value_prog_stat(10)
                change_lws_status("checking system files (pm_error1.vbs)")
                time.sleep(load_time)
            if os.path.exists("programs.py"):
                center_window(lws)
                center_window(lws)
                center_window(lws)
                add_value_prog_stat(10)
                change_lws_status("checking system files (ws_warn1.vbs)")
                time.sleep(load_time)
            if os.path.exists("windoweffect/__init__.py"):
                center_window(lws)
                center_window(lws)
                center_window(lws)
                add_value_prog_stat(10)
                change_lws_status("checking system files (windoweffect/c_structures.py)")
                time.sleep(load_time)
            if os.path.exists("windoweffect/window_effect.py"):
                center_window(lws)
                center_window(lws)
                center_window(lws)
                add_value_prog_stat(10)
                change_lws_status("checking system files (ppack/ppack.py)")
                time.sleep(load_time)
            if os.path.exists("ppack/ppack.py"):
                center_window(lws)
                center_window(lws)
                center_window(lws)
                add_value_prog_stat(10)
                change_lws_status("finishing up...")
                time.sleep(load_time)
            time.sleep(load_time)
            change_lws_status("importing themes")
            import_themes()
            time.sleep(load_time)
            change_lws_status("importing fonts")
            import_fonts()
            time.sleep(load_time)
            change_lws_status("setting up config.ini")
            time.sleep(load_time)
            change_lws_status("setting up config.ini (dock)")
            load_dock()
            time.sleep(load_time)
            change_lws_status("setting up config.ini (theme)")
            load_theme()
            time.sleep(load_time)
            change_lws_status("setting up config.ini (font)")
            load_font()
            time.sleep(load_time)
            change_lws_status("loadind hadlers")
            load_handlers()
            time.sleep(load_time)
            change_lws_status("loading programs")
            load_programs()
            time.sleep(load_time)
            change_lws_status("loading workspace menubar (this window will close)")
            time.sleep(2)
            dpg.delete_item("load_ws")
            time.sleep(2)
            dpg.show_item("program_manager")
            dpg.show_item("ws_menubar")
            center_window("program_manager")


        with dpg.theme() as blank_button_theme: # To make a button look like text
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 0, 0, 0))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (0, 0, 0, 0))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (0, 0, 0, 0))                   

        with dpg.window(label="lws", width=600, height=220, tag="load_ws", no_title_bar=True, no_resize=True, no_move=True) as lws:
            center_window(lws)
            center_window(lws)
            center_window(lws)
            thread = threading.Thread(target=run_task, args=(), daemon=True)
               
            dpg.add_text(f"Workspace {version}\n© 2023 Workspace Desktop Enviroment, All Rights Reserved\n\n\n\n\n\n\n\n\n\n")                 
            dpg.add_text("None", tag="lws_status")             
            dpg.add_progress_bar(default_value=prog_status, tag="lws_prog_status", width=-1) 
            
            thread.start()

        dpga.add("opacity", "load_ws", 0, 1, [.16,.66,.83,.67], 5, loop="")



#------------------= Main =------------------#
os.system('cls' if os.name == 'nt' else 'clear')
print("[DEBUG STARTED]\n\nHello World from Dr. AIT!\nMessages from DPG and Workspace will appear here\n\n")
dpg.create_context()

if platform.system() == "Linux":
    print("WARNING: Workspace is running on Linux, some features may not work.")
elif platform.system() == "Darwin":
    print("WARNING: Workspace is running on MacOS, some features may not work.")
    


log = dearpygui_ext.logger.mvLogger()
dpg.hide_item(log.window_id)
#------------------= Themes =------------------#
log.log("importing themes...")

log.log("importing fonts...")
#dpg.configure_app(init_file="win.ini")
log.log("setting settings from config.ini:")
dpg.create_viewport(title='Workspace', width=1009, height=1009, disable_close=True, clear_color=[0,0,0, 0])
ws_programs.load_ws()


setup_dpg()


log.log("creating viewport")
ws_programs.ws_menu_bar()
ws_programs.program_manager()
#------------------= Render Loop =------------------#

log.log_info("STARTING RENDER LOOP")
render_loop()

try:
    dpg.start_dearpygui()
finally:
    print("\n\n[DEBUG ENDED]")
    dpg.destroy_context()
